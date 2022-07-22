import sys
import asyncio
import ipaddress
from typing import List

from utils import parse_args
from scanner import check_network


async def main() -> None:
    ip, ports = parse_args(sys.argv)
    await check_network(ip, ports)

if __name__ == '__main__':
    asyncio.run(main())