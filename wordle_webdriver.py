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

def goaway_popup(driver_instance):
    close_button = driver_instance.find_element(By.CLASS_NAME, 'Modal-module_closeIcon__TcEKb')
    #driver_instance.find_element(By.CSS_SELECTOR, '[aria-label="Close"]').click()
    close_button.click()
    print("Clicking close button")

def click_play(driver_instance):
    play_button = driver_instance.find_element(By.CSS_SELECTOR, '[data-testid="Play"]')
    play_button.click()
    print("Clicking Play button")

def EmailNotifyRun(all_guesses):
    num_tries = all_guesses[-1]
    guesses = all_guesses[:-1]

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
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are an incredible poet drawing inspiration from all world-famous poets and poetry. You can make poetry out of anything. I can give you a series of random words and then can you make a poem that includes all of them."},
            {"role": "user", "content": all_words}
        ]
    )
    # Access the first choice from the completion
    gpt_response = completion.choices[0]
    #print(gpt_response)

    # Get the text content of the response
    poem = gpt_response.message.content
    print(poem)
    body += poem

    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    s.sendmail("WordleSolver@gmail.com", storage.GMAIL_USER, msg.as_string())
    s.quit()

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
EmailNotifyRun(all_guesses)

time.sleep(5)

driver.quit()
