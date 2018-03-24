#!/usr/bin/env python3
import os 
import json

item_list = open('../item_8.6.json')
item_list = json.loads(item_list.read())

for item in item_list["data"].keys():
    #IMG = "{}.png".format(item_list["data"][item]['name'].replace(" ",'_').replace("'",""))
    #CMD = "wget -O {} https://ddragon.leagueoflegends.com/cdn/8.6.1/img/item/{}.png".format(IMG,item)
    CMD = "wget https://ddragon.leagueoflegends.com/cdn/8.6.1/img/item/{}.png".format(item)
    os.popen(CMD)


