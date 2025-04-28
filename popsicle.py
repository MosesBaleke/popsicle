hi from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient
from starlette.requests import Request as StarletteRequest
from starlette.datastructures import Headers, URL
SELECT *
FROM your_table
WHERE CURRENT_TIMESTAMP >= start_timestamp
  AND CURRENT_TIMESTAMP <= end_timestamp;
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
    
    from moto import mock_ecs
import boto3
import pytest
from your_module import stop_task  # Replace with the path to your function

@mock_ecs
def test_stop_task():
    # Set up mock ECS environment
    client = boto3.client('ecs', region_name='us-east-1')

    # Create a cluster and a task
    cluster_name = "test-cluster"
    client.create_cluster(clusterName=cluster_name)
    
    task_arn = "arn:aws:ecs:us-east-1:123456789012:task/test-task-id"
    client.run_task(cluster=cluster_name, taskDefinition="test-task-def")
    
    # Mock stopping the task
    response = stop_task(cluster_name, task_arn)
    
    # Validate the response
    assert response['task']['taskArn'] == task_arn
    assert response['task']['lastStatus'] == 'STOPPED'
    
    
    from moto import mock_ecs
import boto3
from your_module import stop_task  # Replace with your actual function

@mock_ecs
def test_stop_task():
    # Set up mock ECS environment
    client = boto3.client('ecs', region_name='us-east-1')

    # Create a cluster
    cluster_name = "test-cluster"
    client.create_cluster(clusterName=cluster_name)

    # Register a task definition
    client.register_task_definition(
        family="test-task-def",
        containerDefinitions=[
            {
                "name": "test-container",
                "image": "test-image",
                "memory": 128,
                "cpu": 128,
            }
        ],
    )

    # Run a task (use the registered task definition)
    task_response = client.run_task(
        cluster=cluster_name,
        taskDefinition="test-task-def"
    )
    task_arn = task_response["tasks"][0]["taskArn"]

    # Stop the task
    response = stop_task(cluster_name, task_arn)

    # Validate the response
    assert response['task']['taskArn'] == task_arn
    assert response['task']['lastStatus'] == 'STOPPED'
    
    import os
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"


import pytest
import requests

def fetch_task(metadata_url):
    """Function that fetches task details from the given metadata_url."""
    response = requests.get(f"{metadata_url}/task")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed with status code {response.status_code}"}

def test_fetch_task(monkeypatch):
    """Test the fetch_task function using monkeypatch to mock requests.get."""
    # Define a mock response
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(url):
        # Return a mock response depending on the URL
        if url == "https://example.com/api/task":
            return MockResponse({
                "id": "12345",
                "name": "Sample Task",
                "status": "pending",
                "created_at": "2024-12-01T12:00:00Z",
                "updated_at": "2024-12-01T12:15:00Z",
                "details": {
                    "priority": "high",
                    "assigned_to": "user123",
                    "due_date": "2024-12-10T12:00:00Z"
                }
            }, 200)
        else:
            return MockResponse({"error": "Not found"}, 404)

    # Use monkeypatch to replace requests.get with mock_get
    monkeypatch.setattr(requests, "get", mock_get)

    # Call the function and assert the response
    metadata_url = "https://example.com/api"
    result = fetch_task(metadata_url)
    assert result["id"] == "12345"
    assert result["name"] == "Sample Task"
    assert result["status"] == "pending"
    assert result["details"]["priority"] == "high"
    
    
    
    import os
import pytest

def get_task_id():
    """Example function that retrieves an environment variable."""
    ecs_url = os.environ.get('ECS_TASK_METADATA_URL')
    if ecs_url:
        return ecs_url
    return "Environment variable not set"

def test_get_task_id(monkeypatch):
    """Test the get_task_id function by mocking os.environ.get."""
    # Mock the environment variable
    mock_value = "https://example.com/api/task"
    monkeypatch.setenv("ECS_TASK_METADATA_URL", mock_value)

    # Call the function and assert the result
    result = get_task_id()
    assert result == mock_value
    
    
    def mock_get(url):
    if url == "https://example.com/api/task":
        return MockResponse({
            "TaskARN": "arn:aws:ecs:region:account-id:task/task-id"
        }, 200)
    return MockResponse({"error": "Not Found"}, 404)
    
    import com.microsoft.playwright.*;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

public class TableDateSortingValidation {
    public static void main(String[] args) {
        // Initialize Playwright
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false));
            BrowserContext context = browser.newContext();
            Page page = context.newPage();

            // Navigate to the page
            page.navigate("https://example.com");

            // Define the date-time format with milliseconds (adjust the pattern if needed)
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

            // Locator for table rows
            Locator rows = page.locator("table tbody tr"); // Adjust the selector to match your table rows

            // Extract text from the third column of each row and parse into LocalDateTime
            List<LocalDateTime> dateTimes = new ArrayList<>();
            for (int i = 0; i < rows.count(); i++) {
                String cellText = rows.nth(i).locator("td:nth-child(3)").textContent(); // Adjust column index (3 for the third column)
                try {
                    LocalDateTime dateTime = LocalDateTime.parse(cellText.trim(), formatter);
                    dateTimes.add(dateTime);
                } catch (Exception e) {
                    System.err.println("Failed to parse date: " + cellText);
                }
            }

            // Validate ascending order
            List<LocalDateTime> sortedAsc = new ArrayList<>(dateTimes);
            Collections.sort(sortedAsc);

            if (dateTimes.equals(sortedAsc)) {
                System.out.println("The dates are sorted in ascending order.");
            } else {
                System.out.println("The dates are NOT sorted in ascending order.");
            }

            // Validate descending order
            List<LocalDateTime> sortedDesc = new ArrayList<>(dateTimes);
            sortedDesc.sort(Collections.reverseOrder());

            if (dateTimes.equals(sortedDesc)) {
                System.out.println("The dates are sorted in descending order.");
            } else {
                System.out.println("The dates are NOT sorted in descending order.");
            }
        }
    }
    
    
    import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> input = Arrays.asList("[vvvx, vvvx]");
        List<String> output = new ArrayList<>();

        for (String item : input) {
            // Remove the surrounding square brackets and spaces
            String cleaned = item.replaceAll("[\\[\\]]", "").trim();
            // Split the string by comma and trim each element
            String[] parts = cleaned.split(",");
            for (String part : parts) {
                output.add(part.trim());
            }
        }

        // Print the output
        System.out.println(output); // Output: [vvvx, vvvx]
    }
    
    Here is a filled-out version of the provided sections tailored to your role as a software developer:

Collaboration

Demonstrated strong collaboration skills by working closely with cross-functional teams to deliver phase 2 features on time. Coordinated effectively with QA teams, ensuring thorough testing coverage, and collaborated with system architects to optimize S3 data download processes. Additionally, regular communication with stakeholders helped align expectations and address concerns, improving team efficiency and project outcomes.

Expertise

Showcased deep technical expertise in optimizing system performance by implementing index-based filtering, reducing S3 reference data download time for 17GB objects from 30 to 10 minutes. Developed unit and regression tests for critical components (dm-connect, dm-uploader, and jams-splitter), improving code quality and ensuring stability. Applied best practices in code reviews and analysis, identifying opportunities for refactoring and minimizing technical debt.

Innovation

Introduced innovative solutions to enhance system efficiency and monitoring. The implementation of email alert notifications improved error detection and response time, ensuring teams were promptly informed of system warnings and failures. Leveraged automation in regression testing to streamline QA processes and minimize manual intervention, improving overall system reliability.

Responsibility

Took ownership of critical system improvements and QA practices, ensuring timely delivery of features and maintaining system stability. Proactively identified performance bottlenecks and implemented solutions to enhance speed and reliability. By increasing unit test coverage and creating robust regression tests, ensured future enhancements could be delivered with confidence and minimal risk. Maintained high accountability for code quality through regular analysis and reviews.

This summary aligns your achievements as a developer with key areas of collaboration, expertise, innovation, and responsibility. Let me know if you’d like further refinements!
    
    
    import com.microsoft.playwright.*;

public class TableCheck {
    public static void main(String[] args) {
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false));
            BrowserContext context = browser.newContext();
            Page page = context.newPage();

            // Navigate to the page
            page.navigate("YOUR_PAGE_URL");

            // Locate the table
            Locator table = page.locator("table");

            // Locate all rows in the table
            Locator rows = table.locator("tr");

            // Loop through rows
            for (int i = 0; i < rows.count(); i++) {
                Locator row = rows.nth(i);
                // Locate columns in the current row
                Locator columns = row.locator("td");

                // Loop through columns
                for (int j = 0; j < columns.count(); j++) {
                    String cellText = columns.nth(j).textContent();
                    // Check if the cell contains the desired text
                    if (cellText != null && cellText.contains("YOUR_DESIRED_TEXT")) {
                        System.out.println("Found text in row " + i + ", column " + j);
                    }
                }
            }
            
            from sqlalchemy import Column, Integer, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    start_ts = Column(DateTime, nullable=False)

# Manually creating an instance
record = Record(id=1, start_ts=datetime.datetime.utcnow())

# Accessing the attribute
print(record.start_ts)

wget https://github.com/java-decompiler/jd-cli/releases/latest/download/jd-cli.jar -O /usr/local/bin/jd-cli.jar
echo 'alias jd="java -jar /usr/local/bin/jd-cli.jar"' >> ~/.bashrc
source ~/.bashrc
        }
    }
}
dnf install -y java-17-amazon-corretto wget



CREATE FUNCTION set_column_same_as_id() RETURNS TRIGGER AS $$
BEGIN
    NEW.your_column := NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER set_column_same_as_id
BEFORE INSERT ON your_table
FOR EACH ROW
EXECUTE FUNCTION set_column_same_as_id();

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class DateTimeExample {
    public static void main(String[] args) {
        String dateString = "2025-03-25";  // Given date

        // Convert String to LocalDate
        LocalDate date = LocalDate.parse(dateString);

        // Get current time
        LocalTime currentTime = LocalTime.now();

        // Combine date and time
        LocalDateTime dateTime = LocalDateTime.of(date, currentTime);

        // Format the output
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formattedDateTime = dateTime.format(formatter);

        // Print result
        System.out.println("Updated DateTime: " + formattedDateTime);
    }
}

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.regions.providers.DefaultAwsRegionProviderChain;

public class AwsRegionDetector {
    public static void main(String[] args) {
        Region region;
        try {
            region = new DefaultAwsRegionProviderChain().getRegion();
            if (region == null) {
                // Fallback to a default
                region = Region.US_EAST_1;
            }
        } catch (Exception e) {
            // Fallback in case of error
            region = Region.US_EAST_1;
        }

        System.out.println("Using AWS region: " + region.id());
    }
}
import boto3

# Create a boto3 client
autoscaling_client = boto3.client('autoscaling')

# Update the Auto Scaling Group
response = autoscaling_client.update_auto_scaling_group(
    AutoScalingGroupName='your-auto-scaling-group-name',
    MinSize=2,
    MaxSize=5,
    DesiredCapacity=3,
    HealthCheckType='EC2',
    HealthCheckGracePeriod=300
)

print("Update response:", response)


}
}
}

