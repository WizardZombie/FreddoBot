import io
import json
import sys
import os
from datetime import datetime, date, time

originalFreddo = 0.30
freddoPrice = None
token = None

def setup():
    global originalFreddo, freddoPrice, token
    reply = False
    userInput = ""
    while userInput == "":
        userInput = input('Please enter bot token: \n')
    token = userInput
    freddoPrice = 0.30
    originalFreddo = 0.10
    with io.open('utils/config.txt', 'w', encoding='utf-8') as f:
                f.write(json.dumps({'token':token, 'freddoPrice':freddoPrice, 'originalFreddo':originalFreddo}, sort_keys=True, indent=4, ensure_ascii=False))

try:
    with open('utils/config.txt') as data_file:
        data = json.load(data_file)
        originalFreddo = data['originalFreddo']
        freddoPrice = data['freddoPrice']
        token = data['token']
except FileNotFoundError:
    print('Config Not found! Initiating setup ...')
    setup()

def get_freddo():
    return freddoPrice

def get_original():
    return originalFreddo

def get_token():
    return token

def change_price(newPrice):
    try:
        freddoPrice = newPrice()
        return 1
    except ValueError:
        return 0