import requests
import curses
import os
import time
import json
from CtfScoreboard import CtfScoreboard
from ConsoleColors import ConsoleColors
from requests.auth import HTTPBasicAuth

############################################################################################
#Aliasies

clear = lambda: os.system('clear')

############################################################################################
#Globals

CTF_SCOREBOARD_URL = 'https://finalsim.cyberchallenge.it/ctf_scoreboard'
SCOREBOARD = ''
AUTH_CREDS = ''

############################################################################################

def format_scoreboard_0():
        
    board = '' #This will be printed at the end of the building

    board += ConsoleColors.UNDERLINE + ConsoleColors.HEADER + 'Round:' + str(SCOREBOARD.current_round) + ConsoleColors.ENDC + '\n'
    board += 'Pos'.center(5,' ')
    board += 'Team'.center(10,' ')
    board += 'Score'.center(10,' ')
    board += 'Submitted'.center(10,' ')
    board += 'Stolen'.center(10,' ')
    #list of total sla
    board += '||'.center(5,' ')
    for chall in SCOREBOARD.challenges_names:
        board +=  str(ConsoleColors.HEADER + chall + ':' + ConsoleColors.ENDC).center(20, ' ')
        board += 'Sub'.center(5,' ')
        board += 'Stol'.center(5,' ')
        board += 'Sla'.center(5,' ')
        board += '|'.rjust(2, ' ')
    board += '\n'

    for i in range(0, len(SCOREBOARD.team_names)):
        board += str(i+1).center(5,' ')
        board += str(SCOREBOARD.team_names[i]).center(10,' ')
        board += str(int(SCOREBOARD.team_total_score(i))).center(10,' ')
        board += str(SCOREBOARD.total_attack_flags(i)).center(10,' ')
        board += str(SCOREBOARD.total_defense_flags(i)).center(10,' ')
        #list of total sla
        board += '||'.center(5,' ')
        for serv in SCOREBOARD.challenges_names:
            status = (ConsoleColors.FAIL + '?down?') if SCOREBOARD.team_challenge_integrity(i, serv) is False else (ConsoleColors.OKBLUE + '!up!')
            board += str(status + ConsoleColors.ENDC).center(20, ' ')
            board += str(int(SCOREBOARD.team_challenge_attack_flags(i, serv))).center(5,' ')
            board += str(int(SCOREBOARD.team_challenge_defense_flags(i, serv))).center(5,' ')
            board += str(str(int(SCOREBOARD.team_challenge_sla_percentage(i, serv))) + "%").center(5,' ')
            board += '|'.rjust(2, ' ')
        board += '\n'
    return board

def get_scoreboard_json(url):
    try:
        return json.loads(requests.get(url, auth=HTTPBasicAuth(AUTH_CREDS['email'], AUTH_CREDS['password'])).text)
    except :
        print("cred.json is not correctly formatted!")
        return

############################################################################################

def main():
    global AUTH_CREDS
    global SCOREBOARD
    global CTF_SCOREBOARD_URL
    
    if(CTF_SCOREBOARD_URL == ''):
        print('Enter the scoreboard url: ', end='' )
        CTF_SCOREBOARD_URL = input()

    try:
        AUTH_CREDS = json.load(open("cred.json"))
        SCOREBOARD = CtfScoreboard(get_scoreboard_json(CTF_SCOREBOARD_URL))
        while(True):
            SCOREBOARD = CtfScoreboard(get_scoreboard_json(CTF_SCOREBOARD_URL))
            print(format_scoreboard_0())
            time.sleep(3)
    except OSError:
        print('cred.json is missing')

############################################################################################

if(__name__ == '__main__'):
    main()