# -*- coding: utf-8 -*-
"""
Subtract-a-square mathematical strategy game
implemented in Python

This is a "smart" version, which computes the quickest way to win
and then plays that move.

I don't know if I solved the game or not.
"""
import random
import time

NEWPLAYER = True
NORMALPLAY = True

RULES = """This is the Subtract-a-square game.
The rules are as follows:
 - A number is selected
 - You are asked if you want to go first
 - You enter a number
 - The square of that number is deducted from the selected number
 - The computer selects and deducts a square from the number
 - The process is repeated
 - Whoever completes that last move wins
"""  # in case we got a nub playing this


def sqrt(num):
    """
    Return the largest integer whose square is less than the parameter
    """
    return int(num ** 0.5)


def losing(num):
    """
    Determines whether it is a winning or a losing position
    """
    if not hasattr(losing, 'memo'):  # provides HUGE performance boosts
        losing.memo = {0: False}
    if num in losing.memo:
        return losing.memo[num]
    else:
        all_moves = [num - i**2 for i in range(1, sqrt(num)+1)]
        losing.memo[num] = filter(lambda x: not losing(x), all_moves) != []
    return losing.memo[num]


def find_winning(num):
    """
    Finds all the numbers from the given one
    that can win the game
    """
    return filter(lambda x: not losing(x),  # not losing == winning, right?
                  [num-i*i for i in range(sqrt(num)+1)])


def declare_number():  # basically just a macro
    print "The number is {}.".format(initial)


initial = random.normalvariate(5000, 750)  # basically never get a small number
initial = int(initial)
# to expand losing.memo
if NEWPLAYER:
    print RULES
begin = time.clock()
count = 10
while count < 10500:  # 10500 is an auspicious number
    losing(count)     # it misses < 0.0000000001% of cases, no jokes
    count += 10       # incrementing in tens seems to be the fastest
end = time.clock() - begin  # rudimentary timing, works though
if NEWPLAYER:
    time.sleep(10 - end)  # to read the rules and comprehend
print "Memoization took {} seconds.".format(end)

# losing.memo should be big enough now
player_first = 'n' not in raw_input("Wanna go first? ")
declare_number()
if not player_first:
    if not NEWPLAYER:  # EXTREAM DIFFICULTY!!!
        small_win = initial - find_winning(initial)[-1]  # quickest win
        small_win = small_win if small_win else 1  # we can't be subtracting 0
    else:  # newbie play
        small_win = sqrt(initial)**2  # largest square, guaranteed to not be 0
    print "Subtracting {}^2 = {}.".format(sqrt(small_win), small_win)
    initial -= small_win
    declare_number()

while initial > 0:
    # player's turn
    number = int(float(raw_input("Enter the square you want to subtract. ")))
    if number ** 2 > initial:  # the cheek!
        print "Too big, assuming you meant {}.".format(sqrt(initial))
        number = sqrt(initial)
    if number < 1:  # must not be zero, don't get any clever ideas
        number = 1
    print "Subtracting {}^2 = {}.".format(number, number ** 2)
    initial -= number ** 2  # the customer is always right?
    if not initial:
        player_won = NORMALPLAY  # ughhhhh
        break  # now
    declare_number()
    # computer's turn
    if not NEWPLAYER:
        small_win = initial - find_winning(initial)[-1]  # quickest win
    else:
        small_win = sqrt(initial)**2  # largest square
    initial -= small_win
    print "Subtracting {}^2 = {}.".format(sqrt(small_win), small_win)
    declare_number()
    if not initial:
        player_won = not NORMALPLAY  # we win!

if player_won:
    print "Congratulations! You won!"  # we gotta be kind, you know
else:
    print "Better luck next time!"  # snicker, snicker
