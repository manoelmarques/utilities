"""
This python script is supposed to run from inside the repo root folder
"""
from typing import List
import os
import sys

CMD = ['git', 'filter-repo', '--force']


def prepare_array(src: List[str]) -> List[str]:
    ret_list = []
    for path in src:
        ret_list.append('--path')
        ret_list.append(path)
    return ret_list


def main(cmd: List[str]) -> None:
    from utilities.command import execute
    from utilities.filter_repo import fix_links
    out = execute(cmd=cmd, cwd=os.getcwd())
    print(out.strip().decode('utf-8'))
    fix_links()


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import utilities.globals as glb
    # main(CMD + prepare_array(glb.OP_FLOW))
    # main(CMD + prepare_array(glb.ALGORITHMS))
    # main(CMD + prepare_array(glb.OPTIMIZATION_ROOT))
    # main(CMD + prepare_array(glb.FINANCE_ROOT))
    # main(CMD + prepare_array(glb.CHEMISTRY_ROOT))
    # main(CMD + prepare_array(glb.NATURE_ROOT))
    main(CMD + prepare_array(glb.ML_ROOT))
