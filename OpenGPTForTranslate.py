from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import win32clipboard

# Constants
batch_file_path = 'OpenDebugerChrome.bat'
CHAT_URL = 'https://chat.openai.com'
CHROMEDRIVER_PATH = 'chromedriver-win64/chromedriver.exe'
ASK_FOR_GPT_WORK = "I'm playing a video game, I need you to work as a typo corrector and translator to Vietnamese and I need you to show both the corrected text and translated text and not put them in any code style in your respone!"

# Set the URL of the ChatGPT website
service = Service(executable_path= CHROMEDRIVER_PATH)
chrome_options = Options()
print("Add the protocol of debuggerAddress")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8989")

def check_clipboard():
    # Open the clipboard
    win32clipboard.OpenClipboard()
    
    try:
        # Check if the clipboard contains text
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            # Get the text data from the clipboard
            clipboard_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            return clipboard_data
        else:
            return None
    finally:
        # Close the clipboard
        win32clipboard.CloseClipboard()

if __name__ == "__main__":

    subprocess.call(batch_file_path, shell=True)
    print("Opening GPT on chrome done!")

    driver = webdriver.Chrome(service=service, options = chrome_options,keep_alive=True)
    # Open the ChatGPT website
    driver.get(CHAT_URL)
    # Wait for the page to load (you might need to adjust the sleep duration)
    time.sleep(2)

    # Interact with the chat interface (replace with appropriate element locators)
    print("Send mesege to GPT")
    chat_input = driver.find_element(By.ID,'prompt-textarea')
    chat_input.send_keys(ASK_FOR_GPT_WORK + Keys.ENTER)
    print("Send mesege to GPT done!!")

    # Initialize the variable to keep track of the clipboard content
    previous_clipboard_content = check_clipboard()

    while True:
        # Check the clipboard for changes
        current_clipboard_content = check_clipboard()

        # If there is new content, perform the paste and Enter key press actions
        if current_clipboard_content and current_clipboard_content != previous_clipboard_content:
            print("Send mesege to GPT")
            chat_input = driver.find_element(By.ID,'prompt-textarea')
            chat_input.send_keys(current_clipboard_content.replace('\n', ' ').replace('\r', '') + Keys.ENTER)
            print("Send mesege to GPT done!!")
            previous_clipboard_content = current_clipboard_content

        # Add a delay to avoid continuously checking the clipboard (adjust as needed)
        time.sleep(0.5)