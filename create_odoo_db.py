#!/usr/bin/python3

import argparse

from switch_odoo_branches import switch_odoo_branches
from tools import launch_odoo, get_python_path, get_odoo_repo_version


ARGUMENTS = {
    ("db", ): {
        "help": "name of the database",
    },
    ("--version", ) : {
        "help": "version of the new db",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
}


def create_odoo_db(version, db, extra_args=None, pull=False):
    if not version:
        version = get_odoo_repo_version()
    else:
        switch_odoo_branches(version, pull)
    python_path = get_python_path(version)
    launch_odoo(db, extra_args=extra_args, python_path=python_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    create_odoo_db(args.version, args.db, extra_args=extra_args, pull=args.pull)
