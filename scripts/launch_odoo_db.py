#!/usr/bin/python3

import argparse

from utils.tools import extract_version_from_db, get_odoo_repo_version, get_python_path, launch_odoo
from switch_odoo_branches import switch_odoo_branches


ARGUMENTS = {
    ("db", ): {
        "help": "name of the database",
    },
    ("--shell", ): {
        "action": "store_true",
        "help": "launch the odoo shell",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
    ("--switch", ): {
        "action": "store_true",
        "help": "switch the branches",
    },
}


def launch_odoo_db(db, extra_args=None, shell=False, pull=False, switch=False):
    if switch:
        version = extract_version_from_db(db)
        switch_odoo_branches(version, pull)
    else:
        version = get_odoo_repo_version()
    python_path = get_python_path(version)
    launch_odoo(db, shell=shell, extra_args=extra_args, python_path=python_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    launch_odoo_db(args.db, extra_args=extra_args, shell=args.shell, pull=args.pull, switch=args.switch)
