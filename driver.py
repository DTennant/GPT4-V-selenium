from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
import time
import socket
import threading
import os



class ChatGPTAutomation:

    def __init__(self, chrome_path, chrome_driver_path):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """

        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = r"https://chat.openai.com"
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver(free_port)
        
        self.images_path = []
        self.num_prompts = 0



    def find_available_port(self):
        """ This function finds and returns an available port number on the local machine by creating a temporary
            socket, binding it to an ephemeral port, and then closing the socket. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]



    def launch_chrome_with_remote_debugging(self, port, url):
        """ Launches a new Chrome instance with remote debugging enabled on the specified port and navigates to the
            provided url """

        def open_chrome():
            # chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir=remote-profile {url}"
            chrome_cmd = f"/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port={port} --user-data-dir=remote-profile --no-first-run {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()



    def setup_webdriver(self, port):
        """  Initializes a Selenium WebDriver instance, connected to an existing Chrome browser
             with remote debugging enabled on the specified port"""

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        service = ChromeService(executable_path=self.chrome_driver_path, )
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver



    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """

        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
        prompt = prompt.replace("'", "\\'")
        js_code = f"""arguments[0].value = '{prompt}';"""
        self.driver.execute_script(js_code, input_box)
        input_box.send_keys(Keys.RETURN)
        input_box.submit()

        if self.num_prompts == len(self.images_path):
            # this prompt do not have images
            self.images_path.append('no image')
        self.num_prompts += 1

        time.sleep(5)

    def upload_image(self, file_path):
        if not self.driver:
            raise Exception('You need to initialize first')
        
        # Find the input element and upload the file
        input_element = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        input_element.send_keys(file_path)
        
        self.images_path.append(file_path)
        
        # Wait until the upload is complete by checking the send button's state
        WebDriverWait(self.driver, timeout=30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="send-button"]:not([disabled])'))
        )
        
    def clear_chat(self, ):
        # XPath to find the link with the specific text and part of the class names provided.
        # Adjust the XPath if necessary to better suit the uniqueness of the element.
        clear_chat_xpath = "//a[contains(@class,'cursor-pointer') and contains(@class,'text-sm') and .//span[text()='Clear chat']]"

        try:
            # Wait for the element to be clickable
            clear_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, clear_chat_xpath))
            )

            # Click the 'Clear chat' button
            clear_button.click()
            print("Chat cleared successfully.")
        except Exception as e:
            print(f"Error clearing chat: {e}")



    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')



    def save_conversation(self, file_name):
        """
        It saves the full chatgpt conversation of the tab open in chrome into a text file, with the following format:
            prompt: ...
            response: ...
            delimiter
            prompt: ...
            response: ...

        :param file_name: name of the file where you want to save
        """

        directory_name = "conversations"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        with open(os.path.join(directory_name, file_name), "a") as file:
            # NOTE: assuming each prompt contains at most one image
            for i in range(0, len(chatgpt_conversation), 2):
                if i // 2 in range(len(self.images_path)):
                    images = self.images_path[i // 2]
                else:
                    images = 'no image'
                file.write(
                    f"image: {images}\n"
                    f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 1].text}"
                    f"\n\n{delimiter}\n\n")



    def return_last_response(self):
        """ :return: the text of the last chatgpt response """

        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        return response_elements[-1].text



    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")



    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()