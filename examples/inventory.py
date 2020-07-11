from csinventorypy import CSInventory

csinv = CSInventory("YOUR_STEAMID")

# Get inv data (Item-Names + Amount)
def get_my_cs_inventory_data():
    print(csinv.get_myinv_data(dump_to_json_file=False))

# Get Inventory (Only Item-Names)
def get_my_inventory():
    print(csinv.get_inventory())

# Get raw data (raw json from api)
def get_my_raw_inventory_data():
    print(csinv.get_raw_data())

if __name__ == "__main__":
    get_my_cs_inventory_data()
    # get_my_inventory()
    # get_my_raw_inventory_data()