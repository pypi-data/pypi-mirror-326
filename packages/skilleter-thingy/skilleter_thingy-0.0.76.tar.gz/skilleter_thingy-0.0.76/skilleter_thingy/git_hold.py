#!/usr/bin/env python3
"""Archive one or more branches by tagging the branch then deleting it
   The branch tag is 'archive/BRANCH_NAME'"""

import sys
import argparse
import fnmatch

import thingy.colour as colour
import thingy.git as git

################################################################################
# Prefix for tags representing archived branches

ARCHIVE_PREFIX = 'archive/'

################################################################################

def archive_tag_name(branch):
    """Return the tag name for an archive branch"""

    return f'{ARCHIVE_PREFIX}{branch}'

################################################################################

def archive_branch_name(tag):
    """Return the branch name for an archive tag"""

    if not tag.startswith(ARCHIVE_PREFIX):
        raise git.GitError(f'{tag} is not an archive tag')

    return tag[len(ARCHIVE_PREFIX):]

################################################################################

def archive_tags():
    """Return the list of current archive tags"""

    return [tag for tag in git.tags() if tag.startswith(ARCHIVE_PREFIX)]

################################################################################

def archive_branches(branches):
    """Archive one or more branches"""

    tags = archive_tags()
    current_branch = git.branch()

    for branch in branches:
        if not git.isbranch(branch):
            colour.error(f'[RED:ERROR:] Branch {branch} does not exist')

        if archive_tag_name(branch) in tags:
            colour.error(f'[RED:ERROR:] An archive tag already exists for branch {branch}')

        if branch == current_branch:
            colour.error('[RED:ERROR:] Cannot archive the current branch')

    for branch in branches:
        tag_name = archive_tag_name(branch)

        git.set_tag(tag_name, branch)
        git.delete_branch(branch, force=True)

    for remote in git.remotes():
        git.push(repository=remote, tags=True)

################################################################################

def list_archive_branches(branches):
    """List archive branches, optionally only those matching entries in the
       branches parameter"""

    tags = archive_tags()

    if branches:
        report = set()

        for branch in branches:
            for tag in tags:
                branch_name = archive_branch_name(tag)
                if branch_name not in report and fnmatch.fnmatch(branch_name, branch):
                    report.add(branch_name)
    else:
        report = set(tags)

    for branch_name in sorted(report):
        print(branch_name)

################################################################################

def restore_archive_branches(branches):
    """Restore archived branches"""

    tags = archive_tags()

    for branch in branches:
        if archive_tag_name(branch) not in tags:
            colour.error(f'[RED:ERROR:] Archive branch {branch} does not exist')

    archive_tag_names = []

    for branch in branches:
        archive_tag = archive_tag_name(branch)
        archive_tag_names.append(archive_tag)

        git.checkout(branch, commit=archive_tag)
        git.delete_tag(archive_tag)

    for remote in git.remotes():
        git.push(repository=remote, delete=True, refspec=archive_tag_names)

################################################################################

def main():
    """Main function"""

    parser = argparse.ArgumentParser(description='Archive, list or recover one or more Git branches')
    parser.add_argument('--list', '-l', action='store_true', help='List archived branches')
    parser.add_argument('--restore', '-r', action='store_true', help='Restore archived branches')
    parser.add_argument('branches', nargs='*', help='Branches')

    args = parser.parse_args()

    if args.list and args.restore:
        colour.error('[RED:ERROR:] The list and restore options cannot be specified together')

    if not args.branches and not args.list:
        colour.error('[RED:ERROR:] No branches specified')

    if args.list:
        list_archive_branches(args.branches)
    elif args.restore:
        restore_archive_branches(args.branches)
    else:
        archive_branches(args.branches)

################################################################################

def git_hold():
    """Entry point"""

    try:
        main()

    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    git_hold()
