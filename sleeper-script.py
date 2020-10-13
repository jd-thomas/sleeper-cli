import json
import csv
import requests
import argparse
import pickle
import os

#command line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--league", help="Enter your league number", type=str)
parser.add_argument("-r", "--refresh", help="refresh master player list. Do not use more than once per day", action="store_true")
parser.add_argument("-m", "--maxroster", help="maximum roster size for your league", type=int)
parser.add_argument("-s", "--save", help="save league number and roster size as defaults", action="store_true")
args = parser.parse_args()

#check if data folder exists and make it if not
if not os.path.exists('sleeper-data'):
    os.makedirs('sleeper-data')

#Download master list if -r is called.  Do not use more than once per day
#Get Master list function
def get_master_list():
    p = requests.get('https://api.sleeper.app/v1/players/nfl')
    with open('sleeper-data/players.json','w') as pout:
        pout.write(p.text)

if args.refresh:
    print("Downloading master list...")
    get_master_list()

try: 
    with open('sleeper-data/user-options', 'rb') as g:
      options = pickle.load(g)
except FileNotFoundError:
    print("No user data detected. To save defaults run with -s.")

#Input league values or retrieve defaults
if args.league:
    league = args.league
else:
    league = options['league']
#Give error if league is not found and exit
ltest = requests.get('https://api.sleeper.app/v1/league/'+ league)
if ltest.status_code == 404:
    print("No league found with this number. Try again with sleeper-cli -l and a proper number")
    exit()
    
#Input roster length values or retrieve defaults
if args.maxroster:
    maxroster = args.maxroster
else:
    maxroster = options['maxroster']

#save user options if -s called
if args.save:
    with open('sleeper-data/user-options', 'wb') as g:
        options = {
            'league': args.league,
            'maxroster': args.maxroster  
        }
        pickle.dump(options, g)
        
#Update league list function
def update_league_lists():
    #full rosters
    r = requests.get('https://api.sleeper.app/v1/league/'+ league +'/rosters')
    with open('sleeper-data/rosters.json','w') as rout:
        rout.write(r.text)
        
    #owner information
    ow = requests.get('https://api.sleeper.app/v1/league/'+ league +'/users')
    with open('sleeper-data/owners.json','w') as ownout:
        ownout.write(ow.text)

update_league_lists()


#Load league owner and names data
with open('sleeper-data/owners.json') as h:
  names = json.load(h)
  
#Load master player list
try: 
    with open('sleeper-data/players.json') as g:
      playermaster = json.load(g)
    players = list(playermaster.values())
except FileNotFoundError:
    print("No master player list found. You need to run with -r at least once to retrieve the master list. (Do not run with -r more than once per day.)")
    exit()
    
#load league rosters
with open('sleeper-data/rosters.json') as f:
  rosters = json.load(f)

# Output
final_list = []

# print names of players from roster list
def pfunction():
    plist = rosters[get_players]["players"]
    pcount = 0
    plen = maxroster
    while pcount < plen:
        try:
            r = plist[pcount] #iterate this
            get_pname = next((index for (index, d) in enumerate(players) if d["player_id"] == r), None)
            pname = players[get_pname]["first_name"] +' '+ players[get_pname]["last_name"], players[get_pname]["position"]
            rlist.append(pname)
            pcount = pcount + 1
        except:
            rlist.append('null')
            pcount = pcount + 1
    else: 
        final_list.append(rlist)


#print owner name, call pfunction, add players to list and final list
qcount = 0;
qlen = len(rosters)
while qcount < qlen:
    q = rosters[qcount]["owner_id"] #iterate this
    rlist = []
    get_index = next((index for (index, d) in enumerate(names) if d["user_id"] == q), None)
    owner = names[get_index]["display_name"]
    rlist.append(owner)
    get_players = next((index for (index, d) in enumerate(rosters) if d["owner_id"] == q), None)
    
    pfunction()
    
    qcount = qcount + 1
else: 
    print('All done! Check sleeperleague.csv')

#changes data from rows to columns and outputs to csv
ziplist = zip(*final_list)
with open("sleeperleague.csv", "w", newline="") as j:
    writer = csv.writer(j)
    writer.writerows(ziplist)
