import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('SLACK_API_TOKEN')
logger = logging.getLogger(__name__)

cached_user_id = {}

class SlackAPI:
    def __init__(self):
        pass

    def fetch_username(self, user_id):
        if user_id in cached_user_id:
            return cached_user_id[user_id]
        url = 'https://slack.com/api/users.info'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'user': user_id}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data['ok']:
            cached_user_id[user_id] = data['user']['name']
            return cached_user_id[user_id]
        else:
            print("Error fetching username:", data.get('error'))
            return None
        
    def fetch_thread_replies(self, channel_id, thread_ts):
        url = 'https://slack.com/api/conversations.replies'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'channel': channel_id, 'ts': thread_ts}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data['ok']:
            # Convert user_id to username
            for message in data['messages']:
                user_id = message.get('user')
                if not user_id:
                    continue
                message['username'] = self.fetch_username(user_id)
            return data['messages']
        else:
            print("Error fetching thread replies:", data.get('error'))
            return None

    def fetch_channel_history(self, channel_id):
        url = 'https://slack.com/api/conversations.history'
        headers = {'Authorization': f'Bearer {token}'}
        cursor = None
        all_messages = []

        for _ in range(4): # Fetch up to 4 pages of messages
            params = {'channel': channel_id}
            if cursor:
                params['cursor'] = cursor

            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            if data['ok']:
                for message in data['messages']:
                    user_id = message.get('user')
                    if not user_id:
                        continue

                    message['username'] = self.fetch_username(user_id)
                    if 'thread_ts' in message:
                        thread_replies = self.fetch_thread_replies(channel_id, message['thread_ts'])
                        message['thread_replies'] = thread_replies
                    all_messages.append(message)

                cursor = data.get('response_metadata', {}).get('next_cursor')
                if not cursor:
                    break
            else:
                print("Error fetching messages:", data.get('error'))
                break

        return all_messages
    
    def fetch_channel_name(self, channel_id):
        url = 'https://slack.com/api/conversations.info'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'channel': channel_id}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if data['ok']:
            return data['channel']['name']
        else:
            print("Error fetching channel name:", data.get('error'))
            return None