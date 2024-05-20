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
    
    # Run the FastAPI app using uvicorn
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
