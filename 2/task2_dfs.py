import requests
from bs4 import BeautifulSoup
import re
import time


def dfs(soup, keyword):
    urlsList = []
    for content in soup.findAll('div', {'class': 'mw-body-content'}):
        for links in content.findAll('a', href=re.compile('/wiki/')):
            part_href = links.get('href')
            part_text = links.text
            if ':' in part_href:
                continue
            if '#' in part_href:
                pos = part_href.index('#')
                part_href = part_href[0 : pos]
            if re.findall(keyword, part_text, re.IGNORECASE) or re.findall(keyword, part_href, re.IGNORECASE):
                href = 'https://en.wikipedia.org' + part_href
                urlsList.append(href)
    return urlsList


def crawler_init(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup


def crawl_wiki(seed, keyword, depth):
    if depth > 5:
        return
    soup = crawler_init(seed)
    urls = dfs(soup, keyword)
    time.sleep(2)
    for url in urls:
        if len(dfs_result) == 1000:
            return
        if url not in dfs_result:
            dfs_result.append(url)
        crawl_wiki(url, keyword, depth + 1)
    return

dfs_result=['https://en.wikipedia.org/wiki/Sustainable_energy']
crawl_wiki('https://en.wikipedia.org/wiki/Sustainable_energy', 'solar', 2)


#output
for href in dfs_result:
    fob = open('task2_dfs.txt', 'a')
    fob.write(href[1] + '\n')
    fob.close()

print(dfs_result)