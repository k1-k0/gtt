import sys
import asyncio
import ipaddress
from typing import List

from utils import parse_args
from port_scan import check_port

async def check_ip_address(ip: ipaddress.IPv4Network, ports: List[int]):
    tasks = [check_port(str(host), ports) for host in ip.hosts()]
    await asyncio.gather(*tasks)

async def main():
    ip_range, ports = parse_args(sys.argv)
    await check_ip_address(ip_range, ports)

if __name__ == '__main__':
    asyncio.run(main())