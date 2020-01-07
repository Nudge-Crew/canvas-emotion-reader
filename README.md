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
def canvas_api():
```

to

```python
def canvas_api(self):
```

## Run Flask
set Environmental Variable `CANVAS_BASE_URL` to the canvas api environment e.g `https://fhict.test.instructure.com/api/v1/`
In order to run flask, you just need to execute `flask run`.

# Endpoints
The only endpoint this function has is `/canvas_api`, here some parameters are expected.

Headers:
* Authorization - Reserved for Authorization headers for external use such as Google Functions or internal authentication.
* X-Canvas-Authorization - Canvas Authorization header / Access Token in Bearer format, as we need access to your Canvas courses.

Parameters;
* Endpoint - Contains the endpoint to the canvas API url after `https://fhict.instructure.com/api/v1/`.
* Canvas related parameters - Parameters expected by canvas itself such as `student_id`.

This should work with most (if not all) canvas endpoints (GET) that use basic parameters.

## Examples
##### Without extra parameters
```json
GET { 
  "endpoint": "/canvas_api",
  "headers": {
    "X-Canvas-Authorization": "Bearer {Canvas_Access_Token}"
  },
  "query": {
    "endpoint": "courses",
  }
}
```

##### With extra parameters

Query Parameters expected by Canvas API are also expected as a query parameter in this endpoint

```json
GET { 
  "endpoint": "/canvas_api",
  "headers": {
    "X-Canvas-Authorization": "Bearer {Canvas_Access_Token}"
  },
  "query": {
    "endpoint": "courses/5034/gradebook_history/days",
    "student_id": "9047"
  }
}
```

##### With Secured Google Cloud Functions or external Authentication

The `Authorization` token is used for Authorization from e.g Google Cloud Functions.

```json
GET { 
  "endpoint": "/canvas_api",
  "headers": {
    "Authorization": "Bearer {Authorization_Token}",
    "X-Canvas-Authorization": "Bearer {Canvas_Access_Token}"
  },
  "query": {
    "endpoint": "courses/5034/gradebook_history/days",
    "student_id": "9047"
  }
}
```
