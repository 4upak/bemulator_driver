# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver

import time
from functions import *
import websocket
import logging
import json


account = "serg_chupak@gmail.com"
driver = webdriver.Chrome('chromedriver')
engage = False

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.



def on_message(ws, message):
    global driver
    global account
    print(message)

    try:
        message = json.loads(message)
        if message['type'] == 'emulator_message':
            message_dict = json.loads(message['message'])
            action = message_dict['action']


            if action == 'login':
                print(action)
                print(message_dict['data'])
                data = message_dict['data']
                action_account = data['account']
                if str(action_account) == str(account):
                    driver = login(driver)
                else:
                    print(action_account + " != " + account)

    except Exception as e:
        print(e)



def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")
    driver.quit()

def on_open(ws):
    print("WebSocket opened")
    # send a message when the WebSocket is opened
    json_message = {"type": "emulator_message", "message": "Hello, world!"}
    ws.send(json.dumps(json_message))

    def send_ping():
        while ws.keep_running:
            ws.send_ping()
            time.sleep(5)


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
    ws.run_forever(ping_timeout=120)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
