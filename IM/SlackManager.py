import os
import sys
sys.path.append(os.getcwd())
import slack
import time
from decouple import config

import io
import json

from Enums.reply_enum import ReplyType
import IM.IMManager as manager

SLACK_TOKEN = config('SLACK_TOKEN')
rtm_client = slack.RTMClient(token=SLACK_TOKEN)

@slack.RTMClient.run_on(event='message')
def say_somethin(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    question = data.get('text', [])
    print(payload)
    print('------')
    print(data)
    if isinstance(question, str) and question != "" and 'subtype' not in data: #'user' in data
        reply, reply_type = manager.get_intention(question)
        channel_id = data['channel']
        #thread_ts = data['ts'] used for replying directly
        #print(data['user'])
        handle_message(web_client, channel_id, reply, reply_type)

def handle_message(web_client, channel_id, reply, reply_type):
    if reply_type == ReplyType.multi:
        for i, j in reply:
            handle_message(web_client, channel_id, i, j)
    elif reply_type == ReplyType.text:
            send_message(web_client, channel_id, reply)
    elif reply_type == ReplyType.photo:
        send_photo(web_client, channel_id, reply)
    elif reply_type == ReplyType.video:
        send_video(web_client, channel_id, reply)

def send_message(web_client, channel_id, message):
    web_client.chat_postMessage(
        channel=channel_id,
        text=message
    )

def send_photo(web_client, channel_id, photo):
    with open(photo, 'rb') as pho:
        r = web_client.api_call("files.upload", files={
            'file': pho,
        }, data={
            'channels': channel_id,
            'filename': 'mining_result.png',
            'title': 'work in progress',
            'initial_comment': 'also work in progress'
        })
        assert r.status_code == 200

def send_video(web_client, channel_id, video):
    pass

def start_bot():
    rtm_client.start()

