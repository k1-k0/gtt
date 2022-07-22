import asyncio
import ipaddress
from typing import List
from collections import namedtuple

import aiohttp


OPEN_STATUS     = "OPENED"
CLOSED_STATUS   = "CLOSED"
DEFAULT_TIMEOUT = 5
HTTP_PORT       = 80
HTTPS_PORT      = 443

PortStatus = namedtuple('PortStatus', ['host', 'port', 'status', 'server'])


async def check_network(ip: ipaddress.IPv4Network, ports: List[int]) -> None:
    """Checks network for open ports"""
    tasks = [get_port_statuses(str(host), ports) for host in ip.hosts()]
    await asyncio.gather(*tasks)


async def get_port_statuses(host: str, ports: List[int]) -> None:
    """Checks and output open ports for the specified host"""
    check_task = [try_connect(host, port) for port in ports]
    results = await asyncio.gather(*check_task)

    for result in results:
        if result.status == OPEN_STATUS:
            show_info(result)


def show_info(port_status: PortStatus) -> None:
    """Prints information about open ports and server"""
    fields = [port_status.host, port_status.port, port_status.status]
    if server := port_status.server:
        fields.append(server)
    print(*fields, sep='\t')


async def try_connect(host: str, port: int) -> PortStatus:
    """Try to connect to specified host:port.
        If connection if successful then the port is open, otherwise - closed"""
    status = CLOSED_STATUS
    server = None
    try:
        await asyncio.wait_for(asyncio.open_connection(host, port),
                               timeout=DEFAULT_TIMEOUT)
        status = OPEN_STATUS

        if port in (HTTP_PORT, HTTPS_PORT):
            server = await check_server_app(to_url(host, port))
    except:
        pass

    return PortStatus(host, port, status, server)


async def check_server_app(host: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(host) as response:
            return response.headers["Server"]


def to_url(host: str, port: int) -> str:
    protocol = "https" if port == HTTPS_PORT else "http"
    return f'{protocol}://{host}:{port}/'