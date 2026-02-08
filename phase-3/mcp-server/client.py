import httpx

url = "https://hackathon-ii.onrender.com/mcp"

# http://localhost:8000/mcP

payload = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list",
    "params": {}
}
all_payload = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "list_tasks",
        "arguments": {
            "user_id": "htI93mLFVnHPmEtTE97I2ldfqjrvcYKg",
            "status": "completed"
        }
    }
}
add_payload ={
    "jsonrpc": "2.0",
    "id": "3",
    "method": "tools/call",
    "params": {
        "name": "add_task",
        "arguments": {
            "task": {
                "title": "Buy Groceries",
                "description": "Milk, eggs, and bread",
                "user_id": "htI93mLFVnHPmEtTE97I2ldfqjrvcYKg"
            }
        }
    }
}

complete_payload = {
    "jsonrpc": "2.0",
    "id": "4",
    "method": "tools/call",
    "params": {
        "name": "complete_task",
        "arguments": {
            "user_id": "htI93mLFVnHPmEtTE97I2ldfqjrvcYKg",
            "task_id": 3
        }
    }
}

update_payload = {
    "jsonrpc": "2.0",
    "id": "5",
    "method": "tools/call",
    "params": {
        "name": "update_task",
        "arguments": {
            "user_id": "htI93mLFVnHPmEtTE97I2ldfqjrvcYKg",
            "task_id": 3,
            "title": "Updated Task Title",
            "description": "Updated Description"
        }
    }
}

delete_payload = {
    "jsonrpc": "2.0",
    "id": "6",
    "method": "tools/call",
    "params": {
        "name": "delete_task",
        "arguments": {
            "user_id": "htI93mLFVnHPmEtTE97I2ldfqjrvcYKg",
            "task_id": 3
        }
    }
}




headers = {
    "Accept": "application/json,text/event-stream",
    "Authorization":"Bearer eyJhbGciOiJFZERTQSIsImtpZCI6ImV0cklycU4xS1ZSVkcxTVEydk5uMnlFNkc4ajYzTEJZIn0.eyJpYXQiOjE3NzA1MzU3MjAsIm5hbWUiOiJNdWhhbW1hZCBUYWxoYSIsImVtYWlsIjoidGFsaGFmaXJvejEyQGdtYWlsLmNvbSIsImVtYWlsVmVyaWZpZWQiOmZhbHNlLCJpbWFnZSI6bnVsbCwiY3JlYXRlZEF0IjoiMjAyNi0wMi0wOFQwNzoyODoyMi4yMDdaIiwidXBkYXRlZEF0IjoiMjAyNi0wMi0wOFQwNzoyODoyMi4yMDdaIiwiaWQiOiJodEk5M21MRlZuSFBtRXRURTk3STJsZGZxanJ2Y1lLZyIsInN1YiI6Imh0STkzbUxGVm5IUG1FdFRFOTdJMmxkZnFqcnZjWUtnIiwiZXhwIjoxNzcxMTQwNTIwLCJpc3MiOiJodHRwczovL2hhY2thdGhvbi1paS1ldGEudmVyY2VsLmFwcCIsImF1ZCI6Imh0dHBzOi8vaGFja2F0aG9uLWlpLWV0YS52ZXJjZWwuYXBwIn0.qVsCtpoEdyRVFtpiF9WIudmA4TOz7D-YqphTNWPXIag_rntRZ-UpMWjRjfXE1lmMD3KwuBcpO9hSq7NHTTlfBw"
}

# response = httpx.post(url, json=payload, headers=headers)
response = httpx.post(url=url,json=delete_payload,headers=headers)

print(response.text) 