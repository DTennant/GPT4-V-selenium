# GPT4-V driver


### 1. Installation

```shell
pip install selenium
```

1. Check your Chrome version: Before downloading ChromeDriver, you need to know which version of Google Chrome you have installed, as ChromeDriver's version must match it. You can find your Chrome version by navigating to Menu > Help > About Google Chrome in the browser.
2. Visit the ChromeDriver download page: Go to the ChromeDriver download page, which is hosted on the Chromium project's site: https://sites.google.com/chromium.org/driver/

```shell
# Replace 'XX' with the correct Chrome version you are using.
wget https://chromedriver.storage.googleapis.com/XX.X.XXXX.X/chromedriver_linux64.zip

# Unzip the downloaded file.
unzip chromedriver_linux64.zip

# Move the ChromeDriver to /usr/local/bin/ or any other directory in your PATH.
sudo mv chromedriver /usr/local/bin/
```

For Windows, you would download the .zip file, extract it, and move chromedriver.exe to a directory in your PATH.


### 2. Usage

1. Create an instance of the ChatGPTAutomation class with the path to your ChromeDriver.
```python
from chatgpt_automation import ChatGPTAutomation

bot = ChatGPTAutomation(chrome_driver_path='/path/to/chromedriver')
```

2. The browser will launch and wait for human verification. Follow the instructions printed in the console. Remember to turn-off chat history if you don't want future ChatGPT to be trained on your test set.

3. If needed, use the `upload_image` method to upload images. Always upload the image before send prompts.
```python
bot.upload_image('/path/to/image.png')
```
4. Use the `send_prompt_to_chatgpt` method to send a message.
```python
bot.send_prompt_to_chatgpt('Hello, ChatGPT!')
```
5. Use `save_conversation` method to save conversation to a file.
```python
bot.save_conversation('conversation.txt')
```
6. Complete usage example:
```python
import os
from tqdm import tqdm
import pandas as pd
from driver import ChatGPTAutomation

chrome_driver_path = "/usr/local/bin/chromedriver"
chatgpt = ChatGPTAutomation(chrome_driver_path)

df = pd.read_csv('C-VQA_GPT4V_300.csv')
base_path = '/Users/tennant/Desktop/cfvqa/C-VQA_GPT4V_images/'
file_name = "cvqa_conversation.txt"

for i, row in tqdm(df.iterrows(), total=len(df)):
    path = os.path.join(base_path, row.img_path)
    prompt = row['new query']

    chatgpt.upload_image(path)
    chatgpt.send_prompt_to_chatgpt(prompt)

    response = chatgpt.return_last_response()
    print(response)

    chatgpt.save_conversation(file_name)
    chatgpt.clear_chat()

chatgpt.quit()

```

