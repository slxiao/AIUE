from __future__ import print_function
from __future__ import division

import re
import random
import sys
import hashlib

import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


home = "https://slxiao.github.io"


def create_browser(webdriver_path):
    browser_options = Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument('--no-sandbox')
    return webdriver.Chrome(webdriver_path, chrome_options=browser_options)

browser = create_browser('/usr/bin/chromedriver')

def encode_string(string):
    import hashlib
    return str(int(hashlib.sha1(string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))


def get_actions(state):
    browser.get(state)
    html = bs(browser.page_source, "lxml")
    actions = []
    for item in html.find_all("a"):
        if "href" in item.attrs and item.attrs["href"].startswith("/") and item.attrs["href"] != "/2018/01/01/demo/" and item.text.strip():
            actions.append(home + item.attrs["href"] + "||" + encode_string(item.attrs["href"] + item.text))
    return actions


iteration = 0
gamma = 0.8
state_action_qvalues = pd.DataFrame(index=[home]) 
state_action_exetimes = pd.DataFrame(index=[home]) 

while iteration < 10000:
    current_state = np.random.choice(state_action_qvalues.index)
    available_actions = get_actions(current_state)

    for action in available_actions:
        if action not in state_action_qvalues.columns:
            state_action_qvalues[action] = 0
            state_action_qvalues.at[current_state, action] = 10000
        if action not in state_action_exetimes.columns:
            state_action_exetimes[action] = 0

    
    best_action = state_action_qvalues.loc[current_state][available_actions].nlargest().sample().index[0]

    next_state = best_action.split("||")[0]
    next_available_actions = get_actions(next_state)

    if next_state not in state_action_qvalues.index:
        state_action_qvalues.loc[next_state] = 0
    if next_state not in state_action_exetimes.index:
        state_action_exetimes.loc[next_state] = 0
    for action in next_available_actions:
        if action not in state_action_qvalues.columns:
            state_action_qvalues[action] = 0
            state_action_qvalues.at[next_state, action] = 10000
    
    if state_action_exetimes.at[current_state, best_action] == 0:
        reward = 10000
    else:
        reward = 1 / state_action_exetimes.at[current_state, best_action]
    
    max_next_state_qvalue = state_action_qvalues.loc[next_state][next_available_actions].max()

    state_action_qvalues.at[current_state, best_action] = reward + gamma * max_next_state_qvalue

    state_action_exetimes.at[current_state, best_action] += 1

    iteration += 1

    print("iteration: %s, current_state: %s, next_state: %s" % (iteration, current_state, next_state))


state_action_qvalues.to_csv('state_action_qvalues.csv')
state_action_exetimes.to_csv('state_action_exetimes.csv')

state_action_qvalues = pd.read_csv("state_action_qvalues.csv", index_col=0)

click_number = 0
current_state = home
unique_states = [home]	
points = [(click_number, len(unique_states))]

while click_number < 1000:	
    available_actions = get_actions(current_state)
    best_action = state_action_qvalues.loc[current_state][available_actions].nlargest().sample().index[0]
    #best_action = state_action_qvalues.loc[current_state][available_actions].idxmax()
    print(current_state, best_action)
    current_state = best_action.split("||")[0]
    if current_state not in unique_states:
        unique_states.append(current_state)
    points.append((click_number, len(unique_states)))
    click_number += 1
    if not click_number % 100:
        current_state = home
    print(click_number, len(unique_states))

print(unique_states)
