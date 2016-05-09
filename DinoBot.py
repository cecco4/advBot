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

class Node():
    def __init__(self, json):
        self.key   = json['key']
        self.name  = json['name']
        self.descr = json['descr']
        self.items = json['items']
        self.links = {}

    def __str__(self):
        return self.key + " " + self.name

class User():
    def __init__(self, chat_id, Pos):
        self.chat_id = chat_id
        self.pos = Pos
        

def handle(msg):
    global Users, Nodes
    
    chat_id = msg['chat']['id']
    command = msg['text']

    usr = None
    try:
        usr = Users[chat_id]
        print "Position: " + usr.pos.name
        
    except KeyError:
        usr = User(chat_id, Nodes['1'])
        Users[chat_id] = usr
        print "New user position: " + usr.pos.name
        
    print 'Got command: %s' % command

    command = command.lower()
    
    if command == 'look':
        bot.sendMessage(chat_id, usr.pos.name + "\n" + usr.pos.descr)
    else:
        try:
            newPos = usr.pos.links[command]
            usr.pos = newPos
            bot.sendMessage(chat_id, usr.pos.name + "\n" + usr.pos.descr)

        except KeyError:
            bot.sendMessage(chat_id, "Non conosco "+command)


print "loading world"
f = open('worlds/dt.txt', 'r')
data = json.loads(f.read())

Nodes = {}
Users = {}

for ndata in data['nodeDataArray']:
    n = Node(ndata)
    Nodes[n.key] = n
    print n

for ldata in data['linkDataArray']:
    if(ldata['text'] != None):
        print ldata['from'] + "->" + ldata['to'] + "  " + ldata['text']
        Nodes[ldata['from']].links[ldata['text']] = Nodes[ldata['to']]
        
    if(ldata['toText'] != None):
        print ldata['to'] + "->" + ldata['from'] + "  " + ldata['toText']
        Nodes[ldata['to']].links[ldata['toText']] = Nodes[ldata['from']]


bot = telepot.Bot('182693625:AAF9gRsL6SgTCg58CTWFz8cjGQfqk-WEIJ0')
bot.message_loop(handle)
print 'I am listening ...'

while 1:
    time.sleep(10)

