from csinventorypy import CSInventory
from steampy.client import SteamClient
from steampy.models import GameOptions
import time
import json

csinv = CSInventory("STEAM_ID")
client = SteamClient("STEAM_API_KEY")

def process():
    inv = csinv.get_myinv_data(False)
    for item in inv:
        if item.startswith("Sealed") or item.startswith("Graffiti") or item.endswith("Medal") or item.startswith("Storage") or item.endswith("Badge"):
            pass
        else:
            try:
                amount = inv[item]["amount"]
                itemid = inv[item]["itemid"]
                inv[item] = client.market.fetch_price(item, GameOptions.CS)
                inv[item]["amount"] = amount
                inv[item]["itemid"] = itemid
                #print(item["amount"])
            except:
                time.sleep(60)
    
    json.dump(inv, open("myinventory.json", "w"))
    return inv


if __name__ == "__main__":
    print(process())