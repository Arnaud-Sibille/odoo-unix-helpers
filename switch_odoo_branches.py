#!/usr/bin/python3

import argparse
import os

from tools import get_value_from_odoo_config, execute_command, pull_repo, get_odoo_repo_path, get_addons_path


ARGUMENTS = {
    ("version", ) : {
        "help": "version to switch the versionned odoo addons to",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
}


def switch_repo(repo_path, branch):
    switch_command = [
        "git",
        "-C",
        repo_path,
        "switch",
        branch,
    ]
    execute_command(switch_command)

def get_versionned_addons_path():
    try: 
        return get_value_from_odoo_config("versionned_addons_path")
    except:
        return get_value_from_odoo_config("addons_path")

def switch_odoo_branches(version, pull=False):
    odoo_dir = get_odoo_repo_path()
    switch_repo(odoo_dir, version)
    if pull:
        pull_repo(odoo_dir)

    addons_path_to_switch = get_versionned_addons_path().split(',')
    for addon_path in get_addons_path():
        # to avoid considering again the community repo
        if addon_path.startswith(odoo_dir):
            continue
        if addon_path in addons_path_to_switch:
            switch_repo(addon_path, version)
        if pull:
            pull_repo(addon_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    switch_odoo_branches(args.version, args.pull)
