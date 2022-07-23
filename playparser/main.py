import asyncio
import sys

from utils import parse_args
from page_parser import (
    get_application_links, parse_application_page,
    validate_applications, convert_applications_info_to_json)



async def main():
    keyword = parse_args(sys.argv)
    app_links = get_application_links(name=keyword)

    tasks = [parse_application_page(link) for link in app_links]
    apps_info = await asyncio.gather(*tasks)

    apps_info = validate_applications(apps_info=apps_info, keyword=keyword)

    result = convert_applications_info_to_json(apps_info=apps_info)
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
