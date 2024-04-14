#!/usr/bin/python3

import argparse

from tools import extract_version_from_db, get_odoo_repo_version, get_python_path, launch_odoo
from switch_odoo_branches import switch_odoo_branches


ARGUMENTS = {
    ("db", ): {
        "help": "database to execute the script",
    },
    ("script", ): {
        "help": "script to run in the db",
    },
    ("--commit", ): {
        "action": "store_true",
        "help": "commit the script to the database (append `env.cr.commit()`)",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
    ("--no-switch", ): {
        "action": "store_true",
        "help": "do not switch the branches",
    },
}


def execute_odoo_script(db, script_path, extra_args=None, commit=False, pull=False, no_switch=False):
    with open(script_path, 'r') as script:
        input_code = script.read()
        if commit:
            input_code += '\nenv.cr.commit()\n'
    if not no_switch:
        version = extract_version_from_db(db)
        switch_odoo_branches(version, pull)
    else:
        version = get_odoo_repo_version()
    python_path = get_python_path(version)
    print("--- executing script ---")
    launch_odoo(db, input_code=input_code, extra_args=extra_args, python_path=python_path)
    print("*** script executed  ***")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    execute_odoo_script(args.db, args.script, extra_args=extra_args, commit=args.commit, pull=args.pull, no_switch=args.no_switch)
