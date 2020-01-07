import canvas_api_caller as canvas
from flask import Flask, jsonify, request, json
from werkzeug.datastructures import MultiDict

app = Flask(__name__)


# Add "self" parameter when working with Google Cloud.
@app.route('/canvas_api', methods=['GET'])
def canvas_api():
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
    query_params = request.args
    endpoint = query_params.get('endpoint')
    array_params = MultiDict()

    for k in query_params.keys():
        if k != 'endpoint':
            array_params.add(k, query_params.get(k))

    access_token = access_token.replace('Bearer ', '')

    json_response = canvas.call(access_token, endpoint, array_params)
    decoded_response = json.loads(json_response)
    return jsonify({
        "message": decoded_response['message']
    }), decoded_response['code'], headers
