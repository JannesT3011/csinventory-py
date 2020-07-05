import requests
from urllib.request import urlopen
import json
import time


def process(steamid:str, to_json:bool=False) -> dict:
    try:
        data = urlopen('http://steamcommunity.com/profiles/'+steamid+'/inventory/json/730/2')
    except:
        time.sleep(60)
        process(steamid)

    json_data = json.loads(data.read())
    descriptions = json_data['rgDescriptions']
    inv =  [descriptions[v] for v in descriptions]
    inventory = json_data["rgInventory"]
    
    amount = {}
    items = {}
    all_ids = []

    for rginv_id in inventory:
        all_ids.append(inventory[rginv_id]["classid"])
    
    for iid in all_ids:
        amount[iid] = all_ids.count(iid)

    for item in inv:
        _item = item["market_hash_name"]
        _item_id = item["classid"]
        items[_item] = {}
        items[_item]["itemid"] = _item_id
        items[_item]["amount"] = amount[_item_id]

    if to_json:
        json.dump(items, open("test.json", "w"))
        
    return items
    

if __name__ == "__main__":
    print(process("76561198439884801"))