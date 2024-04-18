#!/usr/bin/python3

import argparse
import configparser
import os

from tools import VERSIONS, get_odoo_config_file_path, get_venv_config_file_path, get_repo_directory


# -- can be modified -- #

ALIAS_FILE = ".alias"
ALIAS_IGNORE = [
    "set_up.py",
    "tools.py",
]

# --------------------- #


def version_to_arg(version):
    arg_name = "--" + version
    help = f"python path for {version = }"
    return (arg_name, ), {"help": help}

ARGUMENTS = {
    ("--odoo-bin-path", ): {
        "help": "path to odoo-bin",
    },
    ("--addons-path", ): {
        "help": "comma separated pathes to the odoo addons",
    },
    ("--versionned-addons-path", ): {
        "help": "comma separated pathes to the versionned odoo addons",
    },
    ("--upgrade-path", ): {
        "help": "comma seperated pathes to the upgrade repos",
    },
    ("--data-dir", ): {
        "help": "parent directory of the filestore directory",
    },
    ("--create-alias", ): {
        "action": "store_true",
        "help": f"create the {ALIAS_FILE} file, containing aliases for the different commands",
    },
}
VENV_ARGUMENTS = {version_to_arg(version)[0]:version_to_arg(version)[1] for version in VERSIONS}
ARGUMENTS.update(VENV_ARGUMENTS)


def add_to_config_file(config_file_path, section, option, value):
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if section not in config:
        config.add_section(section)
    config.set(section, option, value)
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def add_to_venv_config(version, venv_path):
    add_to_config_file(get_venv_config_file_path(), version, 'python_path', venv_path)

def add_to_odoo_config(option, value):
    add_to_config_file(get_odoo_config_file_path(), 'options', option, value)

def arg_to_version(arg):
    return arg.replace("_", "-")

def get_program_alias_name(program_path):
    filename = os.path.basename(program_path)
    filename_without_extension = os.path.splitext(filename)[0]
    return filename_without_extension.replace("_", "-")

def get_program_alias_command(program_path):
    program_name = get_program_alias_name(program_path)
    return f'alias {program_name}="python3 {program_path}"\n'

def get_programs():
    file_names = os.listdir(get_repo_directory())

    programs = []
    for file_name in file_names:
        if not file_name.startswith('.') and file_name not in ALIAS_IGNORE:
            file_path = os.path.join(get_repo_directory(), file_name)
            if os.path.isfile(file_path):
                programs.append(file_path)
    return programs

def create_alias_file():
    alias_file_path = os.path.join(get_repo_directory(), ALIAS_FILE)
    content = ""
    for program_path in get_programs():
        content += get_program_alias_command(program_path)
    with open(alias_file_path, "w") as alias_file:
        alias_file.write(content)
        bashrc_command = f"source {alias_file_path}"
        print(f"{ALIAS_FILE} file created.  Add `{bashrc_command}` in your ~/.bashrc file to have them available in your future sessions.")

def set_up(option, value):
    if value:
        if arg_to_version(option) in VERSIONS:
            add_to_venv_config(arg_to_version(option), value)
        elif option == "create_alias":
            create_alias_file()
        else:
            add_to_odoo_config(option, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args = parser.parse_args()
    for option, value in args._get_kwargs():
        set_up(option, value)
