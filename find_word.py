#!/usr/bin/python3

import argparse
import subprocess

from tools import get_addons_path


ARGUMENTS = {
    ("word", ): {
        "help": "wordto look for",
    },
}


def find_word(word):
    search_pattern = f'[^A-Za-z0-9_]{word}[^A-Za-z0-9_]'
    addons_path = get_addons_path()
    for addon_path in addons_path:
        grep_command = [
            'grep',
            '-n',
            '-r',
            '-E',
            '--include',
            '*.py',
            '--include',
            '*.js',
            '--include',
            '*.xml',
            search_pattern,
            addon_path,
        ]
        subprocess.run(grep_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    find_word(args.word)
