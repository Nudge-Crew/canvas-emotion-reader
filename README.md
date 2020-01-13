# Installation Guide
## Virtual Environment
### Linux and MacOS

The venv folder contains all dependencies which are needed to run this project. To enter the venv virtual environment use:

``` source venv/bin/activate ```

If this is the first time running or if anything in the requirements has changed use:

``` virtualenv venv && source venv/bin/activate && pip install -r requirements.txt ```

after installing a new package use: 

``` pip freeze > requirements.txt ```

to update the requirments folder

### Windows
The venv folder contains all dependencies which are needed to run this project. To enter the venv virtual environment use:

``` source venv/bin/activate ```

If this is the first time running or if anything in the requirements has changed use:

``` virtualenv venv && source venv/Scripts/activate && pip install -r requirements.txt ```

after installing a new package use: 

``` pip freeze > requirements.txt ```

to update the requirments folder

#### Important Note
Make sure to have python37 and python37\Scripts added in your environmental path.
Else command such as ```virtualenv venv``` may not work.

Example environmental variables:

![Environmental Variables](https://i.imgur.com/2u3va11.png "Environmental Variables")

## Google Cloud Functions
Google cloud functions requires an extra parameter named `self` in the `canvas_api` method.
When using Google Cloud Functions, in `main.py` change:
```python
def emotion():
```

to

```python
def emotion(self):
```

## Run Flask
set Environmental Variable `CANVAS_BASE_URL` to the canvas api environment e.g `https://fhict.test.instructure.com/api/v1/`
Also set environmental variable `EMOTION_API_URL` to the emotion API endpoint e.g `https://us-central1-school-230709.cloudfunctions.net/translate_data`
In order to run flask, you just need to execute `flask run`.

# Endpoints
The only endpoint this function has is `/emotion`, here some parameters are expected.

Headers:
* X-Canvas-Authorization - Canvas Authorization header / Access Token in Bearer format, as we need access to your Canvas courses.

Parameters;
* `course_id` - Contains the Canvas Course the Assignment and Submission is from
* `assignment_id` - Contains the Canvas Assignment the Submission is from
* `submission_id` - Contains a canvas submission of a specific Assignment.

## HTTP Request
```json
GET { 
  "endpoint": "/emotion",
  "headers": {
    "X-Canvas-Authorization": "Bearer {Canvas_Access_Token}"
  },
  "query": {
    "course_id": "{CANVAS_COURSE_ID}", 
    "assignment_id": "{CANVAS_ASSIGNMENT_ID}", 
    "submission_id": "{CANVAS_SUBMISSION_ID}", 
  }
}
```

# Workflow
1. Find the submission from Canvas
2. Download all attachments of a submission
3. Extract content (text) from the PDF files.
4. Pass content to Emotion API
5. Return emotions for each attachment
