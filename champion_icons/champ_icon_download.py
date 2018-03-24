#!/usr/bin/env python3
import os 
import json

champ_list = open('../champion.json')
champ_list = json.loads(champ_list.read())

for champ in champ_list["data"].keys():
    CMD = "wget https://ddragon.leagueoflegends.com/cdn/8.6.1/img/champion/{}.png".format(champ)
    os.popen(CMD)


