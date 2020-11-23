import argparse
import os
import distutils.dir_util
import subprocess

aqua_prefix = "https://github.com/Qiskit/qiskit-aqua/tree/72c116801c1bfd4bb1f074e079590aab08800422/"


def generate_co_authors(paths, aqua_path):
    authors = set()
    for path in paths:
        cmd = ['git', 'shortlog', '--summary', '--follow', '--numbered', '--email']
        cmd.append(path)
        raw = subprocess.run(cmd, cwd=aqua_path, capture_output=True, check=True)
        co_authors_list = raw.stdout.decode('utf8')
        for line in co_authors_list.splitlines():
            authors.add(' '.join(line.split()[1:]))
    return authors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('terra_path',
                        help='Path to local terra checkout')
    parser.add_argument('aqua_path',
                        help='Path to local aqua checkout')
    parser.add_argument('dest_dir',
                        help='Destination dir in terra repo (relative to repo root)')
    parser.add_argument('paths', nargs='+',
                        help="Paths in aqua (relative to repo root) to copy")
    args = parser.parse_args()

    authors = generate_co_authors(args.paths, args.aqua_path)
    dest_dir = os.path.join(args.terra_path, args.dest_dir)
    dest_module = args.dest_dir.replace('/', '.')
    links = []
    sources = []
    for path in args.paths:
        src_path = os.path.join(args.aqua_path, path)
        distutils.dir_util.copy_tree(src_path, dest_dir)
        sources.append(path.replace('/', '.'))
        links.append(aqua_prefix + path)

    commit_msg = """Migrate %s from qiskit-aqua to qiskit-terra
                      
This commit migrates the amplitude amplifier algorithms modules from
the qiskit-aqua package to live in %s
                      
This module was originally copied from:
%s                    
you can refer to that for the full development history leading
up until this point.  
                      
%s                    
""" % (' & '.join(sources), dest_module, '\n'.join(links),
       '\n'.join(['Co-authored-by: %s' % x for x in authors]))
    cmd = ['git', 'add', dest_dir]
    subprocess.run(cmd, cwd=args.terra_path, check=True)
    cmd = ['git', 'commit', '-m', commit_msg]
    subprocess.run(cmd, cwd=args.terra_path, check=True)


if __name__ == '__main__':
    main()
