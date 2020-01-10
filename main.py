import canvas_api_caller as canvas
from flask import Flask, jsonify, request, json
import urllib3
from tika import parser
from werkzeug.datastructures import MultiDict
import requests
import os

app = Flask(__name__)


# Add "self" parameter when working with Google Cloud.
@app.route('/emotion', methods=['GET'])
def emotion():
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }

    if request.method == 'OPTIONS':
        return ('', 204, headers)

    access_token = request.headers.get('X-Canvas-Authorization')

    params = request.args
    course_id = params.get('course_id')
    assignment_id = params.get('assignment_id')
    submission_id = params.get('submission_id')
    endpoint = f"courses/{course_id}/assignments/{assignment_id}/submissions/{submission_id}"

    json_response = canvas.call(access_token, endpoint)
    response = json.loads(json_response)
    attachments = response['message']['attachments']

    content = read_attachments(attachments)

    return jsonify(content)

# Get Emotions from EmotionAPI by content
def call_emotion_api(content):
    default_emotion_api_url = 'https://us-central1-school-230709.cloudfunctions.net/translate_data'

    decoded_content = bytes(content, "utf-8").decode("unicode_escape").encode('latin1').decode('utf8')

    data = {
        "data": decoded_content
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    url = requests.post(
        os.environ.get('EMOTION_API_URL', default_emotion_api_url),
        json=data,
        headers=headers
    )

    if url.status_code is not 200:
        return {
            "error": "Unable to read emotions from text"
        }

    return url.json()

# Get emotions from emotionAPI
def read_attachments(attachments):
    content = MultiDict()

    for a in attachments:
        content.add(a['filename'], call_emotion_api(reader(a['url'])))

    return content

# Read a PDF and return content
def reader(url):
    poolManager = urllib3.PoolManager()
    response = poolManager.request('GET', url)
    data = response.data

    raw = parser.from_buffer(data)

    return raw['content']
