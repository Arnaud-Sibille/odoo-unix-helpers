#!/usr/bin/python3

import argparse

from tools import extract_version_from_db
from create_odoo_db import create_odoo_db


ARGUMENTS = {
    ("db", ): {
        "help": "name of the database",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
    ("--no-switch", ): {
        "action": "store_true",
        "help": "do not switch the branches",
    }
}


def launch_odoo_db(db, extra_args=None, pull=False, no_switch=False):
    version = extract_version_from_db(db) if not no_switch else None
    # create function will just launch if db exists
    create_odoo_db(version, db, extra_args=extra_args, pull=pull)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    launch_odoo_db(args.db, extra_args=extra_args, pull=args.pull, no_switch=args.no_switch)
