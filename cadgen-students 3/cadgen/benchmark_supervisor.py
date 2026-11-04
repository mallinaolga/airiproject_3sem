"""Resume a saved corpus with a wall-clock deadline outside the CAD worker."""
import argparse
import faulthandler
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

DEFAULT_ROOT=Path(__file__).resolve().parents[1]/'generations/assemblies/benchmark_100'


def save(path,value):
    temp=path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,indent=2,ensure_ascii=False))
    temp.replace(path)


def read(path,default=None):
    try:return json.loads(path.read_text())
    except (FileNotFoundError,json.JSONDecodeError):return default


def terminate_group(process,grace=3):
    """SIGKILL reaches native code and surviving descendants even without GIL."""
    try:os.killpg(process.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:process.wait(timeout=grace)
    except subprocess.TimeoutExpired:pass
    try:os.killpg(process.pid,signal.SIGKILL)
    except ProcessLookupError:pass
    process.wait()


def run_bounded(command,log,seconds,*,cwd=None):
    started=time.monotonic()
    with log.open('ab',buffering=0) as stream:
        process=subprocess.Popen(command,stdout=stream,stderr=subprocess.STDOUT,cwd=cwd,start_new_session=True)
        try:
            process.wait(timeout=seconds)
            return dict(timeout=False,returncode=process.returncode,elapsed_seconds=time.monotonic()-started,pid=process.pid)
        except subprocess.TimeoutExpired:
            terminate_group(process)
            return dict(timeout=True,returncode=process.returncode,elapsed_seconds=time.monotonic()-started,pid=process.pid)
        except BaseException:
            terminate_group(process)
            raise


def worker(root,name):
    diagnostics=root/'new/.supervisor'/name
    with (diagnostics/'python_stacks.log').open('a') as trace:
        faulthandler.enable(file=trace,all_threads=True)
        faulthandler.dump_traceback_later(60,repeat=True,file=trace)
        try:
            from .constructive_workflow import compare
            from .assembly_geometry import AssemblySettings
            from .constructive_geometry import ConstructiveSettings
            compare(root/'sources',root/'new/.workers'/name,AssemblySettings(),ConstructiveSettings(),models=[int(name[6:])])
        finally:faulthandler.cancel_dump_traceback_later()


def resume(root):
    output=root/'new';report_path=output/'report.json'
    control=output/'.supervisor';control.mkdir(exist_ok=True)
    with (control/'lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        report=read(report_path);assert report is not None
        manifest=read(root/'sources/manifest.json');assert len(manifest)==100
        completed={r['model'] for r in report['models']}
        assert len(completed)==len(report['models'])
        for source in manifest:
            name=source['model']
            if name in completed:continue
            target=output/name;worker_root=output/'.workers'/name
            if target.exists() or target.is_symlink() or worker_root.exists():
                raise RuntimeError(f'Refusing to overwrite unfinished or existing results: {name}')
            diag=control/name;diag.mkdir()
            # Worker creates the actual folder; the stable public path is ready
            # immediately and never requires copying or moving active outputs.
            target.symlink_to(Path('.workers')/name/name,target_is_directory=True)
            save(control/'active.json',dict(model=name,status='running',timeout_seconds=900,started_unix=time.time()))
            print('START',name,'deadline_seconds=900',flush=True)
            result=run_bounded([sys.executable,'-m','cadgen.benchmark_supervisor','--root',str(root),'--worker',name],diag/'worker.log',900,cwd=Path(__file__).resolve().parents[1])
            save(diag/'process_result.json',result)
            child=read(worker_root/'report.json',{})
            child_rows=child.get('models',[])
            if not result['timeout'] and child_rows:
                assert len(child_rows)==1 and child_rows[0]['model']==name
                row=child_rows[0]
            else:
                geometry=read(target/'geometry/metadata.json',{})
                status='timeout' if result['timeout'] else 'worker_error'
                row=dict(model=name,assembly_status=status,assembly_success=False,
                    decomposition_success=bool(geometry.get('geometry_success')),
                    components=geometry.get('main_component_count'),
                    assembly_reason='Per-model wall-clock deadline exceeded (900 seconds)' if result['timeout'] else f'Worker exited without a result (code {result["returncode"]})',
                    elapsed_seconds=round(result['elapsed_seconds'],3),timeout_limit_seconds=900 if result['timeout'] else None,
                    diagnostics=f'.supervisor/{name}',partial_files_preserved=True)
                target.resolve().mkdir(parents=True,exist_ok=True)
                save(target/(status+'.json'),dict(row,process=result,files_may_be_incomplete=True))
            row['supervised_wall_seconds']=round(result['elapsed_seconds'],3)
            report['models'].append(row);completed.add(name);report['status']='running'
            save(report_path,report)
            save(control/'active.json',dict(model=name,status=row['assembly_status']))
            print('END',name,row['assembly_status'],flush=True)
        report['status']='complete';report['per_model_timeout_seconds']=900
        save(report_path,report)
        save(control/'active.json',dict(status='complete'))
        print('COMPLETE',len(report['models']),flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=DEFAULT_ROOT);parser.add_argument('--worker')
    args=parser.parse_args()
    if args.worker:worker(args.root.resolve(),args.worker)
    else:resume(args.root.resolve())

if __name__=='__main__':main()
