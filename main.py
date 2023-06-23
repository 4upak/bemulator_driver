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
from websocket import create_connection
import ssl

ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.check_hostname = False


account = "serg.chupak@gmail.com"
#account = "avshapes@gmail.com"
#ws_url = "ws://0:8000/ws/emulator/emulator/"
ws_url = "wss://wss.digichanger.pro/ws/emulator/emulator/"
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
                send_notification(account,"Login request received")
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']

                if str(action_account) == str(account):
                    driver = login(driver, account)
                    #driver = get_ballance(driver, action_account)
                else:
                    print(action_account + " != " + account)


            if action == 'add_payment_method':

                print(action)
                send_notification(account,"add_payment_method request received")
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']
                if str(action_account) == str(account):
                    driver = add_payment_method(driver,action_account, data['card_number'], data['name_on_card'], data['bank_name'])
                else:
                    print(action_account + " != " + account)

            if action == 'create_bid':
                print(action)
                send_notification(account,"create_bid request received")
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']
                digichanger_order_id = data['digichanger_order_id']
                if str(action_account) == str(account):
                    driver = add_bid(driver, data['currency'],data['amount'], data['min_amount'], data['autoreplay_text'], account)
                    print(f"{digichanger_order_id} created")
                    posted_bid_data = get_created_bid_data(driver, account)
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
                send_notification(account,"post_bid request received")
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']

                digichanger_order_id = data['digichanger_order_id']
                time.sleep(3)
                i=0
                if str(action_account) == str(account):
                    while True:
                        print("Main iretation started")
                        driver = add_payment_method(driver, action_account, data['card_number'], data['name_on_card'],
                                                    data['bank_name'])
                        time.sleep(5)
                        result = add_bid(driver, data['currency'], data['amount'], data['min_amount'],
                                         data['autoreplay_text'], account)
                        print(result)
                        print('Post bid iteration end')
                        driver = result['driver']
                        success = result['success']


                        if success == True:
                            print(f"{digichanger_order_id} created")
                            time.sleep(10)
                            j=0
                            break
                        i+=1
                        if i>3:
                            break
                            print("bid not posted 3 times")

                    j = 0
                    while True:
                        posted_bid_data = get_created_bid_data(driver, account)
                        print(posted_bid_data)
                        if posted_bid_data:
                            posted_bid_data['digichanger_order_id'] = digichanger_order_id
                            posted_bid_data['account_email'] = action_account
                            print(posted_bid_data)
                            post_request = requests.post('https://services.digichanger.pro/bemulator/api/binance_bid/add/',
                                                         data=posted_bid_data)
                            print(vars(post_request)['_content'])
                            if json.loads(vars(post_request)['_content'])['succeess'] == True:
                                print("bid posted")
                                break
                            else:
                                driver.refresh()
                                time.sleep(3)
                            j += 1
                        if j > 3:
                            break
                            print("data not send 3 times")




                else:
                    print(action_account + " != " + account)

            if action == 'set_currency':
                print(action)
                send_notification(account,"set_currency request received")
                data = message_dict['data']
                print(data['account'])
                action_account = data['account']

                if str(action_account) == str(account):
                    driver = set_currency(driver,action_account, data['currency'])
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
            ws.run_forever(ping_timeout=120,sslopt={"cert_reqs": ssl.CERT_NONE,
                   "check_hostname": False,
                   "ssl_version": ssl.PROTOCOL_TLSv1_2})
        except Exception as e:
            print(f"WebSocket error: {e}")
            time.sleep(1)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
