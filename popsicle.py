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

#!/bin/bash

# Define the error message parameter
error_message="$1"

# Define other parameters for the email
subject="Error Notification"
recipient=""
sender=""
body="An error occurred during the process:\n\n$error_message"

# Send the email using AWS SES
aws ses send-email \
    --from "$sender" \
    --destination "ToAddresses=$recipient" \
    --message "Subject={Data=$subject,Charset=utf-8},Body={Text={Data=$body,Charset=utf-8}}"


# Construct the SQL query to set max_wal_size
        query = sql.SQL("ALTER SYSTEM SET max_wal_size = %s;").format(sql.Identifier(f"{size_gb}GB"))

        # Execute the SQL query
        cur.execute(query, [f"{size_gb}GB"])

        # Reload the configuration to apply changes
        cur.execute("SELECT pg_reload_conf();")


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class PostgresCopyExample {
    public static void main(String[] args) {
        String url = "jdbc:postgresql://localhost:5432/yourdatabase";
        String user = "yourusername";
        String password = "yourpassword";

        // Path to your pipe-delimited file
        String filePath = "/path/to/your/file.txt";

        // SQL COPY command with pipe delimiter
        String copyCommand = "COPY your_table_name FROM ? WITH (FORMAT csv, DELIMITER '|', HEADER true)";

        try (Connection conn = DriverManager.getConnection(url, user, password);
             PreparedStatement pstmt = conn.prepareStatement(copyCommand)) {

            // Set the file path parameter
            pstmt.setString(1, filePath);

            // Execute the COPY command
            pstmt.execute();

            System.out.println("Data imported successfully.");

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
SELECT
    t.relname AS table_name,
    l.locktype,
    l.mode,
    l.granted,
    l.pid,
    a.query,
    a.state
FROM pg_locks l
JOIN pg_class t ON l.relation = t.oid
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE t.relname = 'your_table_name';
import pytest
from unittest.mock import MagicMock
from fastapi import Request
from sqlalchemy.orm import Session
from myapp import ToggleGrid  # Adjust this import to match your project structure

def test_get_toggle_status(mocker):
    # Mock the request and session
    mock_request = MagicMock(spec=Request)
    mock_session = MagicMock(spec=Session)
    
    # Mock the database instance in request object
    mock_db_instance = MagicMock()
    mock_request.app.databaseInstance = {
        "fatr_tggl_stts": {"instance": mock_db_instance}
    }
    
    # Mock the table and column references
    mock_table = MagicMock()
    mock_db_instance.meta = {"fatr_tggl_stts": {"instance": mock_table}}

    # Mock the query and return value
    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.first.return_value = {
        "FATR_STTS_ID": 1,
        "FATR_ID": 123,
        "IS_ON_FL": True,
        "UPDT_BY_USER_ID": "user123",
        "LAST_UPDT_TS": "2024-10-03 12:00:00"
    }
    
    # Create instance of ToggleGrid
    toggle_grid = ToggleGrid(mock_request)

    # Call the get_toggle_status method
    result = toggle_grid.get_toggle_status(mock_session)

    # Assert that the session's query and other methods are called correctly
    mock_session.query.assert_called_once()
    mock_query.order_by.assert_called_once()
    mock_query.first.assert_called_once()

    # Verify the result
    assert result == {
        "FATR_STTS_ID": 1,
        "FATR_ID": 123,
        "IS_ON_FL": True,
        "UPDT_BY_USER_ID": "user123",
        "LAST_UPDT_TS": "2024-10-03 12:00:00"
    }
    
    
    import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;

public class LogFileChecker {
    public static void main(String[] args) throws IOException, InterruptedException {
        File logFile = new File("path/to/your/logfile.log");
        
        String lastLine = null;
        String currentLine;
        int stableCount = 0;
        int requiredStableIterations = 5; // Number of stable iterations to confirm no more data

        while (true) {
            currentLine = readLastLine(logFile);
            if (currentLine != null && currentLine.equals(lastLine)) {
                stableCount++;
                System.out.println("Stable count: " + stableCount);
                if (stableCount >= requiredStableIterations) {
                    System.out.println("No new data has been added to the log file.");
                    break;
                }
            } else {
                stableCount = 0; // Reset if a new line is detected
                lastLine = currentLine;
                System.out.println("New data detected in the log file.");
            }
            // Wait for a few seconds before checking again
            Thread.sleep(3000);
        }
    }

    private static String readLastLine(File file) throws IOException {
        String lastLine = null;
        try (RandomAccessFile randomAccessFile = new RandomAccessFile(file, "r")) {
            long fileLength = randomAccessFile.length() - 1;
            if (fileLength < 0) {
                return null;
            }

            randomAccessFile.seek(fileLength);
            int readByte;
            while ((readByte = randomAccessFile.readByte()) != '\n') {
                fileLength--;
                randomAccessFile.seek(fileLength);
                if (fileLength == 0) {
                    break;
                }
            }

            lastLine = randomAccessFile.readLine();
        }
        return lastLine;
    }
}


import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class LogFileChecker {
    private static String lastLine = null;
    private static int stableCount = 0;
    private static final int REQUIRED_STABLE_ITERATIONS = 5;
    
    public static void main(String[] args) {
        File logFile = new File("path/to/your/logfile.log");
        
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        
        Runnable checkTask = () -> {
            try {
                String currentLine = readLastLine(logFile);
                if (currentLine != null && currentLine.equals(lastLine)) {
                    stableCount++;
                    System.out.println("Stable count: " + stableCount);
                    if (stableCount >= REQUIRED_STABLE_ITERATIONS) {
                        System.out.println("No new data has been added to the log file.");
                        scheduler.shutdown(); // Stop the scheduler once stable
                    }
                } else {
                    stableCount = 0; // Reset if a new line is detected
                    lastLine = currentLine;
                    System.out.println("New data detected in the log file.");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        };
        
        // Schedule the checkTask to run every 3 seconds
        scheduler.scheduleAtFixedRate(checkTask, 0, 3, TimeUnit.SECONDS);
    }

    private static String readLastLine(File file) throws IOException {
        String lastLine = null;
        try (RandomAccessFile randomAccessFile = new RandomAccessFile(file, "r")) {
            long fileLength = randomAccessFile.length() - 1;
            if (fileLength < 0) {
                return null;
            }

            randomAccessFile.seek(fileLength);
            int readByte;
            while ((readByte = randomAccessFile.readByte()) != '\n') {
                fileLength--;
                randomAccessFile.seek(fileLength);
                if (fileLength == 0) {
                    break;
                }
            }

            lastLine = randomAccessFile.readLine();
        }
        return lastLine;
    }
}

