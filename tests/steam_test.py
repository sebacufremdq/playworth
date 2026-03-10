import requests

url = "https://store.steampowered.com/api/featuredcategories"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers)

print("STATUS:", r.status_code)
print("FIRST 200:", r.text[:200])