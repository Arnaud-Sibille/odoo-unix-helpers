#!/usr/bin/python3

import argparse
import os

from tools import get_value_from_odoo_config, execute_command, pull_repo, get_odoo_repo_path


ARGUMENTS = {
    ("version", ) : {
        "help": "version to switch the versionned odoo addons to",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
}


def switch_repo(repo_path, branch, pull=False):
    switch_command = [
        "git",
        "-C",
        repo_path,
        "switch",
        branch,
    ]
    execute_command(switch_command)
    if pull:
        pull_repo(repo_path)

def get_versionned_addons_path():
    try: 
        return get_value_from_odoo_config("versionned_addons_path")
    except:
        return get_value_from_odoo_config("addons_path")

def switch_odoo_branches(version, pull=False):
    odoo_dir = get_odoo_repo_path()
    switch_repo(odoo_dir, version, pull)

    addons_path_to_switch = get_versionned_addons_path()
    for addon_path_to_switch in addons_path_to_switch.split(','):
        # to avoid pulling again the community repo
        if not addon_path_to_switch.startswith(odoo_dir):
            switch_repo(addon_path_to_switch, version, pull)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    switch_odoo_branches(args.version, args.pull)
