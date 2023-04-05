# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver

import time
from functions import *
import websocket
import logging
import json

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def start_browser():
    driver = webdriver.Chrome('chromedriver')


    driver = login(driver)


    driver.quit()

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")
    # send a message when the WebSocket is opened
    json_message = {"type": "emulator_message", "message": "Hello, world!"}
    ws.send(json.dumps(json_message))
    start_browser()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger('websocket')
    logger.setLevel(logging.DEBUG)
    ws = websocket.WebSocketApp("ws://0:8000/ws/emulator/emulator/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open,
                                )
    ws.on_open = on_open
    ws.run_forever()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
