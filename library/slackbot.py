import slack
import os
from pathlib import Path
from dotenv import load_dotenv


def send_message(config, text):
    env_path = config["slack_token_envfile"]
    load_dotenv(dotenv_path=env_path)
    
    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#aqpi', text=text)

    