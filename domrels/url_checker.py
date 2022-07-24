import asyncio


async def find_ip_by_url(url: str):
    """Try to get IP information by given URL"""
    try:
        loop = asyncio.get_event_loop()
        result = await loop.getaddrinfo(url, 80)
        if result:
            ip_address = result[0][-1][0]
            show_info(url, ip_address)
    except Exception:
        pass


def show_info(url, ip_address):
    print(f"{url:>30} - {ip_address:<15}")
