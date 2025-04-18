import os, requests

key = os.getenv("HEYGEN_API_KEY")
print("🔑 HEYGEN_API_KEY =", key)

url = "https://api.heygen.com/v2/avatars"
headers = {"X-Api-Key": key}
resp = requests.get(url, headers=headers)

print("➡️ GET /v2/avatars  →", resp.status_code)
print(resp.text)
