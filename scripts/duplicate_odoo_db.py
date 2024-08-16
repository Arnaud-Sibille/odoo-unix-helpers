#!/usr/bin/python3

import argparse
import os

from utils.tools import get_filestore_path, get_filestore_dir, execute_command


ARGUMENTS = {
    ("db_template", ): {
        "help": "database to duplicate",
    },
    ("new_db", ): {
        "help": "name of the new database",
    },
}


def duplicate_filestore(db_template, new_db):
    template_filestore_path = get_filestore_path(db_template)
    if template_filestore_path:
        new_filestore_path = os.path.join(get_filestore_dir(), new_db)
        duplicate_filestore_command = [
            "cp",
            "-r",
            template_filestore_path,
            new_filestore_path,
        ]
        execute_command(duplicate_filestore_command)

def duplicate_odoo_db(db_template, new_db):
    duplicate_filestore(db_template, new_db)
    duplicate_db_command = [
        "createdb",
        "-T",
        db_template,
        new_db,
    ]
    execute_command(duplicate_db_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    duplicate_odoo_db(args.db_template, args.new_db)
