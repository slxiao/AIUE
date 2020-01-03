#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import random

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HOME = "https://slxiao.github.io"

def create_browser(webdriver_path):
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    return webdriver.Chrome(webdriver_path, chrome_options=browser_options)


def get_hyperlinks(browser, url):
    if url.startswith("/"):
        url = HOME + url
    browser.get(url)
    html = bs(browser.page_source, "lxml")

    links = []
    for item in html.find_all("a"):
        if "href" in item.attrs and any([item.attrs["href"].startswith(i) for i in ["/", "home"]]):
            links.append(item.attrs["href"])
    if "/2018/01/01/demo/" in links:
        links.remove("/2018/01/01/demo/")
    return links

def main():
    browser = create_browser('/usr/bin/chromedriver')

    click_number = 0
    unique_links = []
    points = [(click_number, len(unique_links))]
    links = get_hyperlinks(browser, HOME)
    
    while click_number < 1000:
        if click_number > 0 and not click_number % 100:
            links = get_hyperlinks(browser, HOME)
        
        if links:
            link = random.choice(links)
            links = get_hyperlinks(browser, link)

            click_number += 1
            if link not in unique_links:
                unique_links.append(link)
            points.append((click_number, len(unique_links)))
            print(click_number, len(unique_links))
        else:
            print("sub links of %s are empty, exit from loop" % link)
            break
    
    return points

if __name__ == "__main__":
    result = []
    for i in range(10):
        result.append((i, main()))
    
    with open("data.txt", "wb") as f:
        f.write(str(result))
