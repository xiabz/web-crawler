import requests
from bs4 import BeautifulSoup
import re
import time


result1 = []
result2 = []
visited1 = set()
visited2 = set()

def crawl_wiki(seed, result, visited):
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
            get_urls(soup, depth, result, visited)
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

def get_urls(soup, depth, result, visited):
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


crawl_wiki('https://en.wikipedia.org/wiki/Sustainable_energy', result1, visited1)
crawl_wiki('https://en.wikipedia.org/wiki/Solar_power', result2, visited2)


i = 0
j = 0
num = 0
merge = []
# merge_set = set()
while num < 1000:
    if result1[i][0] < result2[j][0]:
        # if result1[i][1] in merge_set:
        #     continue
        merge.append(result1[i][1])
        # merge_set.add(result1[i][1])
        i += 1
        num += 1
    elif result2[j][0] < result1[i][0]:
        # if result2[j][1] in merge_set:
        #     continue
        merge.append(result2[j][1])
        # merge_set.add(result2[j][1])
        j += 1
        num += 1
    else:
        # if result1[i][1] in merge_set:
        #     continue
        merge.append(result1[i][1])
        # merge_set.add(result1[i][1])
        i += 1
        num += 1
        if num == 1000:
            break
        # if result2[j][1] in merge_set:
        #     continue
        merge.append(result2[j][1])
        # merge_set.add(result2[j][1])
        j += 1
        num += 1





for href in merge:
    fob = open('task3_mergeList.txt', 'a')
    fob.write(href + '\n')
    fob.close()




print(len(merge))
print(merge)


