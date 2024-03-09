from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from wordle_bot import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import storage
from openai import OpenAI
client = OpenAI()
import os
from datetime import datetime

def goaway_popup(driver_instance):
    close_button = driver_instance.find_element(By.CLASS_NAME, 'Modal-module_closeIcon__TcEKb')
    #driver_instance.find_element(By.CSS_SELECTOR, '[aria-label="Close"]').click()
    close_button.click()
    print("Clicking close button")

def click_play(driver_instance):
    play_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="Play"]')
    play_button.click()
    print("Clicking Play button")


def write_poem_to_file(poem):
    # Get the current date
    current_date = datetime.now()

    # Format the date as required
    formatted_date = current_date.strftime("%b_%d_%Y")

    # Create the poems directory if it doesn't exist
    poems_dir = os.path.join(os.path.dirname(__file__), "poems")
    os.makedirs(poems_dir, exist_ok=True)

    # Construct the filename
    filename = os.path.join(poems_dir, f"{formatted_date}.txt")

    # Write the poem to the file
    with open(filename, 'w') as f:
        f.write(poem)

def write_words_to_file(words, num):
    # Get the current date
    current_date = datetime.now()

    # Format the date as required
    formatted_date = current_date.strftime("%b_%d_%Y")

    # Write the poem to the file
    with open("word_list_history.txt", 'a') as f:
        f.write(formatted_date + " ")
        f.write(str(words) + " " + str(num) + "\n")

def EmailNotifyRun(all_guesses):
    num_tries = all_guesses[-1]
    guesses = all_guesses[:-1]

    # Write words to a file
    write_words_to_file(guesses, num_tries)

    # Email Code
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(storage.GMAIL_USER, storage.GMAIL_PASS)

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = "WordleSolver@gmail.com"
    msg['To'] = storage.GMAIL_USER

    # Change the subject here
    if num_tries < 7:
        subject = "Wordle Completed in " + str(num_tries) + " attempts!"
    else:
        subject = "Wordle Notification"

    msg['Subject'] = subject

    # Add message body
    body = ""
    all_words = ""
    if num_tries < 7:
        body += "Success!! Wordle Completed in " + str(num_tries) + " attempts!\nWords Guessed:\n"
    else:
        body += "Failure!! :("
    for g in guesses:
        body += g + "\n"
        all_words += g + " "
    body += "\n\n"

    completion = client.chat.completions.create(
        #model="gpt-3.5-turbo-0125",
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system",
             "content": "You are an incredible poet drawing inspiration from all world-famous poets and poetry. You can make poetry out of anything. I can give you a series of random words and then can you make a poem that includes all of them. Create a title after creating the poem."},
            {"role": "user", "content": all_words}
        ]
    )
    # Access the first choice from the completion
    gpt_response = completion.choices[0]
    #print(gpt_response)

    # Get the text content of the response
    poem = gpt_response.message.content
    print(poem)
    write_poem_to_file(poem)
    body += poem

    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    s.sendmail("WordleSolver@gmail.com", storage.GMAIL_USER, msg.as_string())
    s.quit()

# <button type="button" id="AppHeader-module_navButton__nKv2h" class="AppHeader-module_icon__qLz07" aria-label="Menu" aria-haspopup="menu" aria-controls="nav-modal" aria-expanded="false"><svg aria-hidden="true" class="NavIcon-module_burgerSvg__j9Cig" width="20" height="17" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="0.172974" width="20" height="3" rx="1.5" fill="var(--color-tone-1)"></rect><rect x="0.172974" y="7" width="20" height="3" rx="1.5" fill="var(--color-tone-1)"></rect><rect x="0.172974" y="14" width="20" height="3" rx="1.5" fill="var(--color-tone-1)"></rect></svg></button>
def login_nyt(driver_instance):
    # # Click Setting button
    # setting_button = driver_instance.find_element(By.CLASS_NAME, 'AppHeader-module_icon__qLz07')
    # setting_button.click()
    # print("Clicking Setting button")
    # time.sleep(1)
    # # Click Login Button
    # # <a href="https://myaccount.nytimes.com/auth/enter-email?response_type=cookie&amp;client_id=games&amp;application=nyt-lires&amp;redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fgames%2Fwordle%2Findex.html" role="button" class="NavAccount-module_loginButton__p4LNv" data-track-label="log-in-nav">Log In</a>
    # login_button = driver_instance.find_element(By.CLASS_NAME, 'NavAccount-module_loginButton__p4LNv')
    # login_button.click()
    # print("Clicking Login button")
    # time.sleep(2)=nyt-lires&amp;redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fgames%2Fwordle%2Findex.html
    # Click Login Button
    # <a href="https://myaccount.nytimes.com/auth/enter-email?response_type=cookie&amp;client_id=games&amp;application" role="button" class="NavAccount-module_loginButton__p4LNv" data-track-label="log-in-nav">Log In</a>
    #< a class ="Welcome-module_button__ZG0Zh Welcome-module_secondary__fv3cc" href="https://myaccount.nytimes.com/auth/enter-email?response_type=cookie&amp;client_id=games&amp;application=nyt-lires&amp;redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fgames%2Fwordle%2Findex.html" > Log in < / a >
    print("Trying to Login")
    time.sleep(3)
    login_button = driver_instance.find_element(By.CLASS_NAME, 'Welcome-module_button__ZG0Zh')
    login_button.click()
    print("Clicking Login button")
    time.sleep(5)
    # Enter Email
    # email_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="Play"]')
    # email_button.click()
    # print("Clicking Play button")
    NYT_EMAIL = os.environ.get('NYT_LOGIN')
    type_word(driver_instance, NYT_EMAIL)
    continue_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="submit-email"]')
    continue_button.click()
    print("Clicking Continue button")
    time.sleep(1)
    NYT_PASS = os.environ.get('NYT_PASS')
    type_word(driver_instance, NYT_PASS)
    # final Login Button
    final_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]')
    final_button.click()
    print("Clicking Final button")
    return
driver = webdriver.Safari()

url = "https://www.nytimes.com/games/wordle/index.html?register=email&auth=register-email"
driver.get(url)
# Find the button by its data-testid attribute

#play_button = driver.find_element_by_css_selector('[data-testid="Play"]')
# Optional Log in
LOGIN = 0
if LOGIN:
    print("Login option selected")
    login_nyt(driver)
    # Click the Play button
    click_play(driver)
    time.sleep(2)
    # Close Pop up
    goaway_popup(driver)
    time.sleep(2)
else:
    print("Non login option selected")
    # Click the Play button
    click_play(driver)
    time.sleep(2)
    # Close Pop up
    goaway_popup(driver)
    time.sleep(2)



all_guesses = play_wordle_bot_2(driver)
print(all_guesses)
EmailNotifyRun(all_guesses)

time.sleep(5)

driver.quit()
