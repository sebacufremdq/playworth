from clients.steam_client import SteamClient
import sys
print(sys.path)

steam = SteamClient()

catalog = steam.get_catalog()

print("TOTAL GAMES:", len(catalog))
print(catalog[:5])

appid = catalog[0]["appid"]

details = steam.get_app_details(appid)

print(details["name"])

reviews = steam.get_reviews(appid)

print("REVIEWS:", reviews)