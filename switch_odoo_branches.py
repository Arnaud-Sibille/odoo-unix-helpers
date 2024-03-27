#!/usr/bin/python3

import argparse
import os

from tools import get_value_from_odoo_config, execute_command


ARGUMENTS = {
    ("version", ) : {
        "help": "version to switch the odoo addons to",
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
    pull_command = [
        "git",
        "-C",
        repo_path,
        "pull",
    ]
    execute_command(switch_command)
    if pull:
        execute_command(pull_command)

def switch_odoo_branches(version, pull=False):
    odoo_bin_path = get_value_from_odoo_config("odoo_bin_path")
    odoo_dir = os.path.dirname(odoo_bin_path)
    switch_repo(odoo_dir, version, pull)

    addons_path = get_value_from_odoo_config("addons_path")
    for addon_path in addons_path.split(','):
        # to avoid pulling two times the community repo
        if not addon_path.startswith(odoo_dir):
            switch_repo(addon_path, version, pull)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    switch_odoo_branches(args.version, args.pull)
