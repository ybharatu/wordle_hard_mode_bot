from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from wordle_bot import *

def goaway_popup(driver_instance):
    close_button = driver_instance.find_element(By.CLASS_NAME, 'Modal-module_closeIcon__TcEKb')
    #driver_instance.find_element(By.CSS_SELECTOR, '[aria-label="Close"]').click()
    close_button.click()
    print("Clicking close button")

def click_play(driver_instance):
    play_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="Play"]')
    play_button.click()
    print("Clicking Play button")


driver = webdriver.Safari()

url = "https://www.nytimes.com/games/wordle/index.html?register=email&auth=register-email"
driver.get(url)
# Find the button by its data-testid attribute

#play_button = driver.find_element_by_css_selector('[data-testid="Play"]')
# Click the Play button
click_play(driver)
time.sleep(2)
# Close Pop up
goaway_popup(driver)
time.sleep(2)

all_guesses = play_wordle_bot_2(driver)
print(all_guesses)

time.sleep(10)

#driver.quit()
