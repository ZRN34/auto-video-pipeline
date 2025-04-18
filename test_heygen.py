import os, requests

key = os.getenv("HEYGEN_API_KEY")
resp = requests.get(
    "https://api.heygen.com/v2/video/status.get?video_id=dummy",
    headers={"X-Api-Key": key}
)
print(resp.status_code, resp.text)
