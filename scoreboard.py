import requests
import curses
import os
import time
import json
import threading

from ctfmodules.ctfclasses import CtfScoreboard
from ctfmodules.ctfclasses import ConsoleColors
from requests.auth import HTTPBasicAuth

############################################################################################
#Aliasies

clear = lambda: os.system('clear')

############################################################################################
#Globals

CTF_SCOREBOARD_URL = 'https://finalsim.cyberchallenge.it/ctf_scoreboard'
SCOREBOARD = ''
QUIT = False

stdscr = curses.initscr()

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

def curses_print_scoreboard_0(): 
    ##IDEA: inserisci solo un addstr per riga in modo da alleggerire il carico computazionale
    global stdscr

    __tab = 10
    __double_tab = __tab*2
    __half_tab = int(__tab/2)

    stdscr.addstr(0,0,'Round:' + str(SCOREBOARD.current_round), curses.color_pair(1))

    ### Main headers
    ctab = 0
    headers = ['Pos','Team','Score','Submitted','Stolen','Avg SLA']
    for head in headers:
        stdscr.addstr(1,ctab, head)
        if(len(head) > __tab):
            ctab += (len(head) - __tab) + 3
        ctab += __tab 

    #====
    stdscr.addstr(1,ctab, '||')
    #====

    ### Challenges headers
    ctab += __tab 
    for chall in SCOREBOARD.challenges_names:
        ctab -= __tab - 3
        stdscr.addstr(1, ctab, chall)
        if(len(chall) > __tab):
            ctab += (len(chall) - __tab) + 3
        ctab += __tab 
        headers = ['Captured','Lost','SLA','|']
        for head in headers:
            stdscr.addstr(1,ctab, head)
            if(len(head) > __tab):
                ctab += (len(head) - __tab) + 3
            ctab += __tab 

    row = 1
    for i in range(0, len(SCOREBOARD.team_names)):
        row += 1
        ctab = 0
        values =[] 

        values.append(str(i+1))
        values.append(str(SCOREBOARD.team_names[i]))
        values.append(str(int(SCOREBOARD.team_total_score(i))))
        values.append(str(SCOREBOARD.total_attack_flags(i)))
        values.append(str(SCOREBOARD.total_defense_flags(i)))
        values.append(str(int(SCOREBOARD.team_total_sla_percentage(i)))+'%')

        for value in values:
            stdscr.addstr(row,ctab, value)
            if(len(value) > __tab):
                ctab += (len(value) - __tab) + 3
            ctab += __tab 

        #====
        stdscr.addstr(row,ctab, '||')
        #====
        ctab += __tab 
        for serv in SCOREBOARD.challenges_names:
            ctab -= __tab - 3

            values =[] 
            values.append('?down?' if SCOREBOARD.team_challenge_integrity(i, serv) is False else '!up!')
            values.append(int(SCOREBOARD.team_challenge_attack_flags(i, serv)))
            values.append(int(SCOREBOARD.team_challenge_defense_flags(i, serv)))
            values.append(int(SCOREBOARD.team_challenge_sla_percentage(i, serv)))
            values.append('|')

            for value in values:
                if(type(value) is int):
                    if int(value) > 0:
                        if int(value) < 60:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(5))
                        elif int(value) < 80:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(4))
                        elif int(value) < 100:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(3))
                        elif int(value) == 100:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(2))
                        else:
                            stdscr.addstr(row,ctab, str(value))
                    else:
                        if int(value) == 0:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(2))
                        elif int(value) > -100:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(3))
                        elif int(value) >= -300:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(4))
                        elif int(value) < -300:
                            stdscr.addstr(row,ctab, str(value), curses.color_pair(5))
                        else:
                            stdscr.addstr(row,ctab, str(value))
                else:
                    if value == '?down?':
                        stdscr.addstr(row,ctab, value, curses.color_pair(5))
                    elif value == '!up!':
                        stdscr.addstr(row,ctab, value, curses.color_pair(3))
                    else:
                        stdscr.addstr(row,ctab, str(value))

                if(len(str(value)) > __tab):
                    ctab += (len(value) - __tab) + 3
                ctab += __tab 
        
def get_scoreboard_json(url, creds):
    try:
        return json.loads(requests.get(url, auth=HTTPBasicAuth(creds['email'], creds['password'])).text)
    except Exception as e:
        print("cred.json is not correctly formatted! [" + str(e) + "]" )
        quit()

def log_in():
    creds = ''
    while(True):
        try:
            creds = json.load(open("cred.json", 'r'))
            break
        except OSError:
            print('cred.json was not found! insert your credentials to continue:')
            print('email: ', end='')
            email = input()
            print('password: ', end='')
            password = input()
            f = open("cred.json", 'w+')
            f.write('{"email": "' + email + '", "password": "' + password + '"}')
            f.close()
            print('File cred.json created!')
    return creds

def log_out():
    os.remove('cred.json')

def init_window():
    #curses.noecho() #turn off automatic echoing of keys to the screen, in order to be able to read keys and only display them under certain circumstances
    curses.cbreak() #to react to keys instantly, without requiring the Enter key to be pressed
    stdscr.keypad(True) #Terminals usually return special keys as a multibyte escape sequence: enabling this, those key returns special values such as curses.KEY_LEFT
    stdscr.nodelay(True) #makes user inputs non-blocking
    curses.curs_set(0) #hides the cursor
    curses.start_color()

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #sets pairs of foreground/background colors
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  #sets pairs of foreground/background colors
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  #sets pairs of foreground/background colors
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  #sets pairs of foreground/background colors
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)  #sets pairs of foreground/background colors    

def end_window():
    curses.nocbreak()
    stdscr.keypad(False)
    stdscr.nodelay(False)
    curses.echo()
    curses.endwin() #restores the terminal to its original behaviour

def scoreboard_updater():
    global SCOREBOARD
    global QUIT
    global creds

    last_update = time.time() - 400
    while(QUIT is not True):
        if(time.time() - last_update >= 30):
            SCOREBOARD = CtfScoreboard(get_scoreboard_json(CTF_SCOREBOARD_URL, creds))
            last_update = time.time()
            update_screen(mode=0)

def update_screen(mode=0):
        stdscr.clear()
        #if there will be more than just one printing mode
        if(mode==0):
            curses_print_scoreboard_0()
        stdscr.refresh()

############################################################################################

def main():
    global SCOREBOARD
    global CTF_SCOREBOARD_URL
    global QUIT
    global updater
    global creds

    if(CTF_SCOREBOARD_URL == ''):
        print('Enter the scoreboard url: ', end='' )
        CTF_SCOREBOARD_URL = input()

    creds = log_in()

    SCOREBOARD = CtfScoreboard(get_scoreboard_json(CTF_SCOREBOARD_URL, creds))
    updater.start()
    init_window()

    while(QUIT is not True):
        ch = stdscr.getch()
        if ch == ord(' '):
            SCOREBOARD = CtfScoreboard(get_scoreboard_json(CTF_SCOREBOARD_URL, creds))
            update_screen()
        elif ch == ord('q'):
            QUIT = True
############################################################################################

if(__name__ == '__main__'):
    try:
        updater = threading.Thread(target=scoreboard_updater, name='updater_async') 
        creds = ''
        main()
        end_window()
        updater.join()
    except Exception as e:
        end_window()
        print(str(e))
