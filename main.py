import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import asyncio
from EdgeGPT import Chatbot
import json
from pynput import mouse
import pyperclip

print("Place your cursor right before the first letter of the text box.")

scan = True

def on_click(x, y, button, pressed):
    global scan, a, b
    if pressed:
        scan = False
        print("Successfully registered cursor coordinate!")
        a, b = pyautogui.position()
        return False
    
listener = mouse.Listener(on_click=on_click)
listener.start()

while scan:
    x, y = pyautogui.position()
    print(f'X: {x} Y: {y}', end='\r')

intro = "Hello there, I'm ScholarScribe, your personalized AI tool designed to effortlessly write your IB assessments for you."
print(intro)

with open('./cookies.json', 'r') as f:
    cookies = json.load(f)

async def main(prompt):
    bot = await Chatbot.create(cookies=cookies)
    data = await bot.ask(prompt=prompt)
    messages = data['item']['messages']
    bot_text = messages[1]['text']
    print(bot_text)
    await bot.close()
    return bot_text

text = ""
n = ""

time.sleep(3)
essay_type = input("What do you wish to write: \n1.) English IO \n2.) ToK Essay \n3.) Physics IA\nYour answer: ")
if (essay_type!="" and essay_type.isnumeric()):
    if (essay_type == "1"):
        n = "English IO"
    elif (essay_type == "2"):
        n = "ToK Essay"
    elif (essay_type == "3"):
        n = "Physics IA"
    else:
        print("Error, that is not an option !")
        sys.exit(1)

    task = input("Provide the parameters for the essay: ")

prompt = "I am seeking your assistance in creating a sample IB essay on "+n+". Although I understand that you cannot write complete essays, I believe your guidance and insights would greatly benefit me. The essay should explore "+task+" and its significance in today's society. Please provide a well-structured framework, including historical context, influential figures/events, relevant theories, and real-world examples. Your expertise will enhance my understanding and improve my writing skills."

screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouse = pyautogui.position()

def paraphraser():
    # Create a new instance of the Google Chrome driver
    driver = webdriver.Chrome(executable_path=r'C:\Program Files\Google\Chrome\Application')

    # Go to the paraphraser.io webpage
    driver.get('https://www.paraphraser.io/')

    # Find the text box and input some text
    text_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//textarea[@id="inputText"]')))
    text_box.clear()
    text_box.send_keys("Hello, world!")

    # Find and click the paraphrase button
    paraphrase_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-paraphrase"]')))
    paraphrase_button.click()

    # Wait for the paraphrased text to appear and then copy it
    paraphrased_text = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//textarea[@id="outputText"]'))).get_attribute('value')

    print(paraphrased_text)

    # Close the browser
    driver.quit()

def write(x, y, text):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.write(text)

text = asyncio.run(main(prompt=prompt))
write(text=text, x=a, y=b)

if __name__ == "__main__":
    asyncio.run(main())