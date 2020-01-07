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
    browser.get(url)
    html = bs(browser.page_source, "lxml")

    links = []
    for item in html.find_all("a"):
        if "href" in item.attrs and item.attrs["href"].startswith("/") and item.attrs["href"] != "/2018/01/01/demo/" and item.text.strip():
            links.append(item.attrs["href"])
    return [HOME + i for i in links]

def main():
    browser = create_browser('/usr/bin/chromedriver')

    click_number = 0
    unique_links = [HOME]
    points = [(click_number, len(unique_links))]

    all_links = [HOME]
    
    current_link = HOME
    while click_number < 1000:
        links = get_hyperlinks(browser, current_link)

        all_links += links

        current_link = random.choice(links)
        if current_link.strip("/") not in unique_links:
            unique_links.append(current_link.strip("/"))
        points.append((click_number, len(unique_links)))
        click_number += 1
        if not click_number % 100:
            current_link = HOME
        print(click_number, len(unique_links))
    
    print(len(unique_links))
    print(len(list(set(all_links))))
    print(list(set(all_links)))


if __name__ == "__main__":
    main()
    '''
    result = []
    for i in range(10):
        result.append((i, main()))
    
    with open("data.txt", "wb") as f:
        f.write(str(result))
    '''
