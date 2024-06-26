from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient
from starlette.requests import Request as StarletteRequest
from starlette.datastructures import Headers, URL

app = FastAPI()

# Route for demonstration
@app.get("/")
async def read_root():
    return {"message": "Hello, world"}

# Function to create and patch a Request object
def create_request_with_app(app: FastAPI, path: str = "/") -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "root_path": "",
        "scheme": "http",
        "query_string": b"",
        "headers": Headers({}).raw,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }
    starlette_request = StarletteRequest(scope)
    starlette_request._app = app  # Manually set the app attribute
    return Request(starlette_request.scope, receive=starlette_request.receive)

# Custom endpoint to demonstrate patched request usage
@app.get("/custom")
async def custom_endpoint(request: Request):
    app_instance = request.app
    return {"app_title": app_instance.title}

# Example usage of patched request
if __name__ == "__main__":
    # Creating a TestClient for the app
    client = TestClient(app)

    # Creating a custom request with the app patched
    custom_request = create_request_with_app(app, path="/custom")

    # Manually invoking the custom endpoint
    response = custom_request.app.router.handle(custom_request.scope)
    
    # Printing the response for demonstration
    response_body = client.get("/custom").json()
    print(response_body)  # Should print the app title or any custom data
    # testing again
    # Run the FastAPI app using uvicorn
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


    import os

def lambda_handler(event, context):
    # The path to the mounted EFS
    efs_path = '/mnt/efs'
    
    try:
        # Ensure the EFS mount point exists
        if not os.path.exists(efs_path):
            raise Exception(f"The EFS path {efs_path} does not exist.")
        
        # List all files in the EFS directory
        files = os.listdir(efs_path)
        
        return {
            'statusCode': 200,
            'body': {
                'files': files
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }


import os

def lambda_handler(event, context):
    # The path to the mounted EFS
    efs_path = '/mnt/efs'
    
    # The name of the text file to create
    file_name = 'sample.txt'
    
    # The full path of the text file
    file_path = os.path.join(efs_path, file_name)
    
    # The content to write to the text file
    content = "Hello, this is a sample text file stored on EFS."

    try:
        # Ensure the EFS mount point exists
        if not os.path.exists(efs_path):
            raise Exception(f"The EFS path {efs_path} does not exist.")
        
        # Write the content to the text file
        with open(file_path, 'w') as file:
            file.write(content)
        
        return {
            'statusCode': 200,
            'body': f"File '{file_name}' created successfully at {efs_path}."
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

from datetime import datetime

def validate_date_format(date_str):
    try:
        # Parse the date string with the format that includes microseconds
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        # If parsing with microseconds fails, try without microseconds
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # If both parsing attempts fail, the format is incorrect
            return False
        
        # If parsing succeeds without microseconds, check if it matches the desired format
        return date_str == date_obj.strftime("%Y-%m-%d %H:%M:%S")

    # If parsing succeeds with microseconds, the format is incorrect
    return False


import requests
import json

def call_aws_api(api_url, bearer_token, payload):
    try:
        # Define headers including the bearer token and content type
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        # Make the API call with headers and payload
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Print out the data
        print(data)
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Example usage
api_url = "https://your-api-id.execute-api.region.amazonaws.com/your-stage/your-resource"
bearer_token = "your_bearer_token_here"
payload = {
    "key1": "value1",
    "key2": "value2"
}
call_aws_api(api_url, bearer_token, payload)
