from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo

# Replace these with your own API ID, API HASH, and phone number
api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = 'your_phone_number'

with TelegramClient('session_name', api_id, api_hash) as client:
    client.connect()

    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Enter the code: '))

    # Replace 'group_username' with the username of the group you want to crawl
    group_entity = client.get_entity('group_username')

    # Get the messages in the group that contain videos
    videos = client.get_messages(group_entity, filter=InputMessagesFilterVideo)

    # Download each video
    for video in videos:
      client.download_media(video)
      
