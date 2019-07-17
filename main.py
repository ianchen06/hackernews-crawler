import re
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

import requests as r
from bs4 import BeautifulSoup

HACKERNEWS_HOST = 'http://news.ycombinator.com'
HACKERNEWS_URL = 'newest'
NO_PAGE = 10

def get_page(url):
    resp = r.get(url, headers={'user-agent': "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"})
    if 'text' in resp.headers.get('Content-Type'):
        return resp.text
    else:
        return ''

def parse_stories(page):
    return re.findall('<a href="(.+?)" class="storylink" rel="nofollow">.+?</a>', page)

more_link = HACKERNEWS_URL

for x in range(NO_PAGE):
    resp = get_page("%s/%s"%(HACKERNEWS_HOST, more_link))
    links = parse_stories(resp)
    for link in links:
        soup = BeautifulSoup(get_page(link), 'lxml')
        [x.extract() for x in soup.select('script')]
        content = soup.get_text()
        print(content)
    more_link = re.findall('<a href="(.+?)" class="morelink" rel="next">More</a>', resp.text)[0]
