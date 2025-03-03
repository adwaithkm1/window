import requests

LIST_FILES_URL = "https://your-render-url.com/files"
response = requests.get(LIST_FILES_URL)
print(response.json())
