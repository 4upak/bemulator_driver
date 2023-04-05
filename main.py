# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def start_browser():
    driver = webdriver.Chrome('chromedriver')
    driver.get('https://binance.com')

    time.sleep(10) # Let the user actually see something!
    #click link element by id header_login
    #link = driver.find_element_by_id('header_login')
    link = driver.find_element(By.ID, 'header_login')
    #if element finded
    if link:
        #click on element
        link.click()
    else:
        print('link not found')

    time.sleep(10) # Let the user actually see something!


    driver.quit()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    start_browser()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
