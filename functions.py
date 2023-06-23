from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random

def get_mfa_code(email):
    post_data = {
        'email': email,
    }
    print(post_data)
    response = requests.post('https://services.digichanger.pro/bemulator/api/get_binance_auth_by_mail/', data=post_data)
    print(response.json())
    try:
        return response.json()['code']
    except Exception as e:
        print(e)
        return False

def set_input_value(driver, input, value):
    ActionChains(driver).double_click(input).perform()
    ActionChains(driver).send_keys(Keys.DELETE).send_keys(value).perform()

    input_value = input.get_attribute('value')
    i=0
    while float(input_value) != float(value):
        print(input_value + "!=" + value)
        ActionChains(driver).double_click(input).perform()
        ActionChains(driver).send_keys(Keys.DELETE).send_keys(currency).perform()
        input_value = input.get_attribute('value')
        i+=1
        if i>5:
            return False

    return True

def login(driver,account_email):
    driver.get('https:///p2p.binance.com')
    while True:
        try:
            if driver.find_element(By.ID, 'header_deposit_drawer'):
                break
        except Exception as e:
            pass

        try:
            link = driver.find_element(By.ID, 'header_login')
            if link:
                link.click()
                break
        except Exception as e:
            print('Wair for login button')
            send_notification(account_email, 'Wair for login button')
            time.sleep(1)
            continue

        try:
            print('Checking for coockies button')
            send_notification(account_email, 'Checking for coockies button')
            accept_coockies_button = driver.find_element(By.XPATH, "//button[contains(text(),'I accept')]")
            if accept_coockies_button:
                accept_coockies_button.click()
                continue
        except Exception as e:
            pass

    while True:
        try:
            cabinet = driver.find_element(By.ID, 'header_deposit_drawer')
            if cabinet:
                driver.get('https:///p2p.binance.com')
                print('Login success')
                send_notification(account_email, 'Login success')
                return driver
        except Exception as e:
            print('Still waiting for login')
            send_notification(account_email, 'Still waiting for login')
            time.sleep(1)
            continue

def get_ballance(driver, account_email):
    url = 'https://www.binance.com/en/my/wallet/account/overview'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'walletOverview_transaction_history_aLink')))
    time.sleep(3)
    #get text from div with id =balance-text
    balance = driver.find_element(By.ID, 'balance-text').text
    balance = balance.split(' ')[0]
    #get bitcoin price in usd
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url)
    btc_price = float(response.json()['price'])
    print (f"BTC price: {btc_price}")

    balance_in_usd = float(balance) * btc_price
    print (f"Balance in USD: {balance_in_usd}")

    post_data = {
        'balance': balance_in_usd,
        'email': account_email,
    }
    print(post_data)
    result = requests.post('https://services.digichanger.pro/bemulator/api/update_binance_ballance/', data=post_data)
    print(result.json())
    return driver

def quit(webdriver):
    pass

def add_payment_method(driver,account_email,card_number,card_holder_name,bank_name):
    url = 'https://p2p.binance.com/en/myads'
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'C2C_p2pMyAdsList_filter_btn_filter')))
    time.sleep(5)

    print("Checking for other bid")
    try:

        close_element = driver.find_element(By.ID, "C2C_p2pMyAdsList_management_btn_close")
        if close_element:
            print("Other bid found")
            send_notification(account_email, "Other bid found")
            close_element.click()
            print("Close element clicked")
            send_notification(account_email, "Close element clicked")


            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "div.css-vurnku button.css-18jinle").click()
            print("Close button clicked")
            send_notification(account_email, "Close button clicked")

            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR,
                                "div.styled__ButtonWrap-sc-1icz59t-3.fouYfr.css-4cffwv > button.css-18jinle").click()

    except Exception as e:
        print("Other payment methods not found")
    #delete old payment methods
    print("Account email: " + account_email)
    send_notification(account_email, "Account email: " + account_email)
    driver.get('https://p2p.binance.com/en/userCenter#payment')


    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "tab-payment")))
    print("Payment methods page loaded")
    send_notification(account_email, "Payment methods page loaded")

    time.sleep(5)

    buttons = driver.find_elements(By.XPATH,"//button[contains(text(),'Delete')]")

    print(f"{len(buttons)} payment methods found")
    send_notification(account_email, f"{len(buttons)} payment methods found")


    for button in buttons:
        button.click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//div[contains(text(),'Confirm')]").click()
        time.sleep(2)

    print("All payment methods deleted")
    send_notification(account_email, "All payment methods deleted")

    url = f"https://p2p.binance.com/en/payment/add/{bank_name}"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PaymentMethodForm__form_wrapper')))

    input_card_number = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Please enter your bank account number"]')
    input_card_number.send_keys(card_number)

    input_bank_name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter the name of your bank"]')
    input_bank_name.send_keys(card_holder_name)

    confirm_button = driver.find_element(By.XPATH,"//button[contains(text(),'Confirm')]")
    confirm_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'mfa-google-input')))

    mfa_input = driver.find_element(By.ID, 'mfa-google-input')
    mfa_code = get_mfa_code(account_email)
    if mfa_code:
        send_notification(account_email, "MFA code found")
        mfa_input.send_keys(mfa_code)
    else:
        print('MFA code not found')
        send_notification(account_email, "MFA code not found")
        mfa_code = input('Enter MFA code: ')
        mfa_input.send_keys(mfa_code)

    print("MFA code entered")
    send_notification(account_email, "MFA code entered")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PaymentMethodForm__form_wrapper')))
    print("Payment method added")
    send_notification(account_email, "Payment method added")

    return driver

def add_bid(driver, currency, amount, min_amount, autoreplay_text, account_email):
    url = 'https://p2p.binance.com/en/myads'
    driver.get(url)

    time.sleep(3)

    print("Checking for other bid")
    send_notification(account_email, "Checking for other bid")

    try:
        close_element = driver.find_element(By.ID, "C2C_p2pMyAdsList_management_btn_close")
        if close_element:
            print("Other bid found")
            send_notification(account_email, "Other bid found")
            close_element.click()
            print("Close element clicked")
            send_notification(account_email, "Close element clicked")

            time.sleep(1)

            driver.find_element(By.CSS_SELECTOR, "div.css-vurnku button.css-18jinle").click()
            print("Close button clicked")
            send_notification(account_email, "Close button clicked")

            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "div.styled__ButtonWrap-sc-1icz59t-3.fouYfr.css-4cffwv > button.css-18jinle").click()

    except Exception as e:
        print('Other bids chech error')


    print("No other bid found")
    send_notification(account_email, "No other bid found")

    time.sleep(3)

    try:
        driver.find_element(By.ID, 'C2C_p2pNav_btn_postNewAd').click()
        print("New bid button clicked")
        send_notification(account_email, "New bid button clicked")
    except Exception as e:
        print('New bid button not found')
        send_notification(account_email, "New bid button not found")
        return {'driver': driver, 'success': False}

    time.sleep(10)
    try:
        driver.find_element(By.CLASS_NAME,"css-1wk26uy").click()
    except Exception as e:
        print('Sell button not found')
        send_notification(account_email, "Sell button not found")
        return {'driver': driver, 'success': False}

    time.sleep(3)
    try:


        try:
            input = driver.find_element(By.ID, "C2C_p2pPost_step1_price_input")
            #scroll to element
            driver.execute_script("arguments[0].scrollIntoView();", input)

            print("Currency input found")
            send_notification(account_email, "Currency input found")
            print("Try to set currency: " + str(currency))
            send_notification(account_email, "Try to set currency: " + str(currency))

            ActionChains(driver).double_click(input).perform()
            ActionChains(driver).send_keys(Keys.DELETE).send_keys(currency).perform()

            input_value = input.get_attribute('value')

            while float(input_value) != float(currency):
                print(input_value + "!="+ currency)
                ActionChains(driver).double_click(input).perform()
                ActionChains(driver).send_keys(Keys.DELETE).send_keys(currency).perform()
                input_value = input.get_attribute('value')

            print("Currency input value: " + input_value)
            send_notification(account_email, "Currency input value: " + input_value)

        except Exception as e:
            print('Currency input not found')
            send_notification(account_email, "Currency input not found")
            return {'driver': driver, 'success': False}



        print("Currency entered")
        send_notification(account_email, "Currency entered")
    except Exception as e:
        print('Setting currency failed')
        send_notification(account_email, "Setting currency failed")
        return {'driver': driver, 'success': False}

    time.sleep(3)
    try:
        driver.find_element(By.ID,"C2C_p2pPost_step1_btn_next").click()
        print("Next button clicked")
        send_notification(account_email, "Next button clicked")
    except Exception as e:
        print('Next button not found')
        send_notification(account_email, "Next button not found")
        return {'driver': driver, 'success': False}


    #find input with name="initAmount"
    time.sleep(3)
    try:
        amount = round(float(amount), 2)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "initAmount")))
        print("Amount input found")
        send_notification(account_email, "Amount input found")
        input = driver.find_element(By.NAME, "initAmount")
        time.sleep(1)
        input.clear()
        input.send_keys(amount)

        input_value = input.get_attribute('value')


        while float(input_value) != float(amount):
            print(str(input_value) + "!=" + str(amount))
            input.clear()
            input.send_keys(amount)

            time.sleep(2)
            input_value = input.get_attribute('value')

        print("Amount entered: " + input_value)
        send_notification(account_email, "Amount entered: " + input_value)

    except Exception as e:
        print('Amount input not found')
        send_notification(account_email, "Amount input not found")
        return {'driver': driver, 'success': False}


    time.sleep(1)
    try:
        input = driver.find_element(By.NAME, "minOrderPrice")
        input.clear()
        time.sleep(1)
        input.clear()
        input.send_keys(min_amount)
        print("Min amount entered")
        send_notification(account_email, "Min amount entered")
    except Exception as e:
        print('Min amount input not found')
        send_notification(account_email, "Min amount input not found")
        return {'driver': driver, 'success': False}

    #fin button with css selector 'form > div:nth-child(3) > div > button'

    time.sleep(3)
    try:
        # fin button with css selector 'form > div:nth-child(3) > div > button'
        input = driver.find_element(By.CSS_SELECTOR, "form > div:nth-child(3) > div > button")
        input.click()
        time.sleep(2)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"SellPaymentForm__StyledCard-c6pg06-0")))

        driver.find_element(By.CLASS_NAME, "SellPaymentForm__StyledCard-c6pg06-0").click()
        time.sleep(1)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "C2C_p2pPost_step2_btn_next")))


    except Exception as e:
        print('Payment method selection failed')
        send_notification(account_email, "Payment method selection failed")
        return {'driver': driver, 'success': False}

    time.sleep(3)
    try:
        driver.find_element(By.ID, "C2C_p2pPost_step2_btn_next").click()
        print("Next button clicked")
        send_notification(account_email, "Next button clicked")

        #find textarea with name="autoReplyMsg"
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "autoReplyMsg")))
        print("Auto reply input found")
        send_notification(account_email, "Auto reply input found")

        textarea = driver.find_element(By.NAME, "autoReplyMsg")

        textarea.send_keys(autoreplay_text)
        time.sleep(1)

        remarks_textarea =  driver.find_element(By.NAME, "remarks")
        remarks_textarea.send_keys("Для звiтностi потрiбна квитанцiя або скрiншот транзакцiї. Дякую за розумiння.")
        time.sleep(1)

    except Exception as e:
        print('Auto reply input not found')
        send_notification(account_email, "Auto reply input not found")
        return {'driver': driver, 'success': False}


    time.sleep(5)
    try:
    # click on button with id "C2C_p2pPost_step3_btn_publish"
        driver.find_element(By.ID, "C2C_p2pPost_step3_btn_publish").click()
        print("Publish button will be clicked in 5 seconds")
        send_notification(account_email, "Publish button will be clicked in 5 seconds")
        time.sleep(5)

        #click on class with text "Confirm to Post"
        driver.find_element(By.CSS_SELECTOR,"div.css-1u2pn8e button.css-pawbdq").click()
        print("Confirm to post clicked")
        send_notification(account_email, "Confirm to post clicked")

        time.sleep(5)
        print("Bid added")
        send_notification(account_email, "Bid added")
        return {'driver': driver, 'success': True}
    except Exception as e:
        print('Bid not added')
        send_notification(account_email, "Bid not added")
        return {'driver': driver, 'success': False}

def get_order_list(webdriver):
    pass

def get_order_detail(webdriver):
    pass

def accept_order(webdriver):
    pass

def get_created_bid_data(driver, account_email):
    #get text by class css-plprkm
    result = {}
    try:
        bid_id = driver.find_element(By.CSS_SELECTOR,".css-g5ktnw div.css-plprkm").text
        result["ad_number"] = bid_id
    except Exception as e:
        print(e)
        print("ad_number not found")
        send_notification(account_email, "ad_number not found")
        try:
            bid_id = driver.find_element(By.CSS_SELECTOR, ".css-1div323 div.css-plprkm").text
            result["ad_number"] = bid_id
        except Exception as e:
            result["ad_number"] = random.randint(100000, 999999)

    try:
        amount = driver.find_element(By.CSS_SELECTOR,".css-g5ktnw div.css-hjmza4").text
        result["amount"] = amount.replace(',','')
    except Exception as e:
        print(e)
        print("amount not found")
        send_notification(account_email, "amount not found")
        return False

    try:
        price = driver.find_element(By.CSS_SELECTOR,".css-g5ktnw div.css-x56ygg").text
        result["price"] = float(price)
    except Exception as e:
        print(e)
        print("price not found")
        send_notification(account_email, "price not found")
        return False

    try:
        type = driver.find_element(By.CSS_SELECTOR,".css-g5ktnw div.css-1v10lrq").text
        result["type"] = type
    except Exception as e:
        print(e)
        print("type not found")
        send_notification(account_email, "type not found")
        return False

    return result

def send_notification(account, message):
    data = {
        "account_email": account,
        "message": message,
    }
    url = "https://services.digichanger.pro/bemulator/api/driver_notify/"

    try:
        requests.post(url, data=data)
    except Exception as e:
        print(e)
        print("Notification not sent")


def set_currency(driver, account_email, currency):
    driver.get('https://p2p.binance.com/en/myads?type=normal&code=default')
    time.sleep(5)
    delta = 0
    delta_index = 0
    try:
        edit_button = driver.find_element(By.ID, 'C2C_p2pMyAdsList_management_btn_edit')
        edit_button.click()

    except Exception as e:
        print("Currency edit button found")
        send_notification(account_email, "Currency select not found")
        return driver

    time.sleep(5)

    try:

        currency_input = driver.find_element(By.CSS_SELECTOR, '.styled__Wrap-op0405-0 input')
        value = currency_input.get_attribute('value')
        if value != currency:
            set_input_value(driver, currency_input, currency)
            delta =  float(value) - float(currency)
            delta_index = delta/float(value)


    except Exception as e:
        print(e)
        print("Currency input not found")
        send_notification(account_email, "Currency input not found")
        return driver

    time.sleep(2)

    try:
        amount_input = driver.find_element(By.CSS_SELECTOR, '.css-1sstzk2 input.css-16fg16t')
        amount_value = amount_input.get_attribute('value')

        new_amount_value = (float(amount_value)*1.001 + float(amount_value)*1.001*float(delta_index))

        set_input_value(driver, amount_input, round(new_amount_value,2))

    except Exception as e:
        print(e)
        print("Amount input not found")
        send_notification(account_email, "Amount input not found")
        return driver

    try:
        min_limit_input = driver.find_element(By.XPATH, '//*[@id="c2c_advDetail_trading_amount"]/div[3]/div[2]/div[1]/div/input')
        min_limit_value = min_limit_input.get_attribute('value')

        max_limit_input = driver.find_element(By.XPATH, './/*[@id="c2c_advDetail_trading_amount"]/div[3]/div[2]/div[3]/div/input')
        set_input_value(driver, max_limit_input, min_limit_value)
    except Exception as e:
        print(e)
        return driver
    #find button by text "Post"

    time.sleep(2)

    try:
        post_button = driver.find_element(By.CSS_SELECTOR, '.css-14teco8 button.css-g3exg4')
        post_button.click()
        time.sleep(2)
        accept_button = driver.find_element(By.CSS_SELECTOR, '.css-1u2pn8e button.css-pawbdq')
        accept_button.click()

    except Exception as e:
        print("Post button not found")
        send_notification(account_email, "Post button not found")
        return driver

    time.sleep(2)
    return driver






