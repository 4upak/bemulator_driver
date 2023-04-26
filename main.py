# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
import pickle
import dill
import time
from functions import *
import websocket
import logging
import json
from pathlib import Path
from seleniumwire import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


account = "avshapes@gmail.com"
#ws_url = "ws://0:8000/ws/emulator/emulator/"
ws_url = "ws://167.235.77.8:8010/ws/emulator/emulator/"
driver = webdriver.Chrome()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def on_message(ws, message):
    global driver
    global account

    try:
        message = json.loads(message)
        if message['type'] == 'emulator_message':
            message_dict = json.loads(message['message'])
            action = message_dict['action']


            if action == 'login':
                print(action)
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']

                if str(action_account) == str(account):
                    driver = login(driver)
                    #driver = get_ballance(driver, action_account)
                else:
                    print(action_account + " != " + account)


            if action == 'add_payment_method':

                print(action)
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']
                if str(action_account) == str(account):
                    driver = add_payment_method(driver,action_account, data['card_number'], data['name_on_card'], data['bank_name'])
                else:
                    print(action_account + " != " + account)

            if action == 'create_bid':
                print(action)
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']
                digichanger_order_id = data['digichanger_order_id']
                if str(action_account) == str(account):
                    driver = add_bid(driver, data['currency'],data['amount'], data['min_amount'], data['autoreplay_text'])
                    print(f"{digichanger_order_id} created")
                    posted_bid_data = get_created_bid_data(driver)
                    print(posted_bid_data)
                    posted_bid_data['digichanger_order_id'] = digichanger_order_id
                    posted_bid_data['account_email'] = action_account
                    print(posted_bid_data)
                    post_request = requests.post('https://services.digichanger.pro/bemulator/api/binance_bid/add/', data=posted_bid_data)
                    print(vars(post_request))

                else:
                    print(action_account + " != " + account)

            if action == 'post_bid':
                print(action)
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']
                if str(action_account) == str(account):
                    driver = add_payment_method(driver, action_account, data['card_number'], data['name_on_card'],
                                                data['bank_name'])
                else:
                    print(action_account + " != " + account)

                digichanger_order_id = data['digichanger_order_id']
                time.sleep(3)
                if str(action_account) == str(account):
                    driver = add_bid(driver, data['currency'], data['amount'], data['min_amount'],
                                     data['autoreplay_text'])
                    print(f"{digichanger_order_id} created")
                    time.sleep(5)
                    posted_bid_data = get_created_bid_data(driver)
                    print(posted_bid_data)
                    posted_bid_data['digichanger_order_id'] = digichanger_order_id
                    posted_bid_data['account_email'] = action_account
                    print(posted_bid_data)
                    post_request = requests.post('https://services.digichanger.pro/bemulator/api/binance_bid/add/',
                                                 data=posted_bid_data)
                    print(vars(post_request))

                else:
                    print(action_account + " != " + account)






    except Exception as e:
        print(e)

    '''try:
        Path('cookies.json').write_text(
            json.dumps(driver.get_cookies(), indent=2)
        )
        print("cookies saved")
    except Exception as e:
        print(e)'''




def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")
    #reconnect websocket



def on_open(ws):
    print("WebSocket opened")

    # send a message when the WebSocket is opened
    json_message = {"type": "emulator_message", "message": "Hello, world!"}
    ws.send(json.dumps(json_message))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('websocket')
    logger.setLevel(logging.DEBUG)

    while True:
        try:
            ws = websocket.WebSocketApp(ws_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close,
                                        on_open=on_open,

                                        )
            ws.on_open = on_open
            ws.run_forever(ping_timeout=120)
        except Exception as e:
            print(f"WebSocket error: {e}")
            time.sleep(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
