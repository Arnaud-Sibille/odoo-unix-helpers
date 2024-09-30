#!/usr/bin/python3

import argparse
import subprocess

from utils.tools import get_addons_path


ARGUMENTS = {
    ("model_name", ): {
        "help": "name of the model to look for",
    },
}


def find_model_files(model_name, extra_args=[]):
    res = ""
    search_pattern = r'\s(_inherit|_name) = .*[\'"]' + model_name + r'[\'"]'
    addons_path = get_addons_path()
    for addon_path in addons_path:
        grep_command = [
            'grep',
            '-l',
            '-r',
            '-E',
            '--include',
            '*.py',
            search_pattern,
            addon_path,
        ]
        output = subprocess.run(grep_command + extra_args, capture_output=True, text=True)
        res += output.stdout

    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    print(find_model_files(args.model_name, extra_args=extra_args), end="")
