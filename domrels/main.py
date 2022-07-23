import sys
import asyncio

import time

from utils import parse_args
from domain_generator import generate_urls
from url_checker import find_ip_by_url


async def main():
    keywords = parse_args(args=sys.argv)
    urls = await generate_urls(keywords=keywords)
    tasks = [find_ip_by_url(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
