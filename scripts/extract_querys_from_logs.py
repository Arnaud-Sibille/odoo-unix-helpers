#!/usr/bin/python3

import argparse
import re


ARGUMENTS = {
    ("log_file", ): {
        "help": "Log file to extract queries from (needs to have some sql logs to be extracted)",
    },
}


def extract_querys_from_logs(log_file):
    with open(log_file , 'r') as log_file:
        printing_query = False
        for line in file:
            log_sql_pattern = 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    extract_querys_from_logs(args.log_file)
