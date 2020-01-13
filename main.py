import canvas_api_caller as canvas
from flask import Flask, jsonify, request, json
from werkzeug.datastructures import MultiDict
import requests
import os
import io

# PDFMiner
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

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


# Call the canvas API and return the response
def call_canvas(access_token, params):
    access_token = access_token

    course_id = params.get('course_id')
    assignment_id = params.get('assignment_id')
    submission_id = params.get('submission_id')
    endpoint = f"courses/{course_id}/assignments/{assignment_id}/submissions/{submission_id}"

    json_response = canvas.call(access_token, endpoint)
    response = json.loads(json_response)

    return response


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


# Read an attachment from the 'attachments' key in a canvas assignment response.
# Each element should atleast contain 'filename' and 'url'
def read_attachments(attachments):
    content = MultiDict()

    for a in attachments:
        url = a['url']
        filename = a['filename']

        if filename.endswith('.pdf'):
            content.add(filename, call_emotion_api(reader(url)))

    return content


# Download and read the contents of a PDF through a url.
def reader(url):
    r = requests.get(url)
    data = io.BytesIO(r.content)

    # Create parser object to parse the pdf content
    parser = PDFParser(data)

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser)

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources
    # such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted
    # information into desired format
    # Device to connect to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared
    # resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Initialize the text
    extracted_text = ""

    # Ok now that we have everything to process a pdf document,
    # lets process it page by page
    for page in PDFPage.create_pages(document):
        # As the interpreter processes the page stored in PDFDocument
        # object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested
        # in LTTextBox and LTTextLine
        for lt_obj in layout:
            if (isinstance(lt_obj, LTTextBox) or
                    isinstance(lt_obj, LTTextLine)):
                extracted_text += lt_obj.get_text()

    return extracted_text
