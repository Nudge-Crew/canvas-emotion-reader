from werkzeug.datastructures import MultiDict
from app.readers.emotionReader import call_emotion_api
from app.readers.pdfReader import reader
import canvas_api_caller as canvas
import json
from flask import jsonify, request


# Add "self" parameter when working with Google Cloud.
# @app.route('/emotion', methods=['GET'])
def emotion(request):
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': '*'
    }

    if request.method == 'OPTIONS':
        return '', 204, headers

    params = request.args
    access_token = request.headers.get('X-Canvas-Authorization')
    response = call_canvas(access_token, params)

    response_message = response['message']
    response_submission_type = response_message['submission_type']

    if response_submission_type == 'online_text_entry':
        content = call_emotion_api(response_message['body'])
    elif response_submission_type == 'online_upload':
        attachments = response_message['attachments']
        content = read_attachments(attachments)
    else:
        return jsonify({
            "error": f"Filetype: {response_submission_type} is not supported"
        })

    return jsonify(content), 200, headers


def call_canvas(access_token, params):
    access_token = access_token

    course_id = params.get('course_id')
    assignment_id = params.get('assignment_id')
    submission_id = params.get('submission_id')
    endpoint = f"courses/{course_id}/assignments/{assignment_id}/submissions/{submission_id}"

    json_response = canvas.call(access_token, endpoint)
    response = json.loads(json_response)

    return response


def read_attachments(attachments):
    content = MultiDict()

    for a in attachments:
        url = a['url']
        filename = a['filename']

        if filename.endswith('.pdf'):
            content.add(filename, call_emotion_api(reader(url)))

    return content
