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

    # __import__("ipdb").set_trace()
    chatgpt.save_conversation(file_name)
    chatgpt.clear_chat()

chatgpt.quit()

