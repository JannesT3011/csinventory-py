import requests
from urllib.request import urlopen
import json
import time
from steampy.client import SteamClient
from steampy.models import GameOptions
import steampy

_blacklist = []

class CSInventory:
    """ Create instance of CSInventory
    :param steamid: The SteamID of the user
    :type steamid: str
    """
    def __init__(self, steamid:str):
        """ Constructor Mehtod
        """
        self.steamid = steamid

    def get_myinv_data(self, dump_to_json_file:bool=False) -> dict:
        """ Get the data of your inventory, hash_name, itemid and amount
        :param dump_to_json: Dump data to myinventory.json
        :type dump_to_json: bool, optional
        :return: Your inventory data
        :rtype: dict
        """
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')

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
        """ Returns your inventory items, only the hash_market_names
        :return: List of your inventory itemnames
        :rtype: list
        """
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')

        json_data = json.loads(data.read())
        descriptions = json_data['rgDescriptions']
        inv =  [descriptions[v]["market_hash_name"] for v in descriptions]

        return inv

    def get_raw_data(self) -> dict:
        """ Get your raw inventory json data
        :return: dict of raw inventory data from the steam api
        :rtype: dict
        """
        try:
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')
        except:
            time.sleep(60)
            data = urlopen('http://steamcommunity.com/profiles/'+self.steamid+'/inventory/json/730/2')

        json_data = json.loads(data.read())
        return json_data
    
    def get_inv_steamdata(self, api_token:str, dump_to_json_file:bool=False) -> dict:
        """ Get your inventory data + the steammarket data
        :param api_token: Your steamAPI key
        :type api_token: str
        :param dump_to_json: Dump inventory data to myinventory.json file
        :type dump_to_json: str, optional
        :return: Dict of your inventory data + steammarket data
        :rtype: dict
        """
        inv = self.get_myinv_data(False)
        new_inventory = {}

        steam_client = SteamClient(api_token)

        for item in inv:
            if not item.startswith("Sealed Graffiti") and not item.startswith("Graffiti") and not item.endswith("Medal") and not item.endswith("Badge") and not item.startswith("Storage"):
                try:
                    _amount = inv[item]["amount"]
                    _itemid = inv[item]["itemid"]
                    new_inventory[item] = {}
                    _steam_data = steam_client.market.fetch_price(item, GameOptions.CS) 
                    new_inventory[item] = _steam_data
                    new_inventory[item]["amount"] = _amount
                    new_inventory[item]["itemid"] = _itemid
                    _median_price = float(_steam_data["median_price"].split(" USD")[0].split("$")[1])
                    _lowsest_price = float(_steam_data["lowest_price"].split(" USD")[0].split("$")[1])
                    new_inventory[item]["total_median"]  = round(_amount * _median_price, 2)
                    new_inventory[item]["total_cashout"] = round(_amount * _lowsest_price, 2) 
                    new_inventory[item]["median_price"] = _median_price
                    new_inventory[item]["lowest_price"] = _lowsest_price
                except steampy.exceptions.TooManyRequests:
                    time.sleep(60)
                except KeyError:
                    pass
        
        if dump_to_json_file:
            json.dump(new_inventory, open("myinventory.json", "w"))
            return new_inventory

        return new_inventory
