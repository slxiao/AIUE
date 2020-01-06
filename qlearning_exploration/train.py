from __future__ import print_function

import re
import random
import sys
import hashlib

import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from numpy import savetxt
from numpy import loadtxt

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


home = "https://slxiao.github.io"
browser = create_browser('/usr/bin/chromedriver')


def create_browser(webdriver_path):
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    return webdriver.Chrome(webdriver_path, chrome_options=browser_options)


def encode_string(string):
    import hashlib
    return str(int(hashlib.sha1(string).hexdigest(), 16) % (10 ** 8))


def get_actions(state):
    browser.get(state)
    html = bs(browser.page_source, "lxml")
    actions = []
    for item in html.find_all("a"):
        if "href" in item.attrs and item.attrs["href"].startswith("/") and item.attrs["href"] != "/2018/01/01/demo/" and item.text.strip():
            actions.append(home + item.attrs["href"] + "||" + encode_string(item.attrs["href"] + item.text))
    return actions



iterations = 0
gamma = 0.8
current_state = home
quality_value_df = pd.DataFrame(index=[current_state])
action_execution_df = pd.DataFrame(index=[current_state])
available_actions = get_actions(current_state)

while iterations < 1000:
    
    for action in available_actions:
        if action not in quality_value_df.columns:
            quality_value_df[action] = 10000
        if action not in action_execution_df.columns:
            action_execution_df[action] = 0
    
    best_action = quality_value_df.loc[current_state, :][available_actions].argmax()

    next_state = best_action.split("||")[0]
    next_available_actions = get_actions(next_state)

    if next_state not in quality_value_df.index:
        quality_value_df.loc[next_state] = 0
    if next_state not in action_execution_df.index:
        action_execution_df.loc[next_state] = 0

    for action in next_available_actions:
        if action not in quality_value_df:
            quality_value_df[action] = 10000

    available_urls = get_urls(current_url)
    update_url_state_mapping(available_urls)

    available_actions = [url_to_state[url] for url in available_urls]
    
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

    #links_mapping.update({next_available_actions[i]: next_available_links[i] for i in range(len(next_available_links))})
    
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

    stopping_iterations += 1

    if stopping_iterations > 0 and not stopping_iterations % 100:
        current_url = "https://slxiao.github.io"
        current_state = hash(current_url) % 64
    else:
        current_url = next_url
        current_state = next_state


print(q_matrix)

savetxt('data.csv', q_matrix, delimiter=',')

q_matrix = loadtxt('data.csv', delimiter=',')


click_number = 0
unique_links = []
points = [(click_number, len(unique_links))]

current_url = "https://slxiao.github.io"

while click_number < 1000:
    print(current_url)
    links = get_hyperlinks(current_url)
    current_state = hash(current_url) % 64

    q_value_list = []
    for link in links:
        q_value_list.append((link, q_matrix[current_state][hash(link) % 64]))

    max_q_value = max([i[1] for i in q_value_list])

    candidate_links = [i[0] for i in q_value_list if i[1] == max_q_value]

    print(q_value_list)
    next_link = random.choice(candidate_links)
    
    if next_link not in unique_links:
        unique_links.append(next_link)
    
    points.append((click_number, len(unique_links)))
    click_number += 1

    print(click_number, len(unique_links))

    if not click_number % 100:
        current_url = "https://slxiao.github.io"
    else:
        current_url = next_link


    