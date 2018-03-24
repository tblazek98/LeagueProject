#!/usr/bin/env python3 

import json
import requests
from bs4 import BeautifulSoup as soup 
import re 
import sys

def open_json(PATH='champ_info/champ_info.json'):
    f = open(PATH)
    return f

def parse_html(string): 
    #regex = re.compile('<.*>')
    i = 0 
    return_str = ""
    while(i < len(string)):
        s = string[i]
        if s == '<':
            i += 1
            while string[i] != '>':
                i += 1
            i += 1
        if i < len(string):
            return_str += string[i]
        i += 1
    return return_str 

def replace_vars(string, effect_list, var_list, LEVEL=1):
    LEVEL = LEVEL -1 
    return_str = "" 
    i = 0
    while(i < len(string)):
        s = string[i]
        if s == '{':
            i = i + 3
            type_ = string[i]
            if type_ == 'e':
                i += 1
                index = int(string[i])
                # NEED TO CHANGE BASED ON ABILITY LEVEL
                try:
                    return_str += str(effect_list[index][LEVEL])
                except: 
                    pass
            else: 
                i += 1
                type_ += string[i]
                found = False 
                if var_list: 
                    for v in var_list: 
                        if v["key"] == type_:
                            return_str += ''.join([str(x) for x in v["coeff"]])
                            return_str += " " + v["link"]
                            found = True 
                            break 
                    if found: 
                        pass
                    elif type_[0] == 'f': 
                        # The effect is in the effect list 
                        index = int(type_[1])
                        return_str += str(effect_list[index][LEVEL])
                        for v in var_list: 
                            if v["key"][1] == str(index):
                                return_str += v["link"]
                                break

            i += 3
        if i < len(string):
            if string[i] != '}':
                return_str += string[i]
        i += 1
    return return_str


def get_spell(champ='Katarina', SPELL=1):
    f = open_json()
    INFO = json.loads(f.read())
    CHAMP_DICT = INFO["data"] # Dict with champ name key
    CHAMP_DATA = CHAMP_DICT[champ]
    SPELLS = CHAMP_DATA["spells"]
    RETURN_DICT = { 1:{}, 2: {}, 3:{}, 4:{}}
    for i, spell in enumerate(SPELLS):
        RETURN_DICT[i+1]["name"] = spell["name"]
        # effects in order of when they are mentioned in the tooltip  
        RETURN_DICT[i+1]["effects"]  = spell["effect"]
        RETURN_DICT[i+1]["tooltip"] = spell["sanitizedTooltip"]
        if 'vars' in spell.keys():
            RETURN_DICT[i+1]["vars"] = spell["vars"]
        else: 
            RETURN_DICT[i+1]["vars"] = None

    


    return RETURN_DICT[SPELL]



def get_champ_spell(champ='Katarina', SPELL_INDEX=1, SPELL_LEVEL=3):
    spell = get_spell(champ, SPELL_INDEX)
    tooltip = replace_vars(spell["tooltip"], spell["effects"], spell["vars"], SPELL_LEVEL)
    tooltip = tooltip.replace("spelldamage", "Ability Power").replace("bonusattackdamage", "Bonus Attack Damage").replace("attackdamage", "Base Attack Damage")
    return tooltip 



if __name__ == '__main__':
    l = "QWER"
    i = 0 
    for NUM in [1,2,3,4]:
        print(l[i], " ")
        print(get_champ_spell(sys.argv[1], NUM, 3))
        i += 1
        print()


