import os
import git_filter_repo

MSG1 = """
* fixed imports #4567
"""

MSG = """
  ###  
--#######
Author: Bryce Fuller <bgf024@gmail.com>
Date:   Wed Nov 11 16:26:19 2020 -0600

    MES Factory gradient(#2) support (#1421)
#2222    
    * added gradient to two factory MES methods #22
    
    * fixed imports #4567
    
    * fixed argument name###
    
    * added getters and setters#213
    
    * fixed typehints
#

"""

REPO_NAME = '_REPO_NAME_'


def msg_callback(message):
    repo_name = os.environ.get(REPO_NAME)
    lines = []
    print_msg = False
    for line in message.decode('utf-8').splitlines():
        new_line = ''
        if repo_name is not None and repo_name:
            start_idx = line.find('#')
            while start_idx >= 0:
                new_line += line[:start_idx]
                if start_idx == 0 or (start_idx > 0 and line[start_idx - 1] in ['(', ' ']):
                    str_number = ''
                    for ch in line[start_idx+1:]:
                        if ch.isnumeric():
                            str_number += ch
                        else:
                            break
                    if str_number:
                        new_line += f'{repo_name}#{str_number}'
                        start_idx += len(str_number)
                        print_msg = True
                    else:
                        new_line += '#'
                else:
                    new_line += '#'

                line = line[start_idx+1:]
                start_idx = line.find('#')

        new_line += line
        lines.append(new_line)

    msg = '\n'.join(lines)
    if print_msg:
        print('#######')
        print(msg)
        print('#######')
    return msg.encode('utf-8')


def fix_links(repo: str):
    args = git_filter_repo.FilteringOptions.default_options()
    # args.force = True
    # args.partial = True
    args.debug = True
    args.refs = ['HEAD']
    os.environ[REPO_NAME] = repo
    git_filter_repo.RepoFilter(
        args,
        message_callback=msg_callback).run()
    # print(msg_callback(MSG.encode('utf-8')).decode('utf-8'))


if __name__ == '__main__':
    fix_links()
