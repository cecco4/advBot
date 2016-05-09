# -*- coding: utf-8 -*-
import sys
import time
import random
import datetime
import telepot
import json
"""
A simple bot that accepts two commands:
- /roll : reply with a random integer between 1 and 6, like rolling a dice.
- /time : reply with the current time, like a clock.
INSERT TOKEN below in the code, and run:
$ python diceyclock.py
Ctrl-C to kill.
"""

class World():

    def __init__(self, json):
        self.Nodes = {}
        print "loading world"

        for ndata in json['nodeDataArray']:
            n = Node(ndata)
            self.Nodes[n.key] = n
            print n

        for ldata in json['linkDataArray']:
            if(ldata['text'] != None):
                print ldata['from'] + "->" + ldata['to'] + "  " \
                    + ldata['text']

                self.Nodes[ldata['from']].links[ldata['text']] = \
                    self.Nodes[ldata['to']]
        
            if(ldata['toText'] != None):
                print ldata['to'] + "->" + ldata['from'] + "  " \
                    + ldata['toText']
                self.Nodes[ldata['to']].links[ldata['toText']] = \
                    self.Nodes[ldata['from']]

        self.pos = self.Nodes['1']
        self.inv = []

    def pick(self, item):
        item = item.lower().strip()
        print "Searching " + item,
        for i in self.pos.items:
            if item == i.name:
                print " found!"
                self.pos.items.remove(i);
                self.inv.append(i)
                return True
        print " not found :("
        return False

    def drop(self, item):
        item = item.lower().strip()
        print "Searching " + item,
        for i in self.inv:
            if item == i.name:
                print " found!"
                self.pos.items.append(i);
                self.inv.remove(i)
                return True
        print " not found :("
        return False

    def inventory(self):
        if len(self.inv) == 0:
            return "Inventario vuoto"
        s = "Inventario:\n";
        for i in self.inv:
            s += i.name +"\n"
        return s
    
class Node():
    def __init__(self, json):
        self.key   = json['key']
        self.name  = json['name']
        self.descr = json['descr']
        self.items = []
        for itData in json['items']:
            self.items.append(Item(itData))
        self.links = {}

    def __str__(self):
        str =  self.key + " " + self.name + "[ ";
        for i in self.items:
            str += i.name + " "
        str +="]"
        return str

    def description(self):
        msg = self.name + "\n" + self.descr + "\n"
        for i in self.items:
            msg += i.name + "\n";
        return msg

class User():
    global worldData
    
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.world = World(worldData)

class Item():
    def __init__(self, json):
        self.name = json['name']

    def __str__(self):
        return self.name
        
def handle(msg):
    global Users, Nodes
    
    chat_id = msg['chat']['id']
    command = msg['text']

    usr = None
    try:
        usr = Users[chat_id]
        print "Position: " + usr.world.pos.name
        
    except KeyError:
        usr = User(chat_id)
        Users[chat_id] = usr
        print "New user position: " + usr.world.pos.name
        
    print 'Got command: %s' % command

    command = command.lower().strip()
    
    if command == 'look':
        bot.sendMessage(chat_id, usr.world.pos.description())
    
    elif command == 'inv':
        bot.sendMessage(chat_id, usr.world.inventory())
        
    elif "prendi" in command:
        item = command.split(" ", 1)
        if len(item)>1:
            if usr.world.pick(item[1]):
                bot.sendMessage(chat_id, item[1] + u" raccolto")
            else:
                bot.sendMessage(chat_id, u"non c'è " + item[1])

    elif "molla" in command:
        item = command.split(" ", 1)
        if len(item)>1:
            if usr.world.drop(item[1]):
                bot.sendMessage(chat_id, item[1] + u" mollato per terra")
            else:
                bot.sendMessage(chat_id, u"non c'è " + item[1])
            
    else:
        try:
            newPos = usr.world.pos.links[command]
            usr.world.pos = newPos
            bot.sendMessage(chat_id, usr.world.pos.description())

        except KeyError:
            bot.sendMessage(chat_id, "Non conosco "+command)


f = open('worlds/dt.txt', 'r')
worldData = json.loads(f.read())

Users = {}

bot = telepot.Bot('182693625:AAF9gRsL6SgTCg58CTWFz8cjGQfqk-WEIJ0')
bot.message_loop(handle)
print 'I am listening ...'

while 1:
    time.sleep(10)

