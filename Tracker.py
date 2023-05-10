import asyncio
import warnings
from roblox import Client
import time
import requests
warnings.filterwarnings("ignore", category=DeprecationWarning) 
try:
    f = open("ids.txt", "r")
    print("Read file",f.name)
except IOError:
    print('File "ids.txt" does not exist. Please ensure there is a file in the same directory named ids.txt, and restart if the file exists')
    time.sleep(9e5)
lines = f.readlines()
totrack = []
for line in range(len(lines)):
    lines[line].strip()
    try:
        totrack.append(int(lines[line]))
    except:
        print("Error parsing value "+lines[line].strip()+" at line "+str(line+1)+". Ensure it is a player ID")
f.close()
oldstatus = [None]*len(totrack)
try:
    f2 = open("info.txt", "r")
    print('Read file',f2.name)
except IOError:
    print('File "info.txt" does not exist. Please ensure there is a file in the same directory named info.txt, and restart if the file exists')    
url = f2.readline().strip()
cookie = f2.readline().strip()
client = Client(cookie)
print("Webhook URL:",url)
print("Cookie:",cookie)
print("Users being tracked:",end=" ")
for i in range(len(totrack)-1):
    print(totrack[i],end=", ")
print(totrack[len(totrack)-1]) 

async def main():
    global oldstatus
    global totrack
    global url
    print("Tracker Running")
    while True:
        try:
            f = open("ids.txt", "r")
        except IOError:
            print('File "ids.txt" does not exist. Please ensure there is a file in the same directory named ids.txt, and restart if the file exists')
            time.sleep(9e5)
        lines = f.readlines()
        totrack = []
        for line in range(len(lines)):
            lines[line].strip()
            try:
                totrack.append(int(lines[line]))
            except:
                print("Error parsing value "+lines[line].strip()+" at line "+str(line+1)+". Ensure it is a player ID")
        f.close()
        templist = []
        templist2 = []
        counter=-1
        if len(totrack) > len(oldstatus):
            print("List Updated")
            for i in range(len(totrack)-len(oldstatus)):
                totrack.append(None)
        elif len(totrack) < len(oldstatus):
            print("List Updated")
            oldstatus = [None]*len(totrack)
        for i in totrack:
            counter+=1
            user = await client.get_user(i)
            presence = await user.get_presence()
            ingame = str(presence.user_presence_type)
            ingame = ingame.split(".")
            if presence.place != None:
                currgame = presence.place.id
                gameinfo = await client.get_place(currgame)
            if oldstatus[counter] != None and oldstatus[counter] != ingame[1]:
                if ingame[1] != "in_game":
                    requests.post(url,json={"content":user.name+" is now "+ingame[1]})
                else:
                    if presence.place != None:
                        requests.post(url,json={"content":user.name+" is now in game. Game: "+str(gameinfo.name)})    
                    else:
                        requests.post(url,json={"content":user.name+" is now in game, but they have joins off."})
            templist.append(ingame[1])
        oldstatus = templist
        time.sleep(15)  

asyncio.get_event_loop().run_until_complete(main())
