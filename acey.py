########################################################
#
# Acey Ducey
#
# From: BASIC Computer Games (1978)
#       Edited by David Ahl
#
# This is a simulation of the Acey
# Ducey card game. In the game, the
# dealer (the computer) deals two cards
# face up. You have an option to bet or
# not to bet depending on whether or not
# you feel the next card dealt will have
# a value between the first two.
#
# Your initial money is set to $100. 
# The game keeps going on until you
# lose all your money or interrupt the
# program.
#
# The original BASIC program author was
# Bill Palmby of Prairie View, Illinois.
#
# Python port by Jeff Jetton
#
########################################################

import random


# functions
def dealCardNum():
    return random.randint(0, 12)

def getCardName(n):
    cardNames = (" 2", " 3", " 4", " 5", " 6", \
                 " 7", " 8", " 9", " 10", "Jack", \
                 "Queen", "King", "Ace")
    return(cardNames[n])

def displayBankroll(b):
    print("You now have %s dollars\n"%b)
    


# Display initial title and instructions
print("\n           Acey Ducey Card Game")
print("Creative Computing  Morristown, New Jersey")
print("\n\n\n")
print("Acey-Ducey is played in the following manner")
print("The dealer (computer) deals two cards face up")
print("You have an option to bet or not bet depending")
print("on whether or not you feel the card will have")
print("a value between the first two.")
print("If you do not want to bet, input a 0")

# Initialize bankroll. You may alter this statement
# if you want to start with more or less than $100.
bankroll = 100

# Start the game by displaying the starting bankroll
displayBankroll(bankroll)

# Main game loop. Repeat until out of money.
while bankroll > 0:

    # Deal out dealer cards
    print("Here are your next two cards")
    dealer1 = dealCardNum()
    # If the cards match, we re-deal until they don't
    dealer2 = dealer1
    while dealer1 == dealer2:
        dealer2 = dealCardNum()
    # Organize the cards in order if they're not already
    if (dealer1 >= dealer2):
        (dealer1, dealer2) = (dealer2, dealer1)
    # Show cards to the player (using name rather than number)
    print(getCardName(dealer1))
    print(getCardName(dealer2) + "\n")

    # Get and handle player bet choice
    betIsValid = False
    while not betIsValid:
        currBet = int(input("\nWhat is your bet? "))
        if currBet == 0:
            betIsValid = True
            print("Chicken!!\n")
        elif currBet > bankroll:
            print("Sorry, my friend but you bet too much")
            print("You have only %s dollars to bet"%bankroll)
        else:
            # Deal player card
            betIsValid = True
            player = dealCardNum()
            print(getCardName(player) + "\n")
            
            # Did we win?
            if player > dealer1 and player < dealer2:
                print("You win!!!")
                bankroll += currBet
            else:
                print("Sorry, you lose")
                bankroll -= currBet

            # Update player on new bankroll level
            displayBankroll(bankroll)
            
    # End of main game loop

print("\n\nSorry, friend but you blew your wad")
print("TRY AGAIN CODE GOES HERE")
print("OK Hope you had fun")
                    

########################################################
#
# Ideas for Modifications
#
#   Give the user the ability to quit the game, perhaps
#   by typing "quit" instead of making a bet. Provide a
#   final assement based on how much of the original
#   bankroll they have left.
#
#   Or have the game run for a set number of rounds or
#   until a certain bankroll goal is attained.
#
#   Notice that the player can "bet" a negative amount,
#   which will result in earning money if the bet loses
#   and losing money if it wins! How would you fix this
#   lack of input validation?
#
#   When the player "chickens out", show them what the
#   next card would've been and point out whether they
#   made a good or bad decision.
# 
#   Instead of calling the player "chicken" every time
#   they opt out of betting, how about random taunts?
#
#   In what situations are the odds of winning high
#   enough to justify making a bet? Create a cheat mode
#   where the program identifies these situations and
#   lets the player know.
#
#   Change the card dealing to simulate deals from a
#   single deck (or a user-selectable number of decks).
#
#   Implement a two-player mode where players take turns
#   betting (or both bet on the same dealer cards).
#
########################################################

########################################################
# Porting notes:
#
#   The original BASIC version had a variable named N
#   that was initialized to 100 and then never used.
#   Maybe it was used in feature that was edited out of
#   the final version used in the book? (Such as tracking
#   a set number of rounds?)
#
#   The card value printing logic was originally
#   repeated three times: Once for the two dealer
#   cards and again for the player card. This has
#   been broken out into a single, reused function.
#
#   The OP simply generated random numbers for each
#   card. It did not simulate a true card deck, where
#   the dealing of a card d eliminates it from the
#   deck and reduces the chances of the same value
#   being drawn. This "infinite" deck logic has
#   been maintained.
#
#   The OP allowed negative bets, which would
#   earn you money if you lost! Same here.
#
#   Card values are internally different from card name.
#   Could the RNG in the OP produce out-of-bounds values?
#   No validation on the input. Could be character, etc.
#
#
########################################################
            
        
    

    
