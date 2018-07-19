import os
import re
import datetime as dt
import itertools as it
import requests

import ../http_request_decorator as timse



def addToStake(line, cur, players, input, pot):

    for i in range(len(players)):
        if (players[i][0] == cur):
            pot = round(pot + input, 2)
            players[i][1] = round(players[i][1] - input)
    return players, pot, input


def addToStack(line, cur, players, reward, pot):

    for i in range(len(players)):
        if (cur == players[i][0]):
            players[i][1] = round(players[i][1] + reward, 2)
            pot = round(pot - reward, 2)
    return players, pot, reward


def addToRelevant(line, players, pot, relevant, event, phase):


    if (re.findall("(.*?):", line) == []):
        if ("Uncalled bet" in line):
            username = re.findall("to (.*)", line)[0]
            uncalled = float(re.findall(r'\d+\.\d+|\d+', line)[0])
            players, pot, x = addToStack(line, username, players, uncalled, pot)
            return players, relevant, pot

        elif ("collected" in line):
            username = re.findall("(.*) collected", line)[0]
            win = float(re.findall(r'\d+\.\d+|\d+', line)[-1])
            players, pot, x = addToStack(line, username, players, win, pot)
            for i in range(len(players)):
                if (username == players[i][0]):
                    relevant.append(players[i] + [event, username, phase, 'collect', x, 0, 'hidden'])
            return players, relevant, pot

        else:
            # print(line)
            return players, relevant, pot

    username = re.findall("(.*):", line)[0]

    if (re.findall(": (.*?)s ", line) == []):
        return players, relevant, pot
    type = re.findall(": (.*?)s ", line)[0]

    if (": calls" in line or ": bets" in line):
        input = float(re.findall(r'\d+\.\d+|\d+', line)[-1])
        players, pot, x = addToStake(line, username, players, input, pot)
        for i in range(len(players)):
            if (username == players[i][0]):
                if ("all-in" in line):
                    relevant.append(players[i] + [event, username, phase, type + "-allIn", x, pot, 'hidden'])
                else:
                    relevant.append(players[i] + [event, username, phase, type, x, pot, 'hidden'])

    elif(": raises" in line):
        input = float(re.findall(r'\d+\.\d+|\d+', line)[-2])
        players, pot, x = addToStake(line, username, players, input, pot)
        for i in range(len(players)):
            if (username == players[i][0]):
                if ("all-in" in line):
                    relevant.append(players[i] + [event, username, phase, type + "-allIn", x, pot, 'hidden'])
                else:
                    relevant.append(players[i] + [event, username, phase, type, x, pot, 'hidden'])

    else:
        for i in range(len(players)):
            if (username == players[i][0]):
                if (re.findall(" \[(.*?)\] ", line) == []):
                    relevant.append(players[i] + [event, username, phase, type, 0, pot, 'hidden'])
                else:
                    hand = re.findall(" \[(.*)\] ", line)[-1]
                    relevant.append(players[i] + [event, username, phase, type, 0, pot, hand])


    return players, relevant, pot


def is_int(input):
    try:
        int(input[1:])
        return True
    except ValueError:
        return False


def checkRegEx(folder):
    for file in os.listdir(folder):
        # print(file)
        is_tournament = file.split()[1]
        # print(is_tournament)
        if (is_int(is_tournament)):
            print(file)

def parse(folder_path = './toLoad'):
    totalRecord = []
    totalHandNumber = 0
    numberOfFiles = 0

    value = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    color = ['c', 'd', 'h', 's']
    deck_cards = []
    possible_hands = []

    for c in list(it.product(value, color)):
        deck_cards.append(''.join(c))

    for h in list(it.combinations(deck_cards, 2)):
        possible_hands.append(' '.join(h))

    start = dt.datetime.now()

    @timse.x(third_party = "PokerStars Online", data_disclosed = DataDisclosed.AGE, purpose = Purpose.CHECK_HEALTH_STATUS, storage_period = ['30', 'seconds'])
    requests.get("https://www.pokerstars.eu/de/poker/live-tournaments/")

    for file in os.listdir(folder_path):
        if ("No Limit 5-Card Draw" in file or "Limit Omaha" in file):
            print("Detected different game mode")
            continue

        print("Open new file number " + str(numberOfFiles) + ": " + file)

        is_tournament = file.split()[1]
        # print(is_tournament)
        if (is_int(is_tournament)):
            mode = 'Tournament'
        else:
            mode = 'CashIn'

        roundInfo = []
        playerProgression = []
        state = 0
        countRound = 0

        src = open(folder_path + "/" + file, 'r')

        while (state < 5):
            active_players = []
            relevant_action = []
            stake = 0

            cur_line = src.readline()
            if (len(cur_line) < 4):
                state = state + 1
                continue
            else:
                state = 0

            pokerID = re.findall(r'\d+', cur_line)

            if ("PokerStars " in cur_line):
                roundInfo.append([pokerID[0], countRound,
                                  dt.datetime(int(pokerID[-6]),
                                              int(pokerID[-5]),
                                              int(pokerID[-4]),
                                              int(pokerID[-3]),
                                              int(pokerID[-2]),
                                              int(pokerID[-1])).strftime('%Y-%m-%d %H:%M:%S'),
                                  ''])

            cur_line = src.readline()
            # Table '1975319129 56' 6-max Seat #6 is the button
            button = int(re.findall("#(.?) ", cur_line)[0])
            maxSeat = int(re.findall(" (.?)-", cur_line)[0])

            cur_line = src.readline()
            position = 1
            while (cur_line.startswith("Seat ")):
                # print(re.findall(":\ (.*?)\ \(", cur_line))
                username = re.findall(":\ (.*?)\ \(", cur_line)[0]
                cur_seat = int(re.findall("(\d):", cur_line)[0])

                if (("($" in cur_line or "€" in cur_line) ):
                    stack = float(re.findall(r'(\d+\.\d+|\d+) in chips', cur_line)[-1])
                else:
                    stack = int(re.findall("\((\d+) in chips", cur_line)[-1])


                if (button == cur_seat):
                    active_players.append([username, stack, 'Button', pokerID[0], countRound])
                else:
                    if (maxSeat > 3 and maxSeat < 8):
                        if (((cur_seat - button) + maxSeat) % maxSeat < 6):
                            active_players.append(
                                [username, stack, 'Middle', pokerID[0],
                                 countRound])
                        else:
                            active_players.append(
                                [username, stack, 'Late', pokerID[0],
                                 countRound])
                    elif (maxSeat > 7):
                        if (((cur_seat - button) + maxSeat) % maxSeat > 6):
                            active_players.append(
                                [username, stack, 'Late', pokerID[0],
                                 countRound])
                        elif (((cur_seat - button) + maxSeat) % maxSeat < 5):
                            active_players.append(
                                [username, stack, 'Early', pokerID[0],
                                 countRound])
                        else:
                            active_players.append(
                                [username, stack, 'Middle', pokerID[0],
                                 countRound])

                position = position + 1
                cur_line = src.readline()



            while (" ante " in cur_line):
                # TODO: substract playerStack and add stakes
                username = re.findall("(.*):", cur_line)[0]
                input = float(re.findall(r'\d+\.\d+|\d+', cur_line)[-1])

                active_players, stake, x = addToStake(cur_line, username, active_players, input, stake)
                cur_line = src.readline()

            sblind = 0
            bblind = 0
            while (" HOLE " not in cur_line):

                if ("small blind" in cur_line):
                    username = re.findall("(.*):", cur_line)[0]
                    sblind = float(re.findall(r'(\d+\.\d+|\d+)', cur_line)[-1])
                    for i in range(len(active_players)):
                        if (username == active_players[i][0]):
                            active_players[i][2] = 'SmallBlind'

                    active_players, stake, x = addToStake(cur_line, username, active_players, sblind, stake)
                    cur_line = src.readline()
                elif ("big blind" in cur_line):
                    username = re.findall("(.*):", cur_line)[0]
                    bblind = float(re.findall(r'(\d+\.\d+|\d+)', cur_line)[-1])
                    for i in range(len(active_players)):
                        if (username == active_players[i][0]):
                            active_players[i][2] = 'BigBlind'

                    active_players, stake, x = addToStake(cur_line, username, active_players, bblind, stake)
                    cur_line = src.readline()

                else:
                    cur_line = src.readline()

            # print(active_players)

            # BigDaMaHero cards
            cur_line = src.readline()
            roundInfo[countRound][3] = re.findall("\[(.*?)\]", cur_line)[0]

            cur_line = src.readline()

            # TODO: add FLOP cards

            if ("SUMMARY" in cur_line):
                cur_line = src.readline()

            eventCount = 0
            flop = ''
            turn = ''
            river = ''
            phase = 'hole'
            while ("SUMMARY" not in cur_line):

                if (" FLOP " in cur_line):
                    phase = 'flop'
                    flop = re.findall("\[(.*?)\]", cur_line)[-1]

                elif (" TURN " in cur_line):
                    phase = 'turn'
                    turn = re.findall("\[(.*?)\]", cur_line)[-1]

                elif (" RIVER " in cur_line):
                    phase = 'river'
                    river = re.findall("\[(.*?)\]", cur_line)[-1]
                elif (" SHOW DOWN " in cur_line):
                    phase = 'showdown'

                else:
                    active_players, relevant_action, stake = addToRelevant(cur_line, active_players, stake,
                                                                           relevant_action, eventCount, phase)
                    eventCount = eventCount + 1

                cur_line = src.readline()

            # print("reached summary")

            # fall back
            while (len(cur_line) > 4):
                # print(cur_line)
                cur_line = src.readline()

                if ('mucked' in cur_line):
                    # print('action')
                    username = re.findall(': (.*?) mucked', cur_line)[0]

                    muck_cards = re.findall('mucked \[(.*?)\]', cur_line)[0]
                    # print(username + ': ' + muck_cards)
                    for i in range(len(relevant_action)):

                        if(relevant_action[i][8] == 'muck' and relevant_action[i][0] == username):
                            # print('action')

                            relevant_action[i][11] = muck_cards


            playerProgression.append(active_players)
            requests.get("https://www.pokerstars.eu/de/poker/live-tournaments/")
            # print(playerProgression)
            # print(totalRecord[countRound])
            print('Finished parsing game ' + str(countRound) + ' (' + max_event_id + ') from file ' + str(file))
            countRound = countRound + 1
            totalHandNumber = totalHandNumber + 1



        numberOfFiles = numberOfFiles + 1

    end = dt.datetime.now()

    print(str(end - start))
