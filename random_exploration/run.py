#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import random

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

home = "http://10.183.42.165:3000"


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
    return [home + i for i in links]


browser = create_browser('/usr/bin/chromedriver')

iteration = 0
current_link = home
unique_links = [current_link]

while iteration < 1000:
    current_link = random.choice(get_hyperlinks(browser, current_link))
    if current_link.strip("/") not in unique_links:
        unique_links.append(current_link.strip("/"))
    
    iteration += 1
    if not iteration % 100:
        current_link = home
    print("iteration: %s, unique_states: %s" % (iteration, len(unique_links)))

print(unique_links)
