"""
The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.

    Dev: wh0ami
Licence: Public Domain <https://unlicense.org>
Project: https://codeberg.org/wh0ami/hcloud-rdns-manager
"""

import argparse
import sys
from argparse import RawTextHelpFormatter
from pathlib import Path

import yaml
from loguru import logger

from hcloud_rdns_manager.deployment import deploy_changes
from hcloud_rdns_manager.export import generate_dump
from hcloud_rdns_manager.validation import validate_config


def main() -> None:
    """argparser, config loading, etc."""
    # read cli parameters
    parser = argparse.ArgumentParser(
        description="The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit, that the changes should really be deployed. (only deploy action)",
    )
    parser.add_argument(
        "--servers",
        metavar="server-id",
        type=str,
        action="append",
        default=[],
        help="Only affect these server id(s). Can be given multiple times. By default, all servers are affected.",
    )
    parser.add_argument(
        "--projects",
        metavar="project-name",
        type=str,
        action="append",
        default=[],
        help="Only affect these projects. The project name passed here is NOT the name from the Web "
        "UI, it is the name that you defined in your local rdns zone file. Can be given multiple "
        "times. By default, all projects are affected.",
    )
    parser.add_argument(
        "action",
        type=str,
        metavar="action",
        choices=["check", "deploy", "dump"],
        help="Valid actions are:\n"
        "check\t- read the rdns zone file and validate it (--servers and --projects will be "
        "ignored, if passed)\n"
        "deploy\t- deploy the rdns entries from the rdns zone file in the Hetzner cloud, "
        "if --commit was passed. Otherwise, it will only perform a dry-run and display the "
        "changes.\n"
        "dump\t- obtain and dump the current config from the Hetzner cloud\n\n",
    )
    parser.add_argument("rdns_zone_file", type=str, help="rDNS zone file that should be processed")
    args = parser.parse_args(sys.argv[1:])

    # open and read config
    try:
        with Path(args.rdns_zone_file).open() as f:
            config = yaml.safe_load(f)
    except OSError:
        logger.error("Config not found or unreadable! Aborting...")
        sys.exit(1)
    except yaml.YAMLError:
        logger.error("Config contains invalid yaml! Aborting...")
        sys.exit(1)

    # validate the configuration (independent of action that should be executed)
    if validate_config(config):
        # check/execute the passed action
        if args.action == "deploy":
            deploy_changes(config=config, project_names=args.projects, server_ids=args.servers, commit=args.commit)
        elif args.action == "dump":
            generate_dump(config, project_names=args.projects, server_ids=args.servers)
        elif args.action == "check":
            pass
        else:
            logger.error("Invalid action!")
            sys.exit(1)
        sys.exit(0)
    else:
        sys.exit(1)
