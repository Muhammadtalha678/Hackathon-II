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
            "user_id": "UgJ72dkAZEi9TaLGwd3D1nGKmIOXvFCt",
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
            "user_id": "UgJ72dkAZEi9TaLGwd3D1nGKmIOXvFCt",
            "task_id": 3
        }
    }
}




headers = {
    "Accept": "application/json,text/event-stream",
    "Authorization":"Bearer eyJhbGciOiJFZERTQSIsImtpZCI6ImV0cklycU4xS1ZSVkcxTVEydk5uMnlFNkc4ajYzTEJZIn0.eyJpYXQiOjE3NzA1ODAyMjAsIm5hbWUiOiJNdWhhbW1hZCBUYWxoYSAiLCJlbWFpbCI6Im11aGFtbWFkdGFsaGEwMTEwQGdtYWlsLmNvbSIsImVtYWlsVmVyaWZpZWQiOmZhbHNlLCJpbWFnZSI6bnVsbCwiY3JlYXRlZEF0IjoiMjAyNi0wMi0wOFQxNDo0OToxMi45NzRaIiwidXBkYXRlZEF0IjoiMjAyNi0wMi0wOFQxNDo0OToxMi45NzRaIiwiaWQiOiJVZ0o3MmRrQVpFaTlUYUxHd2QzRDFuR0ttSU9YdkZDdCIsInN1YiI6IlVnSjcyZGtBWkVpOVRhTEd3ZDNEMW5HS21JT1h2RkN0IiwiZXhwIjoxNzcxMTg1MDIwLCJpc3MiOiJodHRwczovL2hhY2thdGhvbi1paS1ldGEudmVyY2VsLmFwcCIsImF1ZCI6Imh0dHBzOi8vaGFja2F0aG9uLWlpLWV0YS52ZXJjZWwuYXBwIn0.8Lv6ja8zk7rveyXb5of0K4R7c6735YO9te_vgod2zl_e34epSLP0nAMzzRZBjXtRi8a7e0wW1XQtXrJuDyXFCg"
}

# response = httpx.post(url, json=payload, headers=headers)
response = httpx.post(url=url,json=all_payload,headers=headers)

print(response.text) 