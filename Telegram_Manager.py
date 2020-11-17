import json
import requests
import urllib

filename = 'telegramID.txt'

with open(filename) as f:
    IDS = f.read().splitlines()

chat_id = str(IDS[0])
TOKEN = str(IDS[1])
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

class Message_Receiver:
    def __init__(self, text, last_update_id):
        self.text = text
        self.last_update_id = last_update_id


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def get_response(Octavius_Receiver):
    print("Entering get response")
    updates = get_updates(Octavius_Receiver.last_update_id)
    print(f"Update ID = {Octavius_Receiver.last_update_id}")
    if len(updates["result"]) > 0:
        print("Update found")
        Octavius_Receiver.last_update_id = get_last_update_id(updates) + 1
        print(f"Update ID = {Octavius_Receiver.last_update_id}")
        Octavius_Receiver.text = updates["result"][0]["message"]["text"]
        print(f'Received update - {updates["result"][0]["message"]["text"]}')
    else:
        Octavius_Receiver.text = ''
    print(f"Leaving get response with text: {Octavius_Receiver.text}")
    return Octavius_Receiver
