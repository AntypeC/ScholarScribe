import pyautogui
import time
import sys
import asyncio
from EdgeGPT import Chatbot
import json

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

def write(text):
    pyautogui.moveTo(250, 500)
    pyautogui.click()
    # pyautogui.hotkey('command', 't')
    pyautogui.write(text)

text = asyncio.run(main(prompt=prompt))
write(text=text)

if __name__ == "__main__":
    asyncio.run(main())