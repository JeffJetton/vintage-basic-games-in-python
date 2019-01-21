######################################################################
#
# Hunt the Wumpus
#
# From: Best of Creative Computing (1976) and
#       BASIC Computer Games (1978)
#       Both edited by David H. Ahl
#
# A detailed description may be found at:
# https://www.atariarchives.org/bcc1/showpage.php?page=247   and
# https://www.atariarchives.org/morebasicgames/showpage.php?page=178
#
# Original BASIC program by Gregory Yob, circa 1973
#
# Python port by Jeff Jetton, 2019
#
######################################################################



import random, sys


####################  Constants  #####################################

ALLOW_DEBUG = True
STARTING_ARROWS = 5
MAX_ARROW_ROOMS = 5
NUM_BATS = 2
NUM_PITS = 2
# "Set up cave (dodecahedral node list)"
# The cave is 20 rooms, defined as a nested 21 x 3 tuple,
# with each "room" index containing a tuple of the numbers of
# the 3 connecting rooms. Since python is zero-indexed, yet the
# rooms are numbered 1 to 20, we include a "zero room" to
# get everything to match up correctly.
CAVE = ( (0, 0, 0),
         (2, 5, 8),    (1, 3, 10),  (2, 4, 12),   (3, 5, 14),
         (1, 4, 6),    (5, 7, 15),  (6, 8, 17),   (1, 7, 9),
         (8, 10, 18),  (2, 9, 11),  (10, 12, 19), (3, 11, 13),
         (12, 14, 20), (4, 13, 15), (6, 14, 16),  (15, 17, 20),
         (7, 16, 18),  (9, 17, 19), (11, 18, 20), (13, 16, 19) )
NUM_ROOMS = len(CAVE) - 1
# Some game state constants
WINNER_WUMPUS = 0
WINNER_PLAYER = 1
WINNER_NOBODY = 2
WINNER_TEXT = ('Wumpus', 'Player', 'Nobody') # For coder-friendly debugging
TURN_SHOOT = 'S'
TURN_MOVE = 'M'
REPLAY_SAME = '1'
REPLAY_NEW  = '2'
REPLAY_QUIT = '3'
        


#################### Classes and Functions  ##########################

class GameState:
    """
    Track locations of all game items (including player), as
    well as status of player and wumpus
    """
    player_room = 0
    wumpus_room = 0
    bat_rooms = [0] * NUM_BATS
    pit_rooms = [0] * NUM_PITS
    arrows_remaining = STARTING_ARROWS
    winner = WINNER_NOBODY

    def __init__(self, source = None):
        if source is None:
            # Randomly assign unique locations to each game item
            random_rooms = [i+1 for i in range(NUM_ROOMS)]
            random.shuffle(random_rooms)
            self.player_room = random_rooms[0]
            self.wumpus_room = random_rooms[1]
            for i in range(NUM_BATS):
                self.bat_rooms[i] = random_rooms[i + 2]
            for i in range(NUM_PITS):
                self.pit_rooms[i] = random_rooms[i + 2 + NUM_BATS]
        else:
            # If source is passed, make this object a copy
            self.player_room = source.player_room
            self.wumpus_room = source.wumpus_room
            self.bat_rooms = source.bat_rooms.copy()
            self.pit_rooms = source.pit_rooms.copy()
            self.arrows_remaining = source.arrows_remaining
            self.winner = source.winner
            
    def __str__(self):
        s = format("Player Room: %-2d     " % self.player_room)
        s += format("Wumpus Room: %-2d" % self.wumpus_room)
        s += format("\nArrows: %-2d          " % self.arrows_remaining)
        s += "Winner: " + WINNER_TEXT[g.winner] + "\n"
        s += "Bat Rooms: " + str(self.bat_rooms) + "\n"
        s += "Pit Rooms: " + str(self.pit_rooms)
        return s



def print_instructions():
    # Instructions are pretty much as originally written in the 1976
    # printing (some spacing changes and typos were in the 1978 version)
    print("Welcome to 'Hunt the Wumpus'")
    print("  The Wumpus lives in a cave of %d rooms. Each room" % NUM_ROOMS)
    print("has 3 tunnels leading to other rooms. (Look at a")
    print("dodecahedron to see how this works-If you don't know")
    print("what a dodechadron is, ask someone)\n")
    print("     Hazards:")
    print(" Bottomless Pits - %s rooms have bottomless pits in them"
          % ("Two" if NUM_PITS == 2 else str(NUM_PITS)))
    print("     If you go there, you fall into the pit (& lose!)")
    print(" Super Bats - %s other rooms have Super Bats. If you"
          % ("Two" if NUM_BATS == 2 else str(NUM_BATS)))
    print("     go there, a bat grabs you and takes you to some other")
    print("     room at random. (Which might be troublesome)\n")
    print("     Wumpus:")
    print(" The Wumpus is not bothered by the hazards (he has sucker")
    print(" feet and is too big for a bat to lift). Usually")
    print("h e is asleep. Two things that wake him up: Your entering")
    print(" his room or your shooting an arrow.")
    print("     If the Wumpus wakes, he moves (P=.75) one room")
    print(" or stays still (P=.25). After that, if he is where you")
    print(" are, he eats you up (& you lose!)\n")
    
    input("   *** Press RETURN or ENTER to continue *** ")
    
    print("\n     You:")
    print(" Each turn you may move or shoot a crooked arrow")
    print("   Moving: You can go one room (thru one tunnel)")
    print("   Arrows: You have %d arrows. You lose when you run out."
          % STARTING_ARROWS)
    print("   Each arrow can go from 1 to %d rooms. You aim by telling"
          % MAX_ARROW_ROOMS)
    print("   the computer the room#s you want the arrow to go to.")
    print("   If the arrow can't go that way (ie no tunnel) it moves")
    print("   at random to the next room.")
    print("     If the arrow hits the Wumpus, you win.")
    print("     If the arrow hits you, you lose.\n")
    print("    Warnings:")
    print("     When you are one room away from Wumpus or hazard,")
    print("    the computer says:")
    print(" Wumpus-  'I smell a Wumpus'")
    print(" Bat   -  'Bats nearby'")
    print(" Pit   -  'I feel a draft'\n")
    
    input("   *** Press RETURN or ENTER to start the game *** ")



def print_hazards(g):
    print("")
    adjacent_rooms = CAVE[g.player_room]
    if g.wumpus_room in adjacent_rooms:
        print("I smell a Wumpus!")
    for i in range(NUM_PITS):
        if g.pit_rooms[i] in adjacent_rooms:
            print("I feel a draft")
            break
    for i in range(NUM_BATS):
        if g.bat_rooms[i] in adjacent_rooms:
            print("Bats nearby!")
            break



def print_location(g):
    print("You are in room  %d" % g.player_room)
    print("Tunnels lead to  %d  %d  %d\n" % CAVE[g.player_room])
    
    
    
def wake_wumpus(g):
    # Pick a random adjacent room, or stay put
    r = random.randint(0, 3)
    if r < 3:
        g.wumpus_room = CAVE[g.wumpus_room][r]
    # Is the player here for us to eat?
    if g.wumpus_room == g.player_room:
        print("Tsk Tsk Tsk- Wumpus got you!")
        g.winner = WINNER_WUMPUS



def get_turn_choice():
    valid_response = False
    while not valid_response:
        response = input("Shoot or Move (%s-%s)? " % (TURN_SHOOT, TURN_MOVE))
        if len(response) > 0:
            response = response.strip().upper()[0]
            valid_response = response in (TURN_SHOOT, TURN_MOVE, '?')
    return(response)



def get_arrow_path():
    # Get number of rooms to shoot through
    valid_response = False
    while not valid_response:
        num_rooms = input("No. of rooms(1-%d)? " % MAX_ARROW_ROOMS)
        if num_rooms.isdigit():
            num_rooms = int(num_rooms)
            if num_rooms in range(1, MAX_ARROW_ROOMS + 1):
                valid_response = True
    # Get individual room numbers
    path = []
    for i in range(num_rooms):
        valid_response = False
        while not valid_response:
            room = input("Room #? ")
            if room.isdigit():
                room = int(room)
                # Arrows can't "double back"
                if i > 1 and (room == path[i-2]):
                    print("Arrows aren't that crooked - " +
                          "Try another room")
                else:
                    valid_response = True
                    path.append(room)
    return(path)



def shoot_arrow(g, path):
    arrow_room = g.player_room
    for room in path:
        # Move arrow to next room in path if that room
        # ajoins the current one. Otherwise, randomly pick.
        if room in CAVE[arrow_room]:
            arrow_room = room
        else:
            random_index = random.randint(0, 2)
            arrow_room = CAVE[arrow_room][random_index]

        # Did we hit anything?
        if arrow_room == g.wumpus_room:
            print("Aha! You got the Wumpus!")
            g.winner = WINNER_PLAYER
            break
        elif arrow_room == g.player_room:
            print("Ouch! Arrow got you!")
            g.winner = WINNER_WUMPUS
            break
        
    # Was that a total miss (nothing in path)?
    if g.winner == WINNER_NOBODY:
        print("Missed")
        wake_wumpus(g)
        
    # Running out of arrows loses the game
    if g.winner == WINNER_NOBODY:
        g.arrows_remaining -= 1
        if g.arrows_remaining <= 0:
            g.winner = WINNER_WUMPUS



def relocate_player(g, new_room):
    g.player_room = new_room
    # "Check for hazards"
    # "Wumpus"
    if g.player_room == g.wumpus_room:
        print("... Oops! Bumped a Wumpus!")
        wake_wumpus(g)
    # Pits or bats? (If the wumpus didn't get ya yet)
    if g.winner == WINNER_NOBODY:
        if g.player_room in g.pit_rooms:
            print("YYYIIIIEEEE . . . Fell in pit")
            g.winner = WINNER_WUMPUS
        elif g.player_room in g.bat_rooms:
            print("ZAP--Super Bat snatch! Elsewhereville for you!")
            relocate_player(g, random.randint(1, 20))



def get_room_choice(g):
    valid_response = False
    while not valid_response:
        response = input("Where to? ")
        if response.isdigit():
            response = int(response)
            if response in range(1, len(CAVE)):
                if response in CAVE[g.player_room]: # Legal move?
                    valid_response = True
                else:
                    print("Not possible -")
    return(response)



def get_replay_choice():
    print("\n   %s. Play again - Same set-up" % REPLAY_SAME)
    print("   %s. Play again - New set-up" % REPLAY_NEW)
    print("   %s. Quit\n" % REPLAY_QUIT)
    valid_response = False
    while not valid_response:
        response = input("What is your choice? ")
        if len(response) == 1:
            if response in (REPLAY_SAME, REPLAY_NEW, REPLAY_QUIT):
                valid_response = True
    return(response)





######################### Main program ###############################


# Intro text and instructions
print("\n                  Wumpus")
print("Creative Computing  Morristown, New Jersey")
print("\n\n\n")
response = input("Instructions (Y-N)? ")
if len(response) > 0 and response.strip().upper()[0] != "N":
    print_instructions()


# Outer loop plays series of games until player quits.
replay_previous_game = False
still_playing = True
while still_playing:
    
    # Initialize game
    if replay_previous_game:
        g = GameState(saved_state)
    else:
        g = GameState()
        saved_state = GameState(g)
        
    # "Run the game" until we have a winner
    print("\nHunt the Wumpus\n")
    while g.winner == WINNER_NOBODY:
        
        # "Hazard warnings & locations"
        print_hazards(g)
        print_location(g)
        
        # "Move or shoot" (or debug)
        option = get_turn_choice()
        if option == "S":
            arrow_path = get_arrow_path()
            shoot_arrow(g, arrow_path)
        elif option == "M":
            new_room = get_room_choice(g)
            relocate_player(g, new_room)
        elif option == "?" and ALLOW_DEBUG:
            print("\n******************\n")
            print(g)
    
    if g.winner == WINNER_WUMPUS:
        print("Ha Ha Ha - You lose!")
    else:
        print("Hee Hee Hee - The Wumpus'll getcha next time!!")
    choice = get_replay_choice()
    if choice == REPLAY_QUIT:
        still_playing = False
    else:
        replay_previous_game = (choice == REPLAY_SAME)



########################################################
#
# Porting Notes
#
#   The original program used a global array rather than
#   a local object to keep track of the various item
#   locations.  It was written to always have two bats
#   and two pits.  This version refers to the NUM_BATS
#   and NUM_PITS constants rather than making any
#   assumptions, and it can easily accommodate changes
#   to those two values (see Modifications section).
#
#   The original was well-organized for a BASIC program
#   of that era, breaking most game steps out into tidy
#   subroutines.  We stay pretty close to the same
#   structure, although we split a few subroutines
#   into smaller chunks here and there.
#
#   Added ability to exit game. (Original program just
#   asked to play again with same or new set-up.)
#
#   Added a debugging (or cheating!) feature: If
#   enabled by the ALLOW_DEBUG constant, player can
#   type ? to dump the game state object to the screen.
#
#
# Ideas for Modifications
#
#   Keep track of the number of moves and report it out
#   as a sort of score at the end of the game.
#
#   Report on number of arrows remaining after each
#   shot.  Inform player when they've run out (so they
#   understand why they just lost!)
#
#   Let player select a difficulty level by choosing
#   from a preset menu of combinations of values for
#   arrows, bats, and pits.
#
#   Player starts with no arrows--they're randomly
#   strewn about the cave and must be collected.
#
#   Put a rope out there for the player to collect,
#   which will save them from dying from pits if they
#   have it.
#
#   Suggested by the original author, Gregory Yob: "If
#   you are a Wumpus fiend, make a version of Wumpus in
#   which he avoids pits, and superbats can carry him
#   only one room (with the possibility of being dumped
#   into your cave)."
#
#   Add support for different cave systems.  (There were
#   official sequels to Wumpus that actually did that.)
#
#   The current method for specifying moves and arrow
#   shows is just as it was in the original BASIC
#   program--but it's a little clunky.  Try changing the
#   game so that the player just has to type one line
#   for each turn. For example, to move to room five:
#
#     M 5
#
#   Or to shoot through three rooms, 1, 2, and 3:
#
#     S 1 2 3
#
########################################################


            
        
    

    
