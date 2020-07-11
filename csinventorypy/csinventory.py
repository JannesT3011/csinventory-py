import requests
from urllib.request import urlopen
import json
import time


class CSInventory:
    def __init__(self, steamid:str):
        self.steamid = steamid

    def get_myinv_data(self, dump_to_json_file:bool=False) -> dict:
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            self.get_myinv_data(self.steamid)

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

    def get_inventory(self) -> list:
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            self.get_inventory()

        json_data = json.loads(data.read())
        descriptions = json_data['rgDescriptions']
        inv =  [descriptions[v]["market_hash_name"] for v in descriptions]

        return inv

    def get_raw_data(self) -> dict:
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            self.get_raw_data()

        json_data = json.loads(data.read())
        return json_data