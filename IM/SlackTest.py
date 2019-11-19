import os
from decouple import config
import execution
import dialog
import slack

VALET_SLACK_NAME = config('VALET_SLACK_NAME')
VALET_SLACK_TOKEN = config('VALET_SLACK_TOKEN')
VALET_SLACK_ID = config('VALET_SLACK_ID')

valet_slack_client = slack.WebClient(VALET_SLACK_TOKEN)

print(VALET_SLACK_NAME)
print(VALET_SLACK_TOKEN)
is_ok = valet_slack_client.api_call("users.list").get('ok')
print(is_ok)

if(is_ok):
    for user in valet_slack_client.api_call("users.list").get('members'):
        if user.get('name') == VALET_SLACK_NAME:
            print(user.get('id'))

question = ''
answer = ''

while True:
    question = input()
    if question == 'quit':
        break
    print('User:', question)
    answer_from_google = dialog.askGoogle(question)
    reply = execution.findAnswer(answer_from_google)
    print('Bot:', reply)

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']