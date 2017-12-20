#!/usr/bin/python3

def memo(func):
    s = {}
    def g(*args):
        if not args in s:
            s[args] = func(*args)
        return s[args]
    return g


def valid(num):
    for i in range(4):
        if 1 <= num % 10 <= 6:
            num //= 10
        else:
            return False
    return True


def getarray(num):
    value = []
    for i in range(4):
        value.append(num % 10)
        num //= 10
    return value


def getmissmatch(num1, num2):
    a1 = getarray(num1)
    a2 = getarray(num2)

    black = 0
    white = 0

    for i in range(4):
        if a1[i] == a2[i]:
            black += 1
            a1[i] = -1
            a2[i] = -1

    for i in range(4):
        if a1[i] == -1: continue

        for j in range(4):
            if a1[i] == a2[j]:
                white += 1
                a2[j] = -1
                break

    return black, white


def choose(candidates, good):
    minmax = len(good)
    bestchoice = -1

    for num in sorted(good):
        nmap = {}
        for x in candidates:
            value = getmissmatch(num, x)
            if not value in nmap:
                nmap[value] = 0
            nmap[value] += 1

        curmax = 0
        for t in nmap:
            curmax = max(curmax, nmap[t])

        if curmax < minmax:
            bestchoice = num
            minmax = curmax

    return bestchoice


def filter(num, candidates, answer):
    ncandidates = set()

    for x in candidates:
        if getmissmatch(num, x) == answer:
            ncandidates.add(x)

    return ncandidates


game = {}


def play(adversary, verbose=True):
    # Global variable game to keep track of
    # valid options
    global game

    good = {i for i in range(6667) if valid(i)}
    candidates = good

    moves = 0

    while len(candidates) > 1:
        if moves == 0:
            num = 1122
        elif moves == 1:
            cur = (white, black)

            if not cur in game:
                game[cur] = choose(candidates, good)

            num = game[cur]
        else:
            num = choose(candidates, good)

        moves += 1
        white, black = adversary(num)
        candidates = filter(num, candidates, (white, black))

        if verbose:
            print("INFO: Number of remaining candidates:", len(candidates))

    if len(candidates) == 0:
        print("""
    There is no valid candidates for your sequence of responses.
    If you think something is wrong report this as an issue with details
    of the game. I'll be glad to fix it""")
    else:
        answer = list(candidates)[0]

        moves += 1

        if verbose:
            print("==============")
            print("Your number is {}".format(answer))
            print("Solution found in {} steps".format(moves))

    return moves


invalid_option = """
    Invalid option: {}

    Type `help` for some help.
"""

help_message = """
    For example if you think number
    1123 and machine guess number 1431
    you should answer (black pegs, white pegs):

    > 2 1

    There is one white peg since only correct
    number is number 1 in the first position
    and the number 3 and 1 are good colors
    but in bad positions.
"""


def user(num):
    """ Interface for a human player
    """
    while True:
        print("Option: {}".format(num))

        line = input()

        try:
            if line[0] == 'h':
                print(help_message)
            else:
                white, black = map(int, line.split())
                return white, black
        except:
            print(invalid_option.format(line))


def think(answer):
    def adversary(num):
        """ Interface for a machine that choose
            `answer` as the target number
        """
        return getmissmatch(answer, num)
    return adversary


def test():
    top = 0
    for i in range(10**4):
        if valid(i):
            print()
            print("Start:", i)
            cur = play(think(i), False)
            top = max(cur, top)
            print("answer:{} moves:{} max_moves:{}".format(i, cur, top))


init_message = """
    Mastermind Predictor
    ====================

    Learn about the game in wikipedia
    https://en.wikipedia.org/wiki/Mastermind_(board_game)

    Think in a four digit number where each digit must
    be between 1 and 6 (They represent the colors)

    Gameplay

    After each question of the predictor you should
    answer with two numbers. The number of black pegs
    and the number of white pegs.
"""

def main():
    print(init_message)

    play(user)
    # test()

if __name__ == '__main__':
    main()
