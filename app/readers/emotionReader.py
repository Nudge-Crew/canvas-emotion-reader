import requests
import os


# Get Emotions from EmotionAPI by content
def call_emotion_api(content):
    default_emotion_api_url = 'https://us-central1-school-230709.cloudfunctions.net/translate_data'

    data = {
        "data": content
    }

    headers = {
        'Content-Type': 'application/json'
    }

    url = requests.post(
        os.environ.get('EMOTION_API_URL', default_emotion_api_url),
        json=data,
        headers=headers
    )

    if url.status_code is 500:
        return {
            "error": "Unable to read emotions from text"
        }

    return url.json()
