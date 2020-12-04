"""
This python script is supposed to run from inside the repo root folder
"""
from typing import List
import os
import sys


def generate_co_authors(paths):
    from utilities.command import execute
    authors = set()
    for path in paths:
        # cmd = ['git', 'shortlog', '--summary', '--follow', '--numbered', '--email', '--', path]
        # cmd = ['git', 'shortlog', '-sne', '--', path]
        cmd = ['git', 'log', '--follow', path]
        out = execute(cmd, cwd=os.getcwd())
        co_authors_list = out.strip().decode('utf8')
        for line in co_authors_list.splitlines():
            if 'Author:' in line:
                authors.add(' '.join(line.split()[1:]))
    return sorted(authors, key=str.casefold)


def main(paths: List[str], dest_mod: str, prefix: str) -> None:
    authors = generate_co_authors(paths)
    links = []
    sources = []
    for path in paths:
        sources.append(path)
        links.append(prefix + path)

    msg = 'Migrate:\n\n' + '\n'.join(sources) + '\n\nfrom qiskit-aqua to qiskit-terra.\n'
    msg += 'This commit migrates the above from the qiskit-aqua package '
    # msg += 'to live in qiskit.utils and qiskit.exceptions (last 2 files).\n'
    msg += f'to live in {dest_mod}.\n'
    msg += 'They were originally copied from:\n\n' + '\n'.join(links) + '.\n\n'
    msg += 'You can refer to that for the full development history leading up until this point.\n\n'
    msg += '\n'.join(['Co-authored-by: %s' % x for x in authors])

    print(msg)

    with open('msg.txt', 'w') as file:
        file.write(msg)


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import utilities.globals as glb
    # main(glb.UTILS_ROOT, 'qiskit.utils', glb.aqua_prefix_root)
    main(glb.OP_FLOW, 'qiskit.opflow', glb.aqua_prefix_opfl)
    # main(glb.ALGORITHMS, 'qiskit.algorithms', glb.aqua_prefix_algo)
