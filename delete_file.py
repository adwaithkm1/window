import requests

filename = "file-to-delete.txt"
DELETE_URL = f"https://your-render-url.com/delete/{filename}"

response = requests.delete(DELETE_URL)
print(response.json())
