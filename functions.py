from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def login(driver):
    driver.get('https://binance.com')

    #wait = WebDriverWait(driver, 1000000)
    #wait.until(EC.presence_of_element_located((By.ID, ['header_login','header_menu_cabinet','mobile_header_menu_cabinet'])))

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

    while True:
        try:
            cabinet = driver.find_element(By.ID, 'header_deposit_drawer')
            if cabinet:
                print('Login success')
                return driver
        except Exception as e:
            print('Still waiting for login')
            time.sleep(1)
            continue



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


