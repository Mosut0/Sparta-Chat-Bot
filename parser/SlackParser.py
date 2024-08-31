import json
import re

from API.SlackAPI import SlackAPI

IGNORE = ['channel_join', 'channel_leave', 'channel_topic', 'channel_purpose', 'channel_name', 'channel_archive', 'message_deleted']
UNICODE = {
    "\u2018": "'",
    "\u2019": "'",
    "\u2022": "-",
    "\u201c": "\"",
    "\u201d": "\""
}

class SlackParser:
    def __init__(self):
        self.SlackAPI = SlackAPI()
        pass

    def clean_text(self, text):
        # Remove emojis
        text = re.sub(r':[a-zA-Z0-9_]+:', '', text)
        # Replace user_ids with username
        user_ids = re.findall(r'<@U[a-zA-Z0-9]+>', text)
        for user_id in user_ids:
            username = self.SlackAPI.fetch_username(user_id[2:-1])
            text = text.replace(user_id, username)
        # Replace unicode with ASCII
        for unicode_char, ascii_char in UNICODE.items():
            text = text.replace(unicode_char, ascii_char)
        return text

    def parse_conversation(self, raw_data, output_file):
        filtered_messages = []
        for message in raw_data:
            if 'subtype' in message and message['subtype'] in IGNORE: # Ignore messages that are not user messages
                continue

            filtered_message = {}
            
            if 'thread_ts' in message: # Fetch thread replies
                replies = []
                for reply in message.get('thread_replies'):
                    if 'subtype' in reply and reply['subtype'] in IGNORE:
                        continue
                    replies.append({
                        'username': reply.get('username'), 
                        'text': self.clean_text(reply.get('text'))
                    })

                filtered_message['thread_ts'] = message['thread_ts']
                filtered_message['thread_replies'] = replies            

            filtered_message['username'] = message.get('username')
            filtered_message['text'] = self.clean_text(message.get('text'))
            filtered_message['ts'] = message.get('ts')

            filtered_messages.append(filtered_message)

        with open(output_file, 'w') as json_file:
            json.dump(filtered_messages, json_file, indent=4)
