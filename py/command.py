from typing import List
import subprocess


def execute(cmd: List[str], cwd: str) -> bytes:
    # construct minimal environment
    env = {}
    for k in ['SYSTEMROOT', 'PATH']:
        v = os.environ.get(k)
        if v is not None:
            env[k] = v
    # LANGUAGE is used on win32
    env['LANGUAGE'] = 'C'
    env['LANG'] = 'C'
    env['LC_ALL'] = 'C'
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env,
                            cwd=cwd)
    stdout, stderr = proc.communicate()
    if proc.returncode > 0:
        raise OSError(f"Command {cmd} exited with code {proc.returncode}: {stderr.strip().decode('utf-8')}")
    return stdout
