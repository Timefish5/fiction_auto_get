import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from ua_info import ua_list
import random

def getNextChapter_url(url):
    agent = random.choice(ua_list)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        next_chapter_url_a = soup.find('a', id = "next_url")
        if next_chapter_url_a:
            if next_chapter_url_a.text == "没有了 ":
                return None
            next_chapter_url = next_chapter_url_a['href']
            full_next_chapter_url = urljoin(url, next_chapter_url)
            return full_next_chapter_url

def getCurrentChapter_information(url):
    agent = random.choice(ua_list)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        title_name = soup.find('h1', class_ = "title")
        if title_name:
            title_content = title_name.text
            return title_content
        else:
            print("获取标题失败")
            return None

def getFirstChapter(url):
    agent = random.choice(ua_list)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    }
    response = requests.get(url, headers=headers)

    information  = {
        "book_name": None,
        "author": None,
        "first_chapter_url": None,
    }
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        first_chapter = soup.find('a', href = True, text = re.compile("第1章"))
        if first_chapter != None:
            first_chapter_url = first_chapter['href']
            full_first_chapter_url = urljoin(url, first_chapter_url)
            information["first_chapter_url"]  = full_first_chapter_url
        else:
            first_chapter = soup.find('a', href=True, text=re.compile("第一章"))
            first_chapter_url = first_chapter['href']
            full_first_chapter_url = urljoin(url, first_chapter_url)
            information["first_chapter_url"]  = full_first_chapter_url
        # find book name and author
        book_name = soup.find('meta', property = "og:novel:book_name").get('content')
        information["book_name"] = book_name
        author = soup.find('meta', property = "og:novel:author").get('content')
        information["author"] = author
    return information

if __name__ == '__main__':
    getCurrentChapter_information('https://www.xbiqugu.com/wapbook/76778/38086730.html')