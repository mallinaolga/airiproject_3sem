import os
from pathlib import Path
import sys
import time
from cadgen.benchmark_supervisor import run_bounded


def test_completed_worker_is_not_timeout(tmp_path):
    result=run_bounded([sys.executable,'-c','print("finished")'],tmp_path/'log',5)
    assert not result['timeout'] and result['returncode']==0
    assert 'finished' in (tmp_path/'log').read_text()


def test_deadline_kills_unresponsive_worker_and_descendant(tmp_path):
    child_pid=tmp_path/'child.pid';partial=tmp_path/'partial.txt'
    code=f'''import os,signal,subprocess,sys,time
signal.signal(signal.SIGTERM,signal.SIG_IGN)
p=subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(120)'])
open({str(child_pid)!r},'w').write(str(p.pid))
open({str(partial)!r},'w').write('preserved')
while True: time.sleep(1)
'''
    started=time.monotonic()
    result=run_bounded([sys.executable,'-c',code],tmp_path/'log',1)
    assert result['timeout'] and time.monotonic()-started<8
    assert partial.read_text()=='preserved'
    pid=int(child_pid.read_text());stat=Path(f'/proc/{pid}/stat')
    for _ in range(100):
        if not stat.exists() or stat.read_text().split()[2]=='Z':break
        time.sleep(.01)
    else:raise AssertionError('Descendant survived deadline')


def test_resume_preserves_finished_rows_and_continues_after_timeout(tmp_path,monkeypatch):
    import json
    import cadgen.benchmark_supervisor as supervisor
    (tmp_path/'sources').mkdir();(tmp_path/'new').mkdir()
    names=[f'model_{i:02d}' for i in range(1,101)]
    (tmp_path/'sources/manifest.json').write_text(json.dumps([dict(model=n) for n in names]))
    original=[dict(model=n,assembly_status='success',assembly_success=True) for n in names[:98]]
    (tmp_path/'new/report.json').write_text(json.dumps(dict(status='running',models=original)))
    calls=[]
    def fake_worker(command,log,seconds,**kwargs):
        name=command[-1];calls.append(name);assert seconds==900
        if name=='model_100':
            folder=tmp_path/'new/.workers'/name;folder.mkdir(parents=True)
            (folder/name).mkdir()
            (folder/'report.json').write_text(json.dumps(dict(models=[dict(model=name,assembly_status='success',assembly_success=True)])))
        return dict(timeout=name=='model_99',returncode=-9 if name=='model_99' else 0,elapsed_seconds=900 if name=='model_99' else 1,pid=123)
    monkeypatch.setattr(supervisor,'run_bounded',fake_worker)
    supervisor.resume(tmp_path)
    report=json.loads((tmp_path/'new/report.json').read_text())
    assert report['status']=='complete' and len(report['models'])==100
    assert report['models'][:98]==original
    assert calls==['model_99','model_100']
    assert report['models'][98]['assembly_status']=='timeout'
    assert (tmp_path/'new/model_99/timeout.json').exists()
    assert report['models'][99]['assembly_success']
    supervisor.resume(tmp_path)
    assert calls==['model_99','model_100']
