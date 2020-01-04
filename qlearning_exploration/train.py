from __future__ import print_function

import re
import random
import numpy as np

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys
np.set_printoptions(threshold=sys.maxsize)

HOME = "https://slxiao.github.io"

def create_browser(webdriver_path):
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    return webdriver.Chrome(webdriver_path, chrome_options=browser_options)

browser = create_browser('/usr/bin/chromedriver')

def get_hyperlinks(url):
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

gamma = 0.8

q_matrix = np.full((64,64), 10000)

current_url = "https://slxiao.github.io"
current_state = hash(current_url) % 64

click_number = 0

state_action_record = np.zeros((64,64))

while click_number < 10:
    available_links = get_hyperlinks(current_url)
    available_actions = [hash(link) % 64 for link in available_links]

    max_q_value = -1
    max_q_action = None
    max_q_link = ""
    for i in range(len(available_actions)):
        if q_matrix[current_state][available_actions[i]] > max_q_value:
            max_q_value = q_matrix[current_state][available_actions[i]]
            max_q_action = available_actions[i]
            max_q_link = available_links[i]
    
    next_url = max_q_link
    next_state = hash(next_url) % 64
    next_available_links = get_hyperlinks(next_url)
    next_available_actions = [hash(link) % 64 for link in next_available_links]
    
    if state_action_record[current_state][max_q_action] == 0:
        reward = 10000
    else:
        reward = 1 / state_action_record[current_state][max_q_action]
    
    state_action_record[current_state][max_q_action] += 1
    
    max_future_q_value = -1
    max_future_q_action = None
    max_future_q_link = ""
    for i in range(len(next_available_actions)):
        if q_matrix[next_state][next_available_actions[i]] > max_future_q_value:
            max_future_q_value = q_matrix[next_state][next_available_actions[i]]
            max_future_q_action = next_available_actions[i]
            max_future_q_link = next_available_actions[i]

    q_matrix[current_state][max_q_action] = reward + gamma * max_future_q_value

    click_number += 1

    if click_number > 0 and not click_number % 100:
        current_url = "https://slxiao.github.io"
        current_state = hash(current_url) % 64
    else:
        current_url = next_url
        current_state = next_state


print(q_matrix)

    