import asyncio
from typing import List
from collections import namedtuple


OPEN_STATUS     = "OPENED"
CLOSED_STATUS   = "CLOSED"
DEFAULT_TIMEOUT = 5

PortStatus = namedtuple('PortStatus', ['host', 'port', 'status'])


async def try_connect(host: str, port: int):
    """Try to connect to specified host:port.
        If connection if successful then the port is open, otherwise - closed"""
    status = CLOSED_STATUS
    try:
        await asyncio.wait_for(asyncio.open_connection(host, port),
                               timeout=DEFAULT_TIMEOUT)
        status = OPEN_STATUS
    except:
        pass

    return PortStatus(host, port, status)

async def check_port(host: str, ports: List[int]):
    """Asynchronous checking for open ports"""
    check_task = [try_connect(host, port) for port in ports]
    results = await asyncio.gather(*check_task)

    for result in results:
        if result.status == OPEN_STATUS:
            print(result.host, result.port, result.status, sep="\t")