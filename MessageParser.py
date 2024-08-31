from API.SlackAPI import SlackAPI
from parser.SlackParser import SlackParser

import argparse
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
documents_folder = os.path.join(current_dir, 'Documents')

if __name__ == "__main__":
    ## Parse command line arguments
    parser = argparse.ArgumentParser(description="Retrieve messages from Slack or Microsoft Teams")
    parser.add_argument("msgProvider", type=str, help="The messaging provider to use (slack/teams)")
    parser.add_argument("channel_id", type=str, help="The channel ID to retrieve messages from")

    ## Parse arguments
    args = parser.parse_args()
    msgProvider = args.msgProvider
    channel_id = args.channel_id

    ## CLI - ask whether user wants slack or microsoft teams
    # msgProvider = input("Do you want to use Slack or Microsoft Teams? (slack/teams): ").strip().lower()

    # if slack
    if msgProvider == "slack":
        slack = SlackAPI()
        messages = slack.fetch_channel_history(channel_id)
    # if teams
    elif msgProvider == "teams":
        print("Currently not implemented")
        # TeamsAPI.retrieveMessage("")
    else:
        raise ValueError("Invalid messaging provider. Please use 'slack' or 'teams'.")
    
    parser = SlackParser()
    channel_name = slack.fetch_channel_name(channel_id)
    parser.parse_conversation(messages, os.path.join(documents_folder, f'{channel_name}_chunks.json'))