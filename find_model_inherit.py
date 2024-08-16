#!/usr/bin/python3

import argparse
import subprocess

from tools import get_addons_path


ARGUMENTS = {
    ("model_name", ): {
        "help": "name of the model to look for",
    },
}


def find_model_def(model_name, extra_args=[]):
    search_pattern = r'\s_inherits? = .*[\'"]' + model_name + r'[\'"]'
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
    find_model_def(args.model_name, extra_args=extra_args)
