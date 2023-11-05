import pandas as pd
from driver import ChatGPTAutomation

chrome_driver_path = "/usr/local/bin/chromedriver"
chatgpt = ChatGPTAutomation(chrome_driver_path)

prompt = "What's the error in this message?"
chatgpt.upload_image('/Users/tennant/Desktop/cfvqa/WechatIMG658.jpg')
chatgpt.send_prompt_to_chatgpt(prompt)

response = chatgpt.return_last_response()
print(response)

# __import__("ipdb").set_trace()
file_name = "conversation.txt"
chatgpt.save_conversation(file_name)
chatgpt.clear_chat()

chatgpt.quit()

