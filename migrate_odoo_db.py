#!/usr/bin/python3

import argparse


ARGUMENTS = {
    ("db", ): {
        "help": "name of the database",
    },
    ("target_version", ): {
        "help": "version to migrate to",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
    ("--pull-upgrade", ): {
        "action": "store_true",
        "help": "pull the upgrade repos",
    },
}


def migrate_odoo_db(db, target_version, pull=False, pull_upgrade=False, extra_args=None):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    migrate_odoo_db(args.db, args.target_version, args.pull, args.pull_upgrade, extra_args=extra_args)
