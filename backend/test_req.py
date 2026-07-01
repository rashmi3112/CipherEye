import urllib.request
import json
url = "http://127.0.0.1:8000/api/v1/analyze"
data = json.dumps({"content_type": "url", "content": "http://example.com"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(e)
