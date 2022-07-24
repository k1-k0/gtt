import asyncio
import string
from typing import List


DOMAIN_ZONES = (
    'com', 'ru',   'net',
    'org', 'info', 'cn',
    'es',  'top',  'au',
    'pl',  'it',   'uk',
    'tk',  'ml',   'ga',
    'cf',  'us',   'xyz',
    'top', 'site', 'win',
    'bid',
)

# NOTE: Just for speed and example used own homoglyphs dict,
# instead of external lib
HOMOGLYPHS = {
    'o': ('0', 'q', 'c'),
    'O': ('0', 'o', 'q', 'c',),
    '0': ('O', 'o', 'q', 'c',),
    'c': ('o', 'q', 'c'),
    'i': ('1', 'l', 'j'),
    '1': ('l', 'l', 'i'),
    'l': ('i', 'l', '1'),
    'w': ('v', 'vv'),
    'd': ('cl', 'ci', 'b'),
    'b': ('d'),
    'm': ('rn', 'n', 'w', 'ni'),
    'n': ('rn', 'm'),
    '-': ('_'),
}


class Strategy:
    """Class describes various strategies for generating phishing URLs"""
    alphabet = string.digits + string.ascii_lowercase

    @staticmethod
    def add_symbol_to_end(keyword: str):
        """Generates new keywords by appending one new symbol to the end"""
        result = []
        for symbol in Strategy.alphabet:
            result.append(''.join((keyword, symbol)))
        return result

    @staticmethod
    def replace_by_homoglyph(keyword: str):
        """Generates new keywords by replace symbol on to their homoglyphs"""
        result = []
        for i, symbol in enumerate(keyword):
            if symbol in HOMOGLYPHS:
                for homoglyph in HOMOGLYPHS[symbol]:
                    new_keyword = ''.join((keyword[:i],
                                           homoglyph,
                                           keyword[i+1:]))
                    result.append(new_keyword)
        return result

    @staticmethod
    def define_domain(keyword: str):
        """Generates new keywords by adding a domain"""
        result = []
        for i in range(1, len(keyword)):
            if keyword[i].isalnum() and keyword[i-1].isalnum():
                new_keyword = ''.join((keyword[:i], '.', keyword[i:]))
                result.append(new_keyword)
        return result

    @staticmethod
    def remove_symbol(keyword: str):
        """Generates new keywords by removing one symbol"""
        result = []
        for i in range(1, len(keyword)+1):
            result.append(''.join((keyword[:i-1], keyword[i:])))
        return result


async def generate_urls(keywords: List[str]):
    """Returns list of unique bad urls generated from given keywords"""
    tasks = [generate_new_keywords(keyword) for keyword in keywords]
    results = await asyncio.gather(*tasks)

    new_keywords = []
    for result in results:
        new_keywords.extend(result)

    tasks = [append_domain_zone(keyword) for keyword in new_keywords]
    results = await asyncio.gather(*tasks)

    urls = set()
    for result in results:
        for item in result:
            urls.add(item)

    return list(urls)


async def generate_new_keywords(keyword: str):
    """Returns list of phishing urls generated with different strategies"""
    keywords = []

    keywords.extend(Strategy.add_symbol_to_end(keyword))
    keywords.extend(Strategy.replace_by_homoglyph(keyword))
    keywords.extend(Strategy.define_domain(keyword))
    keywords.extend(Strategy.remove_symbol(keyword))

    return keywords


async def append_domain_zone(keyword: str):
    """Returns list of keywords with appended domain zones"""
    urls = set()

    for domain_zone in DOMAIN_ZONES:
        url = ''.join((keyword, '.', domain_zone))
        urls.add(url)

    return urls
