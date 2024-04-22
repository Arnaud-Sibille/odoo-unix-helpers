import configparser
import os
import subprocess
import psycopg2
import re


# -- can be modified -- #

ODOO_CONFIG_FILE = ".odoo_conf"
VENV_CONFIG_FILE = ".venv_conf"

DEFAULT_PYTHON_PATH = "/usr/bin/python3"

MASTER_VERSION = "17.3"

VERSIONS = [
    "master",
    "saas-17.2",
    "saas-17.1",
    "17.0",
    "saas-16.4",
    "saas-16.3",
    "saas-16.2",
    "saas-16.1",
    "16.0",
    "saas-15.4",
    "saas-15.3",
    "saas-15.2",
    "saas-15.1",
    "15.0",
    "14.0",
]

# --------------------- #


def get_odoorc_path():
    home_directory = os.path.expanduser("~")
    odoorc_path = os.path.join(home_directory, ".odoorc")
    if os.path.exists(odoorc_path):
        return odoorc_path
    return None

def get_repo_directory():
    # Works because this function is in a file one level below the repo directory.
    file_directory = os.path.abspath(__file__)
    return os.path.dirname(file_directory)

def get_odoo_config_file_path():
    repo_directory = get_repo_directory()
    config_file_path = os.path.join(repo_directory, ODOO_CONFIG_FILE)
    return config_file_path

def get_venv_config_file_path():
    repo_directory = get_repo_directory()
    venv_file_path = os.path.join(repo_directory, VENV_CONFIG_FILE)
    return venv_file_path

def get_value_from_odoo_config(option):
    def try_find_option(file_path):
        if os.path.exists(file_path):
            config = configparser.ConfigParser()
            config.read(file_path)
            try:
                return config.get("options", option)
            except configparser.NoOptionError:
                return None

    odoorc_path = get_odoorc_path()
    config_file_path = get_odoo_config_file_path()
    value = try_find_option(config_file_path) or try_find_option(odoorc_path)
    if not value:
        raise Exception(f"Could not find '{option}' in [options] section neither at {config_file_path} or {odoorc_path}.")
    return value

def get_odoo_repo_path():
    odoo_bin_path = get_value_from_odoo_config("odoo_bin_path")
    return os.path.dirname(odoo_bin_path)

def get_addons_path():
    addons_path = set(get_value_from_odoo_config("addons_path").split(','))
    base_addon_path = os.path.join(get_odoo_repo_path(), 'odoo/addons')
    addons_path.add(base_addon_path)
    return addons_path

def execute_command(command, get_output=False, input_str=None):
    result = subprocess.run(command, input=input_str.encode() if input_str else None, capture_output=get_output)
    if result.returncode:
        raise Exception(f"Command {command} failed.")
    return result.stdout

def launch_odoo(db, shell=False, extra_args=[], input_code=None, python_path=DEFAULT_PYTHON_PATH):
    odoo_bin_path = get_value_from_odoo_config("odoo_bin_path")
    odoo_command = [
        python_path,
        odoo_bin_path,
    ]
    shell_arguments = [
        "shell",
        "--log-handler",
        ":CRITICAL",
    ] if (shell or input_code) else []
    arguments = [
        "-d",
        db,
        "--config",
        get_odoo_config_file_path(),
    ]
    execute_command(odoo_command + shell_arguments + arguments + extra_args, input_str=input_code)

def get_python_path(version):
    venv_file_path = get_venv_config_file_path()
    if os.path.exists(venv_file_path):
        config = configparser.ConfigParser()
        config.read(venv_file_path)
        try:
            return config.get(version, "python_path")
        except (configparser.NoSectionError, configparser.NoOptionError):
            print(f"No specific python path found in {venv_file_path} for {version}")
    return DEFAULT_PYTHON_PATH

def extract_version(raw_version, saas_prefix=False):
    if re.match(r'^master(-|$)', raw_version):
        return "master"
    if not saas_prefix and re.match(r'^saas(~|-)', raw_version):
        return extract_version(raw_version[5:], saas_prefix=True)
    version_match = re.match(r'\d+\.\d', raw_version)
    if not version_match:
        raise Exception(f"Unable to use database version {raw_version}.")

    version = version_match.group(0)
    if version == MASTER_VERSION:
        return "master"
    return version if not saas_prefix else 'saas-' + version

def extract_version_from_db(db):
    base_version_query = """
        SELECT latest_version
        FROM ir_module_module
        WHERE name = 'base'
        LIMIT 1
    """
    with psycopg2.connect(database=db) as conn:
        with conn.cursor() as cr:
            cr.execute(base_version_query)
            res = cr.fetchall()
    return extract_version(res[0][0])

def pull_repo(repo_path):
    pull_command = [
        "git",
        "-C",
        repo_path,
        "pull",
    ]
    execute_command(pull_command)

def get_repo_current_branch(repo_path):
    get_branch_command = [
        "git",
        "-C",
        repo_path,
        "rev-parse",
        "--abbrev-ref",
        "HEAD",
    ]
    output = execute_command(get_branch_command, get_output=True)
    return output.decode('utf-8').strip()

def extract_version_from_branch(repo_path):
    branch_name = get_repo_current_branch(repo_path)
    return extract_version(branch_name)

def get_odoo_repo_version():
    odoo_dir = os.path.dirname(get_value_from_odoo_config("odoo_bin_path"))
    return extract_version_from_branch(odoo_dir)

def get_filestore_dir():
    data_path = get_value_from_odoo_config("data_dir")
    filestore_path =  os.path.join(data_path, "filestore")
    if not os.path.exists(filestore_path):
        raise Exception(f"Could not find the filestore {filestore_path}")
    return filestore_path

def get_filestore_path(db):
    filestore_dir = get_filestore_dir()
    filestore_path = os.path.join(filestore_dir, db)
    if os.path.exists(filestore_path):
        return filestore_path
    return None
