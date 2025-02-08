"""
The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.

    Dev: wh0ami
Licence: Public Domain <https://unlicense.org>
Project: https://codeberg.org/wh0ami/hcloud-rdns-manager
"""

from loguru import logger
from tabulate import tabulate

from hcloud_rdns_manager.hcloudapi import HcloudApi


def deploy_changes(config: dict, project_names: list, server_ids: list, commit: bool = False) -> None:  # noqa: C901
    """
    Deploy a passed configuration to the Hetzner Cloud.

    :param config: The configuration to use.
    :param project_names: Restrict the action to the passed list of project names.
    :param server_ids: Restrict the action to the passed list of server IDs.
    :param commit: Whether the changes should be deployed or just showed.
    """
    # iterate over all projects
    for project in config["hcloud"]["projects"]:
        # check whether project should be updated
        if len(project_names) == 0 or project in project_names:
            # fetch project config
            project_config = config["hcloud"]["projects"][project]

            # initialize api client
            api = HcloudApi(project_config["token"])

            # fetch current list of server ids (--servers will be applied by passing servers parameter)
            id_list = api.get_all_hcloud_server_ids(server_list=server_ids)

            # iterate over all servers that were fetched above
            for server in id_list:
                # just take those servers, which are defined in rdns zone config
                if server in project_config["servers"]:
                    # fetch current rdns configuration from hcloud
                    current_rdns = api.get_hcloud_server_ptrs(server_id=server)

                    # initialize empty changeset
                    changeset = []

                    # iterate over all entries, that should exist (as defined in config)
                    for ip in project_config["servers"][server]["rdns"]:
                        # ptr that doesn't exist in the current_rdns list needs to be created
                        if ip not in current_rdns:
                            changeset.append(["CREATE", ip, None, project_config["servers"][server]["rdns"][ip]])
                        # ptr that exist (logical result of the condition above) but do not have the same value needs to
                        # be updated
                        elif current_rdns[ip] != project_config["servers"][server]["rdns"][ip]:
                            changeset.append(
                                ["UPDATE", ip, current_rdns[ip], project_config["servers"][server]["rdns"][ip]],
                            )

                    # iterate over all entries, that currently exist
                    changeset.extend(
                        ["DELETE", ip, current_rdns[ip], None]
                        for ip in current_rdns
                        if ip not in project_config["servers"][server]["rdns"]
                    )

                    # print changeset as table
                    logger.info(
                        f"--> Server {server} ({api.get_hcloud_server_nickname_by_id(server_id=server)}) "
                        f"from project {project}",
                    )
                    if len(changeset) > 0:
                        logger.info(
                            "Changeset:\n"
                            + tabulate(changeset, headers=["Action", "IP", "Current PTR", "New PTR"], tablefmt="psql"),
                        )
                        if commit:
                            logger.info("Applying changeset...")
                            for change in changeset:
                                api.set_hcloud_server_ptr(server_id=server, ip=change[1], ptr=change[3])
                            logger.info("Changes applied!")
                    else:
                        logger.warning("Nothing to do!")
