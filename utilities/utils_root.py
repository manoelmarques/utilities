"""
This python script is supposed to run from inside the repo root folder
"""
import os
import sys

def main():
    from utilities.command import execute
    from utilities.filter_repo import fix_links
    cmd = [
        'git', 'filter-repo',
        '--path', 'qiskit/aqua/utils',
        '--path', 'qiskit/aqua/_logging.py',
        '--path', 'qiskit/aqua/aqua_error.py',
        '--path', 'qiskit/aqua/aqua_globals.py',
        '--path', 'qiskit/aqua/missing_optional_library_error.py',
        '--path', 'qiskit/aqua/quantum_instance.py',
    ]
    out = execute(cmd=cmd, cwd=os.getcwd())
    print(out.strip().decode('utf-8'))
    fix_links()


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(sys.path)
    main()
