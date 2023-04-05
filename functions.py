from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login(driver):
    driver.get('https://binance.com')

    wait = WebDriverWait(driver, 1000000)
    wait.until(EC.presence_of_element_located((By.ID, 'header_login')))

    link = driver.find_element(By.ID, 'header_login')
    # if element finded
    if link:
        # click on element
        link.click()
    else:
        print('link not found')

    while True:
        try:
            cabinet = driver.find_element(By.ID, 'header_menu_cabinet')
            if cabinet:
                print('Login success')
                break

            cabinet = driver.find_element(By.ID, 'mobile_header_menu_cabinet')
            if cabinet:
                print('Login success')
                break
        except:
            print('Still waiting for login')
            time.sleep(1)
            continue

    return driver

def quit(webdriver):
    pass

def add_payment_method(webdriver):
    pass

def add_bid(webdriver):
    pass

def get_order_list(webdriver):
    pass

def get_order_detail(webdriver):
    pass

def accept_order(webdriver):
    pass


