import os
import slack
import time
from decouple import config
import requests
import urllib
import tempfile
from datetime import date
#import sys
#sys.path.append(os.getcwd())

import io
import json

from Enums.reply_enum import ReplyType
import IM.IMManager as manager

SLACK_TOKEN = config('SLACK_TOKEN')
BOT_SLACK_NAME = config('BOT_SLACK_NAME')
BOT_SLACK_ID = config('BOT_SLACK_ID')
rtm_client = slack.RTMClient(token=SLACK_TOKEN)
session_r = requests.Session()
#session_r.headers.update({f"Authorization: Bearer {SLACK_TOKEN}"})

@slack.RTMClient.run_on(event='message')
def receive_message(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    msg = data.get('text', [])
    chat_id = data.get('channel')
    user_id = data.get('user')
    user_name = data.get('username')
    '''
    print('------')    
    print('PAYLOAD')
    print('------')
    print(payload)
    print('------')
    print('DATA')
    print('------')
    print(data)
    print('------------------------------------')
    print('PayLoad')
    print('------------------------------------')
    for i, j in payload.items():
        print(i, j)
    print('------------------------------------')
    print('Data')
    print('------------------------------------')
    for i, j in data.items():
        print (i, "\t \t \t", j)
    '''
    print(user_id, " = ", BOT_SLACK_ID)
    print(user_name, " = ", BOT_SLACK_NAME)
    if user_id != BOT_SLACK_ID and user_name != BOT_SLACK_NAME: #'subtype' not in data: #'user' in data
        if 'files' in data: 
            return receive_file(data.get('files')[0], chat_id, user_id, web_client)
        if isinstance(msg, str) and msg != "":
            reply, reply_type = manager.handle_message(msg, chat_id, False)
            channel_id = data['channel']
            #thread_ts = data['ts'] used for replying directly
            #print(data['user'])
            handle_message(web_client, channel_id, reply, reply_type)

#@slack.RTMClient.run_on(event='file_share')
def receive_file(file, chat_id, user_id, web_client):
    print('------')
    print('FILE')
    print('------')
    print(file)
    file_url = file.get('url_private')
    print(file_url)
    file_content = requests.get(file_url, headers={"Authorization": f"Bearer {SLACK_TOKEN}"})
    #file_content = urllib.request.urlopen(file_url)
    #file_content = file_content.read().decode('utf-8')
    #_, tmp_file = tempfile.mkstemp()
    #open(tmp_file, 'wb').write(file.content)
    user = file.get('username')
    name = user if user != '' else user_id
    file_i = {"name": file.get('name'),
              "file": file_content,
              "user": name,
              "upload_date": date.today(),
              "filter": False,
              "size": file.get('size'),
              "type": file.get('name').split('.')[-1],
              "chat_id": str(chat_id)}
    reply, reply_type = manager.handle_message(file_i, chat_id, True)
    handle_message(web_client, chat_id, reply, reply_type)


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
    message = message.replace("<b>", "*").replace("</b>", "*")
    web_client.chat_postMessage(
        channel=channel_id,
        text=message,
        parse="html",
        username=BOT_SLACK_NAME
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

