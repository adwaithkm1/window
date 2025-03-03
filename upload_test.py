import requests

UPLOAD_URL = "https://your-render-url.com/upload"
file_path = "test_file.txt"

with open(file_path, "rb") as file:
    response = requests.post(UPLOAD_URL, files={"file": file})

print(response.json())
