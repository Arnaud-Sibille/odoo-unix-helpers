#!/usr/bin/python3

import argparse
import subprocess

from tools import get_addons_path


ARGUMENTS = {
    ("field_name", ): {
        "help": "name of the field to look for",
    },
}


def find_field_def(field_name, extra_args=[]):
    search_pattern = r'\b' + field_name + r' = fields\.'
    addons_path = get_addons_path()
    for addon_path in addons_path:
        grep_command = [
            'grep',
            '-n',
            '-r',
            '-E',
            '--include',
            '*.py',
            search_pattern,
            addon_path,
        ]
        subprocess.run(grep_command + extra_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    find_field_def(args.field_name, extra_args=extra_args)
