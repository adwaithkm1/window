import requests

UPLOAD_URL = "http://localhost:5000/upload"
file_path = "test.txt"  # Make sure this file exists

with open(file_path, "rb") as file:
    response = requests.post(UPLOAD_URL, files={"file": file})

print(response.json())  # Should return {"message": "File uploaded successfully", "filename": "file-123456.txt"}
