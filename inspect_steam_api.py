import urllib.request
import json

url = "https://store.steampowered.com/api/appdetails?appids=1171690"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode('utf-8'))
    details = data["1171690"]["data"]
    print("Keys in details:", details.keys())
    if "movies" in details:
        print("Movies type:", type(details["movies"]))
        print("First movie keys and structure:")
        first_movie = details["movies"][0]
        print(json.dumps(first_movie, indent=2))
