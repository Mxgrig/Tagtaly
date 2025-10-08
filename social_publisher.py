# social_publisher.py
import requests
import os
from datetime import datetime

BUFFER_API_TOKEN = os.getenv('BUFFER_TOKEN')

def post_to_buffer(image_path, caption):
    """Post to Buffer which then distributes to all your social accounts"""

    # First, upload image
    files = {'media': open(image_path, 'rb')}
    upload_response = requests.post(
        'https://api.bufferapp.com/1/uploads/create.json',
        files=files,
        data={'access_token': BUFFER_API_TOKEN}
    )

    media_url = upload_response.json()['url']

    # Then create post
    post_data = {
        'access_token': BUFFER_API_TOKEN,
        'profile_ids': ['YOUR_PROFILE_IDS'],  # Get from Buffer
        'text': caption,
        'media': {'photo': media_url}
    }

    response = requests.post(
        'https://api.bufferapp.com/1/updates/create.json',
        data=post_data
    )

    return response.json()
