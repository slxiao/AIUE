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


home = "http://10.183.42.165:3000"


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

# initialization
current_state = home
unique_states = [current_state]
available_actions = get_actions(current_state)
state_action_qvalues = pd.DataFrame(index=[current_state]) 
state_action_exetimes = pd.DataFrame(index=[current_state]) 
for action in available_actions:
    state_action_qvalues[action] = 10000
    state_action_exetimes[action] = 0

all_states = [current_state]

while iteration < 1000:
    # select best action
    all_states += [i.split("||")[0] for i in available_actions]
    available_state_action_qvalues = state_action_qvalues.loc[current_state][available_actions]
    best_action = np.random.choice(available_state_action_qvalues.index, p=[i/available_state_action_qvalues.sum() for i in available_state_action_qvalues])
    
    # get next state
    next_state = best_action.split("||")[0]
    if next_state.strip("/") not in unique_states:
        unique_states.append(next_state.strip("/"))
    if next_state not in state_action_qvalues.index:
        state_action_qvalues.loc[next_state] = 0.0
    if next_state not in state_action_exetimes.index:
        state_action_exetimes.loc[next_state] = 0

    # get next available actions
    next_available_actions = get_actions(next_state)
    for action in next_available_actions:
        if action not in state_action_qvalues.columns:
            state_action_qvalues[action] = 0.0
        if action not in state_action_exetimes.columns:
            state_action_exetimes[action] = 0
        if state_action_exetimes.at[next_state, action] == 0:
            state_action_qvalues.at[next_state, action] = 10000.0
    
    # update current state -> best action quality value
    state_action_exetimes.at[current_state, best_action] += 1
    reward = 1 / state_action_exetimes.at[current_state, best_action]
    max_next_state_qvalue = state_action_qvalues.loc[next_state][next_available_actions].max()
    state_action_qvalues.at[current_state, best_action] = reward + gamma * max_next_state_qvalue
    #print(state_action_qvalues.at[current_state, best_action], reward + gamma * max_next_state_qvalue)

    iteration += 1
    
    if not iteration % 100: # return back to home every 100 iterations
        current_state = home
        available_actions = get_actions(home)
    else:
        current_state = next_state
        available_actions = next_available_actions
    print(next_state, [i.split("||")[0] for i in available_actions], "iteration: %s, unique_states: %s" % (iteration, len(unique_states)), len(list(set(all_states))))