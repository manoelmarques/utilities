"""
Python script to migrate issues to another repo
https://github.com/PyGithub/PyGithub
"""

import argparse
from argparse import ArgumentParser
from github import Github

GITHUB_IDS = {
}


def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser(description='Migrate issues.')
    parser.add_argument('ghe_token',
                        help='github.ibm.com token')
    parser.add_argument('ghe_repo',
                        help='Repo name')
    parser.add_argument('gh_token',
                        help='gihub.com token')
    parser.add_argument('gh_repo',
                        help='Repo name')
    args = parser.parse_args()

    ghe = Github(base_url="https://github.ibm.com/api/v3", login_or_token=args.ghe_token)
    ghe_repo = ghe.get_repo(args.ghe_repo)

    gh = Github(args.gh_token)
    gh_repo = gh.get_repo(args.gh_repo)
    gh_issue_titles = []
    for issue in gh_repo.get_issues():
        gh_issue_titles.append(issue.title)

    for idx, issue in enumerate(ghe_repo.get_issues()):
        if issue.title in gh_issue_titles:
            continue

        print(idx, issue.title)
        try:
            # print(issue.user.email)
            github_id = GITHUB_IDS[issue.user.email]
            body = f"Migrated from Enterprise Github.\n" \
                   f"Creator: @{github_id}\n\n" + issue.body
            ret_issue = gh_repo.create_issue(title=issue.title, body=body)
            if issue.comments:
                comments = issue.get_comments()
                for comment in comments:
                    github_id = GITHUB_IDS[comment.user.email]
                    body = f"Creator: @{github_id}\n\n" + comment.body
                    ret_issue.create_comment(body)
        except Exception as ex:
            print(str(ex))


if __name__ == '__main__':
    main()
