#!/usr/bin/env python3

import json
import os
import pygame
import sys


pygame.init()
D_WIDTH = 1600
D_HEIGHT = 717
ITEM_WIDTH = 64
ITEM_HEIGHT = 64
CHAMPION_WIDTH = 120
CHAMPION_HEIGHT = 120

gameDisplay = pygame.display.set_mode((D_WIDTH,D_HEIGHT))
pygame.display.set_caption('ITEM')
clock = pygame.time.Clock()
ITEM_NAME = "NONE"
CURR_DIR = os.getcwd()

# Colors
white = (255,255,255)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
red = pygame.Color('red')
bright_red = pygame.Color('orangered')
gold = pygame.Color('gold')
lightgray = (75,75,75)

# Font
FONT = pygame.font.Font(None, 20)
SMALLFONT = pygame.font.Font(None, 16)

# Structure
ITEM_SET = {}
CURR_ITEMS = []
CHAMPION_SET = {}

# Labels
Champion1 = ''
Champion2 = ''

# Parse through items and add data to ITEM_SET
def createItemList():
    ITEM_LIST = open('item_8.6.json')
    ITEM_LIST = json.loads(ITEM_LIST.read())

    BASE_STATS = ITEM_LIST["basic"]["stats"]
    CURR_STATS = BASE_STATS
    for thing in ITEM_LIST["data"].keys():
    # If on Summoner Rift
        if ITEM_LIST["data"][thing]["maps"]["11"]:
            temp_dict = {};
            for key in ITEM_LIST["basic"].keys():
                if key in ITEM_LIST["data"][thing].keys():
                    temp_dict[key] = ITEM_LIST["data"][thing][key]
                else:
                    temp_dict[key] = ""
            temp_dict["id"] = thing
            ITEM_SET[ITEM_LIST["data"][thing]["name"] ] = temp_dict
    return ITEM_SET, CURR_STATS

# Parse through items and add data to CHAMP_SET
def createChampList(CURR_STATS):
    CHAMPION_LIST = open('champion.json')
    CHAMPION_LIST = json.loads(CHAMPION_LIST.read())
    for stat in CHAMPION_LIST["data"]["Aatrox"]["stats"].keys():
        CURR_STATS[stat] = 0
    for champ in CHAMPION_LIST["data"].keys():
        if champ == "MonkeyKing":
            CHAMPION_LIST ["Wukong"] = CHAMPION_LIST["data"][champ]
        else:
            CHAMPION_LIST [champ] = CHAMPION_LIST["data"][champ]
    return CHAMPION_LIST
# Classes
class CheckBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.selected = False
        self.text = text
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.color)
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.selected= not self.selected
        if self.selected:
            self.color = COLOR_ACTIVE
        else:
            self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.color)
    def draw(self):
        textRect = self.txt_surface.get_rect()
        textRect.center = (self.rect.x + self.rect.w/2, self.rect.y - 10)
        if self.selected:
            pygame.draw.line(gameDisplay, self.color, (self.rect.x,self.rect.y), (self.rect.x+self.rect.w,self.rect.y+self.rect.h))
            pygame.draw.line(gameDisplay, self.color, (self.rect.x+self.rect.w,self.rect.y), (self.rect.x,self.rect.y+self.rect.h))
        gameDisplay.blit(self.txt_surface, textRect)
        pygame.draw.rect(gameDisplay, self.color, self.rect, 2)


class InputBox:
    def __init__(self,x,y,w,h,inputset, text='',search=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.suggestions = []
        self.type = search
        self.prev = text
        if self.type == "item":
            self.set = inputset
        elif self.type.startswith("champion"):
            self.set = inputset
        self.type = search
    def handle_event(self, event, CURR_STATS, OrnnBool):
        if self.type == "item":
            self.set = ITEM_SET
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.type == "item":
                        if self.text in self.set.keys() and len(CURR_ITEMS)<6:
                            CURR_ITEMS.append(self.set[self.text])
                            for stat in self.set[self.text]["stats"].keys():
                                CURR_STATS[stat] += self.set[self.text]["stats"][stat]
                            self.text = ''
                            self.suggestions = []
                    elif (self.type.startswith("champion")):
                        for champ in self.set["data"]:
                            if self.text == self.set["data"][champ]["name"]:
                                for stat, value in self.set["data"][champ]["stats"].items():
                                    CURR_STATS[stat] += round(value, 2)
                                if self.prev != '':
                                    for stat,value in self.set["data"][self.prev]["stats"].items():
                                        CURR_STATS[stat] -= round(value, 2)
                                self.prev = champ
                                self.text = ''
                                self.suggestions = []
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.suggestions = []
                elif event.key == 127: #delete key
                    self.text = ''
                    self.suggestions = []
                elif event.key == pygame.K_TAB:
                    if len(self.suggestions) == 1:
                        self.text = self.suggestions[0]
                elif 57 >= event.key >=48: #1-9
                    if 10 > len(self.suggestions) >= event.key-49 :
                        self.text = self.suggestions[event.key-49]
                        self.suggestions = []
                elif 97 <= event.key <= 122 or event.key == 39 or event.key == 32: #If letter, space, or '
                    self.text += event.unicode
                if self.type.startswith("champion"):
                    self.suggestions = [ self.set["data"][thing]["name"] for thing in self.set["data"] if self.set["data"][thing]["name"].lower().startswith(self.text.lower()) ]
                else:
                    if OrnnBool:
                        self.suggestions = [ string for string in self.set.keys() if string.lower().startswith(self.text.lower())]
                    else:
                        self.suggestions = [ string for string in self.set.keys() if string.lower().startswith(self.text.lower()) and self.set[string]["requiredAlly"] != "Ornn"]
                self.suggestions = sorted(self.suggestions)
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self,screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        if 1<= len(self.suggestions) < 10:
            # Finds width of longest suggestion
            longest = sorted(self.suggestions, key =len)[-1]
            longest_len = FONT.size("Suggestion 5: " + longest)
            pygame.draw.rect(screen, lightgray, (self.rect.x, self.rect.y + self.rect.h + 20, longest_len[0], len(self.suggestions) *20))
            for i, sug in enumerate(self.suggestions):
                message_display(screen, "Suggestion {}".format(i+1), sug, self.rect.x, i*20 + self.rect.y + self.rect.h + 20, orientation="left")

def PushButton(msg,x,y,w,h,ic,ac,box,action=None):
    # ic = not pushed color, ac = pushed color, box = search bof
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    w = SMALLFONT.render(msg, True, white).get_width() + 5
    if x+w > mouse[0] > x and y+h > mouse[1] >y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "deleteitem":
                for i,search in enumerate(CURR_ITEMS):
                    if box.text == search['name']:
                        for key, value in search['stats'].items():
                            CURR_STATS[key] -= value
                        CURR_ITEMS.pop(i)
                        box.text = ''
                        break
        elif click[0] and action == "champ1":
            pass
        elif click[0] and action == "champ2":
            pass

    else:
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    textSurf = SMALLFONT.render(msg, 1, white)
    textRect = textSurf.get_rect()
    textRect.center = (x + w/2 ,(y + h/2))
    gameDisplay.blit(textSurf, textRect)


def message_display(screen, label, stat, x, y, color = white, orientation = "center"):
    display = FONT.render(label + ": " + stat, 1, color)
    textRect = display.get_rect()
    if orientation is "left":
        textRect = (x,y)
    else:
        textRect.center = ( x , y)
    screen.blit(display, textRect)

# Parse Command Line Arguments
def main():
    TYPE_BOX_X= 400
    TYPE_BOX_Y = 25
    TYPE_BOX_WIDTH = 140
    TYPE_BOX_HEIGHT = 32
    INIT_ITEM_SET, CURR_STATS = createItemList()
    CHAMPION_LIST = createChampList(CURR_STATS)
    champ_box = InputBox (TYPE_BOX_X, TYPE_BOX_Y, TYPE_BOX_WIDTH, TYPE_BOX_HEIGHT, CHAMPION_LIST, search = "champion1")
    search_box = InputBox (TYPE_BOX_X, (TYPE_BOX_Y + D_HEIGHT)/2, TYPE_BOX_WIDTH, TYPE_BOX_HEIGHT, INIT_ITEM_SET, search="item")
    ornn_checkbox = CheckBox (TYPE_BOX_X - TYPE_BOX_HEIGHT - 15, (TYPE_BOX_Y + D_HEIGHT)/2 + 3, TYPE_BOX_HEIGHT-6, TYPE_BOX_HEIGHT-6, text="Ornn items?")
    input_boxes = [search_box, champ_box]
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event, CURR_STATS, ornn_checkbox.selected)
            ornn_checkbox.handle_event(event)



        for box in input_boxes:
            box.update()

        gameDisplay.fill((30,30,30))
        
        # Ornn Changes
        ornn_checkbox.draw()
        ITEM_SET = INIT_ITEM_SET

        # Totaling gold
        totalGold = 0;
        search_box.draw(gameDisplay)
        for box in input_boxes:
            box.draw(gameDisplay)
        for num, item in enumerate(sorted(CURR_ITEMS, reverse=True,key=lambda g: g['gold']['total'])):
            totalGold += CURR_ITEMS[num]['gold']['total']
            if num == 0:
                display_icon(item, gameDisplay, 0, 0)
            else:
                display_icon(item, gameDisplay, 0, (num) * (ITEM_HEIGHT +30))
        display_champ_icon(champ_box.prev, TYPE_BOX_X + search_box.rect.w + 30, TYPE_BOX_Y - 13)
        # Displays Gold
        message_display(gameDisplay, "Total Gold Cost", str(totalGold), 10, D_HEIGHT-30,color=gold, orientation="left")
        # Displays labels
        message_display(gameDisplay, "Champion 1", Champion1, TYPE_BOX_X + search_box.rect.w/2, TYPE_BOX_Y - 13, orientation="center")
        message_display(gameDisplay, "Items", Champion1, TYPE_BOX_X + champ_box.rect.w/2, (TYPE_BOX_Y + D_HEIGHT)/2 - 13, orientation="center")
        # Prints out the stats
        i=0
        longest_length = 0
        # Should find the longest string length for the stats
        for key,value in CURR_STATS.items():
            length = FONT.size("{}: {}".format(key,str(value)))[0]
            if longest_length < length:
                longest_length = length
        # Displays all the stats that aren't 0 or not perlevel
        for key,value in sorted(CURR_STATS.items()):
            if value and not key.endswith('perlevel'):
                message_display(gameDisplay, key, str(value), D_WIDTH - longest_length - 10, i*20, orientation="left")
                i += 1
        #Displays Delete item button
        PushButton("Delete Item", TYPE_BOX_X + search_box.rect.w + 10, (TYPE_BOX_Y + D_HEIGHT)/2, TYPE_BOX_HEIGHT, TYPE_BOX_HEIGHT, red, bright_red, search_box, "deleteitem")

        PushButton("Champion 1", TYPE_BOX_X + search_box.rect.w, (TYPE_BOX_Y + D_HEIGHT)/4, TYPE_BOX_HEIGHT, TYPE_BOX_HEIGHT, red, COLOR_INACTIVE, search_box, "champ1")
        # Updates screen
        pygame.display.update()
        clock.tick(60)

# Functions
def display_abilities(champ_name):
    pass
def display_icon(item, screen, x, y):
#    item_mod = item["name"].replace(' ', '_').replace("'","")
    if (os.path.isfile(CURR_DIR + "/item_icons/"+item['id'] + ".png")):
        IMG_NAME = pygame.image.load('{}.png'.format("item_icons/"+ item['id']))
        label = FONT.render(item["name"], 1, white)

        screen.blit(IMG_NAME, (0, y))
        screen.blit(label, (0, y + ITEM_HEIGHT+5))

def display_champ_icon(champ, x, y):
    if (os.path.isfile(CURR_DIR + "/champion_icons/" + champ + ".png")):
        champName = CHAMPION_LIST["data"][champ]["name"]
        IMG_NAME = pygame.image.load('{}.png'.format("champion_icons/" + champ))
        label = FONT.render(champName, 1, white)
        labeltext = label.get_rect()
        labeltext.center = (x+CHAMPION_WIDTH/2, y+ CHAMPION_HEIGHT+10)
        gameDisplay.blit(IMG_NAME, (x,y))
        gameDisplay.blit(label, labeltext)

if __name__ == '__main__':
    main()
    pygame.quit()
