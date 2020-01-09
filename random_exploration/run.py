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

browser = create_browser('/usr/bin/chromedriver')


def get_hyperlinks():
    html = bs(browser.page_source, "lxml")
    links = []
    for item in html.find_all("a"):
        if "href" in item.attrs and item.attrs["href"].startswith("/") and item.attrs["href"] != "/2018/01/01/demo/" and item.text.strip():
            links.append(item.attrs["href"])
    return links

def loop():
    iteration = 0
    current_link = "/"
    browser.get(home)
    unique_links = [current_link]
    points = []
    while iteration < 10000:
        if current_link != "/":
            browser.find_element_by_xpath('//a[contains(@href,"%s")]' % current_link).click()
        current_link = random.choice(get_hyperlinks())
        if current_link.strip("/") not in unique_links:
            unique_links.append(current_link.strip("/"))
    
        iteration += 1
        if not iteration % 1000:
            current_link = "/"
            browser.get(home)
        #print("iteration: %s, unique_links: %s" % (iteration, len(unique_links)))
        points.append((iteration, len(unique_links)))

    return points


result = []
for i in range(10):
    result.append((i, loop()))

print(result)