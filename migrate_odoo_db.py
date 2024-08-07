#!/usr/bin/python3

import argparse

from tools import VERSIONS, extract_version_from_db, get_value_from_odoo_config, pull_repo
from drop_odoo_dbs import drop_odoo_db
from duplicate_odoo_db import duplicate_odoo_db
from switch_odoo_branches import switch_odoo_branches
from launch_odoo_db import launch_odoo_db


ARGUMENTS = {
    ("db", ): {
        "help": "name of the database",
    },
    ("target_version", ): {
        "help": "version to migrate to",
    },
    ("-p", "--pull") : {
        "action": "store_true",
        "help": "pull the branch after switching",
    },
    ("--pull-upgrade", ): {
        "action": "store_true",
        "help": "pull the upgrade repos",
    },
}


def get_intermediate_versions(source_version, target_version):
    if source_version not in VERSIONS:
        raise Exception(f"Unknown database version {source_version}")
    if target_version not in VERSIONS:
        raise Exception(f"Don't recognize {target_version = }")
    source_version_index = VERSIONS.index(source_version)
    target_version_index = VERSIONS.index(target_version)
    if target_version_index >= source_version_index:
        raise Exception(f"{target_version = } should be greater than database version = {source_version}")
    return VERSIONS[target_version_index : source_version_index][::-1]

def migrate(db, version, pull=False, extra_args=None):
    upgrade_path = get_value_from_odoo_config("upgrade_path")
    migrate_args = [
        '-u',
        'all',
        f'--upgrade-path={upgrade_path}',
        '--stop-after-init',
    ]
    extra_args = extra_args if extra_args else []
    switch_odoo_branches(version, pull=pull)
    launch_odoo_db(db, extra_args=extra_args + migrate_args, switch=False)

def pull_upgrade_repos():
    upgrade_repos_pathes = get_value_from_odoo_config("upgrade_path")
    for upgrade_repo_path in upgrade_repos_pathes.split(','):
        pull_repo(upgrade_repo_path)

def migrate_odoo_db(db, target_version, pull=False, pull_upgrade=False, extra_args=None):
    new_db = db + f"_to_{target_version}"
    drop_odoo_db(new_db)
    duplicate_odoo_db(db, new_db)

    if pull_upgrade:
        pull_upgrade_repos()

    db_version = extract_version_from_db(db)
    versions_to_migrate = get_intermediate_versions(db_version, target_version)
    for version in versions_to_migrate:
        migrate(new_db, version, pull=pull, extra_args=extra_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for key, value in ARGUMENTS.items():
        parser.add_argument(*key, **value)
    args, extra_args = parser.parse_known_args()
    migrate_odoo_db(args.db, args.target_version, pull=args.pull, pull_upgrade=args.pull_upgrade, extra_args=extra_args)
