"""
The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.

    Dev: wh0ami
Licence: Public Domain <https://unlicense.org>
Project: https://codeberg.org/wh0ami/hcloud-rdns-manager
"""

from datetime import UTC, datetime
from pathlib import Path

import yaml
from loguru import logger

from hcloud_rdns_manager.hcloudapi import HcloudApi
from hcloud_rdns_manager.validation import validate_config


def generate_dump(config: dict, project_names: list[str], server_ids: list[str]) -> bool:
    """
    Generate a dump of a currently provisioned configuration in the Hetzner Cloud.

    :param config: Configuration to use.
    :param project_names: Restrict action to the passed list of projects names.
    :param server_ids: Restrict action to the passed list of server IDs.
    :return: Whether the dump generation was successful or not.
    """
    # generate dump
    logger.info("Creating project dump...")

    # initialize empty export dump
    dump = {
        "hcloud": {
            "projects": {},
        },
    }

    # iterate over all projects
    for project in config["hcloud"]["projects"]:
        # check whether project should be dumped
        if len(project_names) == 0 or project in project_names:
            # fetch project config
            project_config = config["hcloud"]["projects"][project]

            # initialize api client
            api = HcloudApi(project_config["token"])

            # initialize project dump
            project_dump = {
                "token": str(project_config["token"]),
                "servers": {},
            }

            # iterate over list of servers, that should be dumped, dump then and append the dump to the project dump
            # filter from --servers is passed by serverList parameter
            for server in api.get_all_hcloud_server_ids(server_list=server_ids):
                project_dump["servers"][server] = {}
                project_dump["servers"][server]["rdns"] = api.get_hcloud_server_ptrs(server_id=server)

            # append project dump to export dump
            dump["hcloud"]["projects"][project] = project_dump

    logger.info("Dump created!")

    # validate generated dump
    valid = validate_config(config=dump)

    # write project dump into file, if its valid
    if valid:
        # generate name of dump file
        dumpfile = "hcloud_rdns_dump_" + datetime.now(tz=UTC).strftime("%Y-%m-%d_%H-%M-%S") + ".yml"

        # try to write dump as yaml into the dump file defined above
        logger.info(f"Writing dump to {dumpfile}...")
        try:
            with Path(dumpfile).open("w") as f:
                yaml.dump(dump, f)
        except OSError as ioe:
            logger.error(
                f"Could not write dump! Maybe your current working directory is not writeable? Aborting... [{ioe}]",
            )
            return False
        except yaml.YAMLError as exc:
            logger.error(f"Dump contains invalid yaml! Aborting... [{exc}]")
            return False

        # only on success
        logger.info(f"Dump written to {dumpfile} !")
        return True

    return False
