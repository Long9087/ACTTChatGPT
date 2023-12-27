from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import win32clipboard

# Constants
BATCH_FILE_PATH = 'OpenDebugerChrome.bat'
CHAT_URL = 'https://chat.openai.com'
CHROMEDRIVER_PATH = 'chromedriver-win64/chromedriver.exe'
ASK_FOR_GPT_WORK_FILE = 'FirstChatGPT.txt'

# Set the URL of the ChatGPT website
service = Service(executable_path=CHROMEDRIVER_PATH)
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8989")

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def check_clipboard():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            return win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        else:
            return None
    finally:
        win32clipboard.CloseClipboard()


def initialize_driver():
    subprocess.call(BATCH_FILE_PATH, shell=True)
    print("Opening GPT on chrome done!")
    return webdriver.Chrome(service=service, options=chrome_options, keep_alive=True)


def send_message(driver, message):
    print("Send message to GPT")
    chat_input = driver.find_element(By.ID, 'prompt-textarea')
    chat_input.send_keys(message + Keys.ENTER)
    print("Send message to GPT done!!")


if __name__ == "__main__":
    driver = initialize_driver()

    try:
        driver.get(CHAT_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))

        ASK_FOR_GPT_WORK = read_text_from_file(ASK_FOR_GPT_WORK_FILE)
        send_message(driver, ASK_FOR_GPT_WORK)

        previous_clipboard_content = check_clipboard()

        while True:
            current_clipboard_content = check_clipboard()

            if current_clipboard_content and current_clipboard_content != previous_clipboard_content:
                send_message(driver, current_clipboard_content.replace('\n', ' ').replace('\r', ''))
                previous_clipboard_content = current_clipboard_content

            time.sleep(0.5)

    finally:
        driver.quit()
