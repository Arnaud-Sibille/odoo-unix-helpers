#!/usr/bin/python3

import argparse
import os
import subprocess


ARGUMENTS = {
    ("file_paths", ): {
        "help": "paths of the files to restore",
        "nargs": "+",
    },
}


def restore_files_to_previous_commit(file_paths):
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} doesn't exist")
        with open(file_path, 'w') as file:
            command = [
                'git',
                'show',
                f'HEAD^:{file_path}',
            ]
            subprocess.run(command, stdout=file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    restore_files_to_previous_commit(args.file_paths)
