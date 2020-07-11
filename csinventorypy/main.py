import requests
from urllib.request import urlopen
import json
import time


def get_myinv_data(steamid:str, dump_to_json_file:bool=False) -> dict:
    try:
        data = urlopen('http://steamcommunity.com/profiles/'+steamid+'/inventory/json/730/2')
    except:
        time.sleep(60)
        get_myinv_data(steamid)

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

    if dump_to_json_file:
        json.dump(items, open("myinventory.json", "w"))
        
    return items

def get_inventory(steamid:str) -> list:
    try:
        data = urlopen('http://steamcommunity.com/profiles/'+steamid+'/inventory/json/730/2')
    except:
        time.sleep(60)
        get_inventory(steamid)

    json_data = json.loads(data.read())
    descriptions = json_data['rgDescriptions']
    inv =  [descriptions[v]["market_hash_name"] for v in descriptions]

    return inv

def get_raw_data(steamid: str) -> dict:
    try:
        data = urlopen('http://steamcommunity.com/profiles/'+steamid+'/inventory/json/730/2')
    except:
        time.sleep(60)
        get_raw_data(steamid)

    json_data = json.loads(data.read())
    return json_data

if __name__ == "__main__":
    print(get_raw_data("76561198439884801"))