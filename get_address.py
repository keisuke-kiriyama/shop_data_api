import urllib.request
import urllib.parse
import sys
import json
import os

url = 'https://maps.googleapis.com/maps/api/geocode/json'
latlng = '35.659272,139.697958'
key = os.environ.get('GOOGLE_API_KEY')
query = [
    ("format", "json"),
    ("latlng", latlng),
    ("key", key)
]

url += "?{0}".format(urllib.parse.urlencode(query))

try:
    result = urllib.request.urlopen(url).read()
except ValueError:
    print("APIアクセス失敗")
    sys.exit()

data = json.loads(result.decode('utf-8'))
print(data['results'][0]["formatted_address"])