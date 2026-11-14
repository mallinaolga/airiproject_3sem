"""Detached Windows supervisor: one source per process, persistent checkpoints."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from collections import Counter
import msvcrt

BASE = Path(__file__).resolve().parent
ROOT = BASE/'examples/all_bracings_200'
def now(): return datetime.now(timezone.utc).isoformat()
def save(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    temp.replace(path)

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for name in ('logs','reports','models'): (ROOT/name).mkdir(exist_ok=True)
    lock = (ROOT/'supervisor.lock').open('a+b')
    lock.seek(0); lock.write(b'0'); lock.flush(); lock.seek(0)
    try: msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError: raise SystemExit('Another supervisor is already running')
    manifest = ROOT/'manifest.json'
    state = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else dict(schema='airi-200-v1', models={})
    if state.get('schema') != 'airi-200-v1': raise SystemExit('Incompatible existing manifest')
    state.update(pid=os.getpid(), started=now(), total=200, timeout_seconds=600, status='running', interpreter=sys.executable)
    save(manifest,state)
    for i in range(1,201):
        key=f'model_{i:03d}'
        old=state['models'].get(key,{})
        if old.get('status') in ('geometry_verified','rejected','error','timeout'): continue
        if old.get('worker_pid'):
            # Only terminate a surviving worker if its command line still matches this output.
            ps = "$p=Get-CimInstance Win32_Process -Filter 'ProcessId="+str(old['worker_pid'])+"'; if($p -and $p.CommandLine.Contains('"+old['output'].replace("'","''")+"')) {taskkill /PID "+str(old['worker_pid'])+" /T /F}"
            subprocess.run(['powershell','-NoProfile','-Command',ps],capture_output=True)
        # Interrupted attempts are preserved; completed workers are adopted.
        folder=ROOT/'models'/key
        folder.mkdir(exist_ok=True)
        completed=list(folder.glob('attempt_*/manifest.json'))
        if completed:
            found=json.loads(completed[-1].read_text(encoding='utf-8'))
            if found.get('status') in ('complete','incomplete'):
                old.update(status='geometry_verified' if found['successful_count'] else 'rejected', result=found, ended=now())
                state['models'][key]=old; save(manifest,state); continue
        attempt=folder/f'attempt_{len(list(folder.glob("attempt_*")))+1:03d}'
        record=dict(status='running', seed=140000+i, started=now(), output=str(attempt))
        state['models'][key]=record; save(manifest,state)
        out=(ROOT/'logs'/f'{key}_{attempt.name}.stdout.log').open('wb')
        err=(ROOT/'logs'/f'{key}_{attempt.name}.stderr.log').open('wb')
        code='from cadgen.auto_assembly import generate_auto_batch; from cadgen.assembly_geometry import AssemblySettings; import sys; generate_auto_batch(sys.argv[1],count=1,seed=int(sys.argv[2]),connection="all",max_attempts=1,geometry=AssemblySettings(path_steps=4),check_sequence=False)'
        start=time.monotonic()
        child=subprocess.Popen([sys.executable,'-c',code,str(attempt),str(record['seed'])],cwd=BASE,stdout=out,stderr=err)
        record['worker_pid']=child.pid; save(manifest,state)
        try:
            child.wait(timeout=600)
            result_path=attempt/'manifest.json'
            result=json.loads(result_path.read_text(encoding='utf-8')) if result_path.exists() else {}
            record.update(status=('geometry_verified' if result.get('successful_count') else 'rejected') if child.returncode==0 else 'error', result=result, exit_code=child.returncode)
        except subprocess.TimeoutExpired:
            subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],stdout=err,stderr=err)
            child.wait()
            record.update(status='timeout', reason='600 second processing limit exceeded; process tree terminated')
        finally:
            out.close(); err.close()
        record.update(ended=now(),elapsed_seconds=time.monotonic()-start)
        save(folder/'checkpoint.json',record); save(manifest,state)
        counts=Counter(r['status'] for r in state['models'].values())
        joints=Counter()
        for r in state['models'].values():
            for a in r.get('result',{}).get('assemblies',[]): joints.update(a.get('connection_types',{}))
        save(ROOT/'reports/results.json',dict(counts=dict(counts),unprocessed=200-sum(counts.values()),joints=dict(joints),total_joints=sum(joints.values())))
    state.update(status='complete',ended=now()); save(manifest,state)

if __name__=='__main__': main()
