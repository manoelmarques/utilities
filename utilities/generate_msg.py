"""
This python script is supposed to run from inside the repo root folder
"""
import os
import sys

aqua_prefix = "https://github.com/Qiskit/qiskit-aqua/tree/fe939b1eee848a8dea1810810ff8e90374170e97/"


def generate_co_authors(paths):
    from utilities.command import execute
    authors = set()
    for path in paths:
        cmd = ['git', 'shortlog', '--summary', '--follow', '--numbered', '--email', path]
        out = execute(cmd, cwd=os.getcwd())
        co_authors_list = out.strip().decode('utf8')
        for line in co_authors_list.splitlines():
            authors.add(' '.join(line.split()[1:]))
    return authors


def main():
    paths = [
        'qiskit/aqua/utils/arithmetic.py',
        'qiskit/aqua/utils/backend_utils.py',
        'qiskit/aqua/utils/circuit_utils.py',
        'qiskit/aqua/utils/entangler_map.py',
        'qiskit/aqua/utils/measurement_error_mitigation.py',
        'qiskit/aqua/utils/name_unnamed_args.py',
        'qiskit/aqua/utils/run_circuits.py',
        'qiskit/aqua/utils/subsystem.py',
        'qiskit/aqua/utils/validation.py',
        'qiskit/aqua/aqua_globals.py',
        'qiskit/aqua/quantum_instance.py',
        'qiskit/aqua/aqua_error.py',
        'qiskit/aqua/missing_optional_library_error.py',
    ]
    authors = generate_co_authors(paths)
    dest_module = 'qiskit.utils'
    links = []
    sources = []
    for path in paths:
        sources.append(path)
        links.append(aqua_prefix + path)

    msg = 'Migrate:\n\n' + '\n'.join(sources) + '\n\nfrom qiskit-aqua to qiskit-terra.\n'
    msg += 'This commit migrates the above from the qiskit-aqua package '
    msg += 'to live in qiskit.utils and qiskit.exceptions (last 2 files).\n'
    msg += 'They were originally copied from:\n\n' + '\n'.join(links) + '.\n\n'
    msg += 'You can refer to that for the full development history leading up until this point.\n\n'
    msg += '\n'.join(['Co-authored-by: %s' % x for x in authors])

    print(msg)

    with open('msg.txt', 'w') as file:
        file.write(msg)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
