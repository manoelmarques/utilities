"""
This python script is supposed to run from inside the repo root folder
"""
from typing import List
import os
import sys

CMD = ['git', 'filter-repo']

UTILS_ROOT = [
    '--path', 'qiskit/aqua/utils/arithmetic.py',
    '--path', 'qiskit/aqua/utils/backend_utils.py',
    '--path', 'qiskit/aqua/utils/circuit_utils.py',
    '--path', 'qiskit/aqua/utils/entangler_map.py',
    '--path', 'qiskit/aqua/utils/measurement_error_mitigation.py',
    '--path', 'qiskit/aqua/utils/name_unnamed_args.py',
    '--path', 'qiskit/aqua/utils/run_circuits.py',
    '--path', 'qiskit/aqua/utils/subsystem.py',
    '--path', 'qiskit/aqua/utils/validation.py',
    '--path', 'qiskit/aqua/aqua_globals.py',
    '--path', 'qiskit/aqua/quantum_instance.py',
]

OP_FLOW = [
    '--path', 'qiskit/aqua/operators',
]


def main(cmd: List[str]) -> None:
    from utilities.command import execute
    from utilities.filter_repo import fix_links
    out = execute(cmd=cmd, cwd=os.getcwd())
    print(out.strip().decode('utf-8'))
    fix_links()


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main(CMD + OP_FLOW)
