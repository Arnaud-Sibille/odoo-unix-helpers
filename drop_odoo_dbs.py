#!/usr/bin/python3

import argparse
import os

from tools import get_filestore_path, execute_command


ARGUMENTS = {
    ("dbs", ): {
        "nargs": "+",
        "help": "databases to drop",
    },
}


def drop_db_filestore(db):
    filestore_path = get_filestore_path(db)
    if filestore_path:
        drop_filestore_command = [
            "rm",
            "-r",
            filestore_path,
        ]
        execute_command(drop_filestore_command)

def drop_odoo_db(db):
    drop_db_filestore(db)
    dropdb_command = [
        "dropdb",
        "--if-exists",
        db,
    ]
    execute_command(dropdb_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    for db in args.dbs:
        drop_odoo_db(db)
