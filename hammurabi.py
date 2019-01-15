########################################################
#
# Hammurabi
#
# From: BASIC Computer Games (1978)
#       Edited by David Ahl
#
# In this game you direct the administrator of Sumeria,
# Hammurabi, how to manage the city. The city initially
# has 1,000 acres, 100 people and 3,000 bushels of grain
# in storage.
#
# You may buy and sell land with your neighboring
# city-states for bushels of grain--the price will vary
# between 17 and 26 bushels per acre. You also must use
# grain to feed your people and as seed to plant the
# next year's crop.
#
# You will quickly find that a certain number of people
# can only tend a certain amount of land and that people
# starve if they are not fed enough. You also have the
# unexpected to contend with such as a plague, rats
# destoying stored grain, and variable harvests.
#
# You will also find that managing just the few
# resources in this game is not a trivial job over a
# period of say ten years. The crisis of population
# density rears its head very rapidly.
#
# This program was originally written in Focal at DEC;
# author unknown. David Ahl converted it to BASIC and
# added the 10-year performance accessment [sic]. If
# you wish to change any of the factors, the extensive
# remarks in the program should make modification
# farily straightforward.
#
# Note for trivia buffs: somewhere along the line an m
# was dropped out of the spelling of Hammurabi in the
# Ahl version of the computer program. This error has
# spreadh far and wide until a generation of students
# who have used this program now think that Hammurabi
# is the incorrect spelling.
#
# [Note that the above description was taken from the
#  1978 edition of the book. The original author of
#  the Focal version of this game is now known to be
#  Doug Dyment, who created the program in 1968 and
#  called it "The Sumer Game".
#
# Python port by Jeff Jetton. 
#
########################################################


import random

# Game contants
MAX_YEARS = 10    # How many years should the game last?
STARTING_BASE_POP = 95
STARTING_INCOMING_POP = 5
STARTING_ACRES = 1000
STARTING_YIELD = 3
STARTING_RAT_LOSS = 200

# Display initial title and instructions
print("\n               Hamurabi")
print("Creative Computing  Morristown, New Jersey")
print("\n\n\n")
print("Try your hand at governing ancient Sumeria")
print("for a ten-year term of office.\n")

# Initialize game variables
deathTotal = 0          # D1
starvationPct = 0       # P1
year = 1                # Z
population = STARTING_BASE_POP          # P
acres = STARTING_ACRES                  # A
yieldPerAcre = STARTING_YIELD           # Y
harvestYield = acres * yieldPerAcre     # H
# Initial bushel store takes rat loss into account
ratLoss = STARTING_RAT_LOSS             # E
bushelStore = harvestYield - ratLoss    # S
starved = 0                             # D
incomingPop = STARTING_INCOMING_POP     # I
impeached = False


# Main game loop. Game runs until we've reached MAX_YEARS
# or the player has been impeached.

while year <= MAX_YEARS and not impeached:
    
    print("\n\n\nHamurabi: I beg to report to you,")
    print("in year %s , %s people starved, %s came to the city,"
          %(year, starved, incomingPop))
    # Calculate current-year population
    population += incomingPop
    print("Population is now %s"%population)
    print("The city now owns %s acres."%acres)
    print("You harvested %s bushels per acre."%yieldPerAcre)
    print("Rats ate %s bushels."%ratLoss)
    print("You now have %s bushels in store.\n"%bushelStore)
    
    
    
    
    
    impeached = True
    
    
    
  
  
  

########################################################
#
# Porting notes:
#
#   The origin
#
#
# Ideas for Modifications
#
#   
#
########################################################


            
        
    

    
