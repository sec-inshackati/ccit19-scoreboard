import requests
import os
import sys
#import curses
import _thread
import time
import json
from requests.auth import HTTPBasicAuth

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

############################################################################################
#Aliasies
clear = lambda: os.system('clear')

############################################################################################
#Globals
CTF_COREBOARD_URL = 'https://finalsim.cyberchallenge.it/ctf_scoreboard'
SCOREBOARD = ''
with open('cred.json') as f: 
    credentials = json.load(f)

#===========================================================================================
#=Methods:

###Check data
def total_lost_flags(services):
    sum = 0
    for i in range(0, len(services)):
        sum -= services[i]['defense_flags']
    return sum

def total_submitted_flags(services):
    sum = 0
    for i in range(0, len(services)):
        sum += services[i]['attack_flags']
    return sum

def total_sla(services):
    sum = 0
    for i in range(0, len(services)):
        sum -= services[i]['sla']
    return sum

def total_lost(services):
    sum = 0
    for i in range(0, len(services)):
        sum -= services[i]['defense']
    return sum

def total_scored(services):
    sum = 0
    for i in range(0, len(services)):
        sum += services[i]['attack']
    return sum

def check_integrity(service):
    return service['integrity']['status']

###========================================

def print_scoreboard(scoreboard):
    
    board = '' #This will be printed at the end of the building

    round_number = scoreboard['round']
    team_statistics = scoreboard['scores']
    
    list_of_services = [key for key in scoreboard['scores'][0]['services']]
    list_of_submitted = [] #total submitted of each team
    list_of_stolen = [] #total stolen from each team

    # list_of_teams = []  #team names 
    # list_of_total_scores = [] #total score for each team
    # list_of_service_info = []
    
    for i in range(0, len(team_statistics)): #for each team
        # list_of_teams.append(team_statistics[i]['name']) #add the team name to the list
        # list_of_total_scores.append(team_statistics[i]['score']) #add the total score of the team to the list
        list_of_submitted.append(0) #append new object of totatl flags submitted
        list_of_stolen.append(0) #append new object of totatl flags that have been stolen (FROM the team)
        for serv_key in scoreboard['scores'][i]['services']: #for each challenge (service)
            list_of_submitted[i] += int(scoreboard['scores'][i]['services'][serv_key]['attack_flags']) #add to the total submitted flags
            list_of_stolen[i] += -int(scoreboard['scores'][i]['services'][serv_key]['defense_flags']) #add to the total stolen flags
    #ljust
    board += bcolors.UNDERLINE +bcolors.HEADER + bcolors.BOLD + 'Round:' + str(round_number) + bcolors.ENDC + '\n'
    board += 'Pos'.center(5,' ')
    board += 'Team'.center(10,' ')
    board += 'Score'.center(10,' ')
    board += 'Submitted'.center(10,' ')
    board += 'Stolen'.center(10,' ')
    #list of total sla
    board += '||'.center(5,' ')
    for serv in scoreboard['scores'][i]['services']:
        board +=  str(bcolors.HEADER + serv + ':' + bcolors.ENDC).center(20, ' ')
        board += 'Sub'.center(5,' ')
        board += 'Stol'.center(5,' ')
        board += 'Sla'.center(5,' ')
        board += '|'.rjust(2, ' ')
    board += '\n'

    for i in range(0, len(team_statistics)):
        board += str(i+1).center(5,' ')
        board += str(scoreboard['scores'][i]['name']).center(10,' ')
        board += str(int(scoreboard['scores'][i]['score'])).center(10,' ')
        board += str(list_of_submitted[i]).center(10,' ')
        board += str(list_of_stolen[i]).center(10,' ')
        #list of total sla
        board += '||'.center(5,' ')
        for serv in scoreboard['scores'][0]['services']:
            status = (bcolors.FAIL + '?down?') if scoreboard['scores'][i]['services'][serv]['integrity']['status'] is False else (bcolors.OKBLUE + '!up!')
            board += str(status + bcolors.ENDC).center(20, ' ')
            board += str(int(scoreboard['scores'][i]['services'][serv]['attack_flags'])).center(5,' ')
            board += str(int(scoreboard['scores'][i]['services'][serv]['defense_flags'])).center(5,' ')
            board += str(int(scoreboard['scores'][i]['services'][serv]['sla'])).center(5,' ')
            board += '|'.rjust(2, ' ')
        board += '\n'
    print(board)
    #status = check_integrity(list_of_services[serv_key]) #check integrity
    #submitted = list_of_services[serv_key]['attack_flags'] #get flag submitted for that challenge
    #stolen = -list_of_services[serv_key]['defense_flags'] #get flag stolen from that challenge
            

def get_scoreboard(url):
    response = requests.get(url, auth=HTTPBasicAuth(credentials['username'], credentials['password'])).text
    return json.loads(response)

#===========================================================================================

def update_scoreboard():
    while(True):
        time.sleep(2)
        SCOREBOARD = get_scoreboard(CTF_COREBOARD_URL)

def main():
    _thread.start_new_thread(update_scoreboard, ())
    SCOREBOARD = get_scoreboard(CTF_COREBOARD_URL)
    while(True):
        print_scoreboard(SCOREBOARD)
        #window.refresh()
        time.sleep(1)
        clear()
        
        ##sys.stdout.flush()

#############################################################################################

if(__name__ == '__main__'):
    #stdscr = curses.initscr()
    #curses.wrapper(main)
    main()
