import sys
import asyncio

import time

from utils import parse_args
from domain_generator import generate_urls
from url_checker import find_ip_by_url


async def main():
    start = time.time()
    keywords = parse_args(args=sys.argv)
    urls = await generate_urls(keywords=keywords)
    tasks = [find_ip_by_url(url) for url in urls]
    await asyncio.gather(*tasks)

    print(f"Total time: {time.time() - start}ms")

if __name__ == '__main__':
    asyncio.run(main())
