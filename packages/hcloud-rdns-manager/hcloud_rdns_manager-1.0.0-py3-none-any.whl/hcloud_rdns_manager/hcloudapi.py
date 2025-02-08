"""
The hcloud-rdns-manager - the smart way to manage your rDNS records in the Hetzner cloud.

    Dev: wh0ami
Licence: Public Domain <https://unlicense.org>
Project: https://codeberg.org/wh0ami/hcloud-rdns-manager
"""

import hcloud.servers.client
from hcloud import Client


class HcloudApi:
    """Wrapper around of the Hetzner Cloud library."""

    def __init__(self, token: str) -> None:
        """
        Initialize api connection in ctor and store it as a private attribute.

        :param token: The API token to authenticate at the Hetzner Cloud API.
        """
        self.__client = Client(token=token)

    def get_all_hcloud_server_ids(self, server_list: list | None = None, cast_to_string: bool = True) -> list:
        """
        Get a list of all server ids from the api.

        :param server_list: Restrict action to this list of servers.
        :param cast_to_string: Whether the method should be explicitly cast the server IDs to strings.
        :return: List of server IDs.
        """
        if server_list is None:
            server_list = []
        id_list = []
        for server in self.__client.servers.get_all():
            server_id = str(server.id) if cast_to_string else server.id
            id_list.append(server_id) if len(server_list) == 0 or server_id in server_list else None
        return id_list

    def get_hcloud_server_ptrs(self, server_id: str) -> dict:
        """
        Fetch a dict with all ptr records of a server, which will be identified by its id.

        :param server_id: ID of the server, of which the PTRs should be returned.
        :return: Dict with PTRs.
        """
        server = self.__client.servers.get_by_id(id=server_id)
        ptrs = {server.public_net.ipv4.ip: server.public_net.ipv4.dns_ptr}
        for ptr in server.public_net.ipv6.dns_ptr:
            ptrs[ptr["ip"]] = ptr["dns_ptr"]
        return ptrs

    def set_hcloud_server_ptr(self, server_id: str, ip: str, ptr: str) -> hcloud.servers.client.BoundAction:
        """
        Update the ptr of a server.

        :param server_id: ID of the server, of which the PTR should be set.
        :param ip: IP address, for which the PTR should be created.
        :param ptr: The actual PTR (DNS name).
        :return: BoundAction from the hcloud library.
        """
        return self.__client.servers.get_by_id(id=server_id).change_dns_ptr(ip=ip, dns_ptr=ptr)

    def get_hcloud_server_nickname_by_id(self, server_id: str) -> str:
        """
        Fetch the custom nickname of a server from the api.

        :param server_id: IF of the server, of which the nickname should be returned.
        :return: The nickname of the server.
        """
        return self.__client.servers.get_by_id(id=server_id).name
