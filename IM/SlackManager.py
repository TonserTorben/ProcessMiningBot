import os
import sys
sys.path.append(os.getcwd())
import slack
import time
from decouple import config

from IM.reply_enum import ReplyType
import IM.IMManager as manager

SLACK_TOKEN = config('SLACK_TOKEN')
rtm_client = slack.RTMClient(token=SLACK_TOKEN)

@slack.RTMClient.run_on(event='message')
def say_somethin(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    question = data.get('text', [])
    if 'user' in data: 
        print(payload)
        print('------')
        print(data)
    if isinstance(question, str) and question != "" and 'user' in data:
        # Should be called via IMManager
        #google_answer = dialog.askGoogle(question)
        #answer = execution.findAnswer(google_answer)
        reply, reply_type = manager.get_intention(question)
        channel_id = data['channel']
        thread_ts = data['ts']
        print(data['user'])
        if(reply_type == ReplyType.text):
            web_client.chat_postMessage(
                channel=channel_id,
                text= reply,
                #thread_ts=thread_ts
            )
        elif(reply_type == ReplyType.photo):
            web_client.chat_postMessage(
                channel=channel_id,
                files = reply
            )

def start_bot():
    rtm_client.start()

