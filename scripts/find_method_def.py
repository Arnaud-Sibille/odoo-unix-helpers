#!/usr/bin/python3

import argparse
import re

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

from find_model_files import find_model_files


ARGUMENTS = {
    ("model_name", ): {
        "help": "Model of the method",
    },
    ("method_name", ): {
        "help": "Method to look for",
    }
}

def print_method(method):
    print(highlight(method.rstrip(), PythonLexer(), TerminalFormatter()))

def find_method_def(method_name, model_name, extra_args=[]):
    search_pattern = r'^ {4}def ' + method_name + r'\('
    non_match_pattern = r'^ {0,4}\S'
    model_files = find_model_files(model_name)
    for filename in model_files.split():
        method = ""
        with open(filename, 'r') as file:
            file_name_printed = False
            in_method = False
            for line in file:
                if re.match(search_pattern, line):
                    in_method = True
                    if not file_name_printed:
                        print(f"{filename}")
                        file_name_printed = True
                elif re.match(non_match_pattern, line):
                    in_method = False
                    if method:
                        print_method(method)
                    method = ""
                if in_method:
                    method += line
        if method:
            print_method(method)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    find_method_def(args.method_name, args.model_name, extra_args=extra_args)
