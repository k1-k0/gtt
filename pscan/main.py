import sys
import asyncio

from utils import parse_args
from scanner import check_network


async def main() -> None:
    ip_address, ports = parse_args(sys.argv)
    await check_network(ip_address, ports)

if __name__ == '__main__':
    asyncio.run(main())
