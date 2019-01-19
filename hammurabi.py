########################################################
#
# Hammurabi
#
# From: BASIC Computer Games (1978)
#       Edited by David Ahl
#
# "In this game you direct the administrator of Sumeria,
#  Hammurabi, how to manage the city. The city initially
#  has 1,000 acres, 100 people and 3,000 bushels of
#  grain in storage.
#
# "You may buy and sell land with your neighboring
#  city-states for bushels of grain--the price will vary
#  between 17 and 26 bushels per acre. You also must use
#  grain to feed your people and as seed to plant the
#  next year's crop.
#
# "You will quickly find that a certain number of people
#  can only tend a certain amount of land and that
#  people starve if they are not fed enough. You also
#  have the unexpected to contend with such as a plague,
#  rats destoying stored grain, and variable harvests.
#
# "You will also find that managing just the few
#  resources in this game is not a trivial job over a
#  period of say ten years. The crisis of population
#  density rears its head very rapidly.
#
# "This program was originally written in Focal at DEC;
#  author unknown. David Ahl converted it to BASIC and
#  added the 10-year performance accessment [sic]. If
#  you wish to change any of the factors, the extensive
#  remarks in the program should make modification
#  farily straightforward.
#
# "Note for trivia buffs: somewhere along the line an m
#  was dropped out of the spelling of Hammurabi in the
#  Ahl version of the computer program. This error has
#  spreadh far and wide until a generation of students
#  who have used this program now think that Hammurabi
#  is the incorrect spelling."
#
# Note that the above description was taken from the
# 1978 edition of the book. The original author of
# the Focal version of this game is now known to be
# Doug Dyment, who created the program in 1968 and
# called it "The Sumer Game".
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
BUSHELS_PER_ACRE_TO_PLANT = 0.5
ACRES_TENDED_PER_FARMER = 10


# Functions
def negative_response():
    print("\nHamurabi:  I cannot do what you wish.")
    print("Get yourself another steward!!!!!")
    
def not_enough_bushels(bushels):
    print("Hamurabi:  Think again.  You have only")
    print("%s bushels of grain.  Now then,"%bushels)


# Initialize game variables
death_total = 0          # D1
starvation_pct = 0       # P1
year = 1                # Z
population = STARTING_BASE_POP          # P
acres = STARTING_ACRES                  # A
yield_per_acre = STARTING_YIELD         # Y
harvest_yield = acres * yield_per_acre  # H
# Initial bushel store takes rat loss into account
rat_loss = STARTING_RAT_LOSS             # E
bushel_store = harvest_yield - rat_loss   # S
starved = 0                             # D
incoming_pop = STARTING_INCOMING_POP    # I


# Display initial title and instructions
print("\n               Hamurabi")
print("Creative Computing  Morristown, New Jersey")
print("\n\n\n")
print("Try your hand at governing ancient Sumeria")
print("for a ten-year term of office.\n")


# Main game loop.
game_running = True
while game_running:
    
    print("\n\n\nHamurabi: I beg to report to you,")
    print("in year %s , %s people starved, %s came to the city,"
          % (year, starved, incoming_pop))
    # Calculate current-year population
    population += incoming_pop
    print("population is now %s" % population)
    print("The city now owns %s acres." % acres)
    print("You harvested %s bushels per acre." % yield_per_acre)
    print("Rats ate %s bushels."%rat_loss)
    print("You now have %s bushels in store.\n" % bushel_store)
    # Determine current price per acre (in bushels)
    acre_price = random.randint(0, 9) + 17
    print("Land is trading at %s bushels per acre." % acre_price)
    
    # Get acre purchase choice
    valid_response = False
    while not valid_response:
        acre_purchase = int(input("How many acres do you wish to buy "))
        total_cost = acre_purchase * acre_price
        if acre_purchase < 0:
            negative_response()
            valid_response = True
            game_running = False
        elif total_cost > bushel_store:
            not_enough_bushels(bushel_store)
        elif acre_purchase == 0:
            valid_response = True
            print("TODO: Handle zero purchase (ask for sales)")
        else:
            valid_response = True
            acres += acre_purchase
            bushel_store -= total_cost
    
    # Assuming the acre purchasing went well, get feeding choice
    if game_running:
        valid_response = False
        while not valid_response:
            feed_choice = int(input("How many bushels do you wish to feed your people "))
            if feed_choice < 0:
                negative_response()
                valid_response = True
                game_running = False
            # "*** Trying to use more grain than is in silos?"
            elif feed_choice > bushel_store:
                not_enough_bushels(bushel_store)
            else:
                valid_response = True
                bushel_store -= feed_choice
                print("")
                
    # Still playing? Get planting choice
    if game_running:
        valid_response = False
        while not valid_response:
            plant_acres = int(input("How many acres do you wish to plant with seed "))
            plant_cost = int(plant_acres * BUSHELS_PER_ACRE_TO_PLANT)
            if plant_acres < 0:
                negative_response()
                valid_response = True
                game_running = False
            # "*** Trying to plan more acres than you own?"
            elif plant_acres > acres:
                print("Hamurabi:  Think again.  You own only %s acres.  Now then,"
                      % acres)
            # "*** Enough grain for seed?"
            elif plant_cost > bushel_store:
                not_enough_bushels(bushel_store)
            # "*** Enough people to tend the crops?"
            elif plant_acres > ACRES_TENDED_PER_FARMER * population:
                print("But you have only %s people to tend the fields!  Now then,"
                      % population)
            else:
                valid_response = True
                bushel_store -= plant_cost
                
                # "*** A bountiful harvest!"
                yield_per_acre = random.randint(1, 5)
                harvest_yield = plant_acres * yield_per_acre
                # Check for a rat invasion
                rat_chance = random.randint(1, 5)
                if rat_chance % 2 == 0:
                    # "*** Rats are running wild!!"
                    rat_loss = int(bushel_store / rat_chance)
                # Calculate bushels after harvest and rats
                bushel_store = bushel_store - rat_loss + harvest_yield
                
                # "*** Let's have some babies"
                # Calculate new incoming population
                incoming_pop = int(random.randint(1, 5) *
                               (20 * acres + bushel_store) /
                               population / 100 + 1)
            
                print(incoming_pop)  # DEBUG
                
                # "*** How many people had full tummies?"
                # 20 bushels will feed one person for a year
                fed_pop = int(feed_choice / 20)
                
                # "*** Horror, a 15% chance of plague"
                plague_value = random.randint(0, 100) - 15
                print(plague_value)  # DEBUG
                
                if population >= fed_pop:
                    # Some people have starved
                    starved = population - fed_pop
                    if starved > 0.45 * population:
                        print("Oops")
                
                
                
            
print("DONE")
game_running = False
    
    
    
  
  
  

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


            
        
    

    
