import requests
from bs4 import BeautifulSoup
import re
import time


result = []
visited = set()

def crawl_wiki(seed):
    depth = 1
    result.append([depth, seed])
    visited.add(seed)
    depth += 1
    position = 0
    while depth <= 5:
        count = len(result)
        while position < count:
            url = result[position][1]
            soup = crawler_init(url)
            get_urls(soup,depth)
            if len(result) == 1000:
                break
            position += 1
            time.sleep(1)
        if len(result) == 1000:
            break
        depth += 1


def crawler_init(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    return soup

def get_urls(soup, depth):
    for content in soup.findAll('div', {'class': 'mw-body-content'}):
        for links in content.findAll('a', href=re.compile('/wiki/')):
            part_href = links.get('href')
            if ':' in part_href:
                continue
            if '#' in part_href:
                pos = part_href.index('#')
                part_href = part_href[0 : pos]
            href = 'https://en.wikipedia.org' + part_href
            if href in visited:
                continue
            temp = [depth, href]
            result.append(temp)
            visited.add(href)
            if len(result) == 1000:
                break


crawl_wiki('https://en.wikipedia.org/wiki/Sustainable_energy')
print(result)



for href in result:
    fob = open('task1.txt', 'a')
    fob.write(href[1] + '\n')
    fob.close()




