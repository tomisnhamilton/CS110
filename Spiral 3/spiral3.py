# -----------------------------------------
# Title: Course Project - Spiral 3
# Author: CounterSpective
# Section: M1
# Documentation in canvas submission
# What creative extras you added in canvas submission
# -----------------------------------------

#Don't forget to use your code from spiral 2 as a starting point
#Your spiral 2 code allows the human to fly their aircraft. Now add functions for the enemy fighter per the canvas directions

#__________________________________________________________________________________________________________________________________________________________
# 1. IMPORTING MODULES:

import pythonGraph as pg
import instructor_provided as ip
import time
import random as r
import math

#__________________________________________________________________________________________________________________________________________________________
# 2. DEFINING & SETTING GLOBAL VARIABLES:

# Constants for the width and height of our window
SCREEN_WIDTH = 990
SCREEN_HEIGHT = 990

# How many tiles we want our map to be (15x15)
GRID_DIM = 15

# Creates the world map, represented as a 2D list, that you will use to
# draw each tile and then fly through
WORLD = ip.initialize("15_by_15.csv")

# Constant for the amount of time between updates
UPDATE_INTERVAL_IN_SECONDS = 0.5

# Gives us the current time in seconds, since epoch, so that we can track
# when the jet and missile was last updated
jet_update = time.time()
missile_update = time.time()

# Establishes the standard tile/image size for use in each drawing function
img_w = SCREEN_WIDTH/GRID_DIM
img_h = SCREEN_HEIGHT/GRID_DIM

# Initializes player starting coordinates and heading. We will use these to track the jet's
# location and heading throughout our code
x_jet = 2
y_jet = 6
heading = "NORTH"

# Initializes a list to track our missile - since we haven't launched any yet, it's empty!
missile = []

#__________________________________________________________________________________________________________________________________________________________
# 3. DEFINING PLAYER & WORLD FUNCTIONS:

def draw_missile():
    # Defining Global List (missile) within function
    global missile
    
    # direction (local var) defines the filename of the missile, using string concatenation
    direction = 'images/missile_'+missile[0].lower()+'.png'

    if missile[4] == 'E':
        direction = 'images/explosion.png'
        
    # defines new vars (x_missile, y_missile) for setting the missile's x and y locations to appropriate tiles
    x_missile = missile[1] * img_w
    y_missile = missile[2] * img_h
    
    # calling actual pythonGraph function to draw the image
    pg.draw_image(direction, x_missile, y_missile, img_w, img_h)

    
def draw_tile(asset, x_tile, y_tile):
    # Conditionals to check the given parameter and set it to its actual file name
    if asset == "G":
        asset = 'images/grass.png'
    elif asset == "M":
        asset = 'images/mountain.png'
    elif asset == "R":
        asset = 'images/road.png'
    elif asset == "T":
        asset = 'images/trees.png'
    elif asset == "B":
        asset = 'images/base.png'
    elif asset == "E":
        asset = 'images/explosion.png'
    
    #Sets the x & y parameters to appropriate values on grid
    x_tile *= img_w
    y_tile *= img_h
    
    #calling actual pythonGraph function to draw the image
    pg.draw_image(asset, x_tile, y_tile, img_w, img_h)


def draw_jet():
    # Defining Global Vars (heading, x_jet, y_jet) within function
    global heading
    global x_jet
    global y_jet
    
    # direction (local var) defines the filename of the missile, using string concatenation
    direction = 'images/friendly_fighter_'+heading.lower()+'.png'
    
    # defines new local vars (x_tile, y_tile) for setting the jet's x and y locations to appropriate tiles w/out affecting the global vars
    x_jet_tile = x_jet * img_w
    y_jet_tile = y_jet * img_h
        
    # calling actual pythonGraph function to draw the image
    pg.draw_image(direction, x_jet_tile, y_jet_tile, img_w, img_h)


def draw_world():
    # Creating draw_world function to iteratively draw tiles
    # Defining WORLD as a global var in the function
    global WORLD
    
    # Utilizing nested for-loops to draw out rows and columns sequentially
    for col in range(len(WORLD)):
        for row in range(len(WORLD)):
            # Calling draw_tile to draw the indivual tiles and locations while iterating.
            draw_tile(WORLD[col][row], row, col)


def listen_keyboard():
    # Defining global vars "heading" and "missile"
    global heading
    global missile
    
    # Setting values for pressing keys (arrows & space)
    if pg.key_pressed('up') == True:
        heading = "NORTH"  
    elif pg.key_pressed('down') == True:
        heading = "SOUTH"
    elif pg.key_pressed('left') == True:
        heading = "WEST"
    elif pg.key_pressed('right') == True:
        heading = "EAST"

    if pg.key_pressed('space') == True and missile == []:
        # When the SPACE key is pressed, the missile list is no longer empty
        missile = [heading, x_jet, y_jet, 0, 'MS']
        

def update():
    # Creating the ever-complex update function to update all "dynamic" vars and make a smooth animation
    # Defining all global vars
    global x_jet
    global y_jet
    global heading
    global jet_update
    global missile_update
    global missile
    global jet_tank, fuel_tracker

    # ----------------------------------------- Jet Update -----------------------------------------
    # Implements the time module to have "real-time" animations; conditional updates the jet animation if enough time has passed.
    if time.time()>jet_update + UPDATE_INTERVAL_IN_SECONDS:
        jet_update = time.time()
        
        # Pretty simple... Uses conditionals to simulate animation of a moving jet; ties in w/ arrow keys to play the game
        if heading == "NORTH" and y_jet > 0:
            y_jet -= 1
        elif heading == "SOUTH" and y_jet < GRID_DIM-1:
            y_jet += 1
        elif heading == "WEST" and x_jet > 0:
            x_jet -= 1
        elif heading == "EAST" and x_jet < GRID_DIM-1:
            x_jet += 1

        jet_tank -= fuel_tracker

    # -------------------------------------- Missile Update ---------------------------------------
    if time.time() > missile_update + (0.5 * UPDATE_INTERVAL_IN_SECONDS):
        missile_update = time.time()
        
        # Uses conditionals to update the missile's position on the grid; the missile's own values are used to be independent of the jet's movement
        if bool(missile) == True:
            if missile[0] == "NORTH":
                missile[2] -= 1
            elif missile[0] == "SOUTH":
                missile[2] += 1
            elif missile[0] == "WEST":
                missile[1] -= 1
            elif missile[0] == "EAST":
                missile[1] += 1
            
            # Updates the number of tiles that the missile has flown for
            missile[3] += 1
            # A lot happens here... checks if missile has flown for more than 4 tiles (explodes if true and calls the function to show the correct image)
            # When the missile has flown for 5 (theoretical) tiles, the missile list is set to empty
            if missile[3] == 4:
                missile[4] = 'E'
            elif missile[3] == 5:
                missile = []
                

def draw_hud(x,y):
    # This function draws the player's coordinates as a heads up display (HUD) - no changes required
    # as this is provided to help you troubleshoot
    pg.draw_text("Player Coordinates: " + str(x) + ", " + str(y), 10, 10, "BLUE", 24)


#__________________________________________________________________________________________________________________________________________________________
# 4. DEFINING NEW HOSTILE VARIABLES & FUNCTIONS:

# Hostile Position Variables:
hostile_heading_list = ["NORTH", "SOUTH", "EAST", "WEST"]
# randomizing the heading of the enemy jet
hostile_heading = r.choice(hostile_heading_list)
x_hostile = 9
y_hostile = 3

# Hostile Movement Variables:
hostile_update_time = time.time()
hostile_missile_update = time.time()
hostile_tiles_flew = 0

# Hostile FOV & Pathfinding Variables:
x_goal = x_jet
y_goal = y_jet
detected = False

# Hostile Missile Variables:
hostile_missile = []

# Collision Variables:
jet_collision = 0
hostile_collision = 0

# Alive and Dead State
jet_alive = True
hostile_alive = True


# Displays the Enemy Jet
def draw_hostile():
    # Defining Global Vars (heading, x_jet, y_jet) within function
    global x_hostile
    global y_hostile
    global hostile_heading
    
    # direction (local var) defines the filename of the missile, using string concatenation
    direction = 'images/hostile_fighter_'+hostile_heading.lower()+'.png'
    
    # defines new local vars (x_tile, y_tile) for setting the jet's x and y locations to appropriate tiles w/out affecting the global vars
    x_hostile_tile = x_hostile * img_w
    y_hostile_tile = y_hostile * img_h
    
    # calling actual pythonGraph function to draw the image
    pg.draw_image(direction, x_hostile_tile, y_hostile_tile, img_w, img_h)
        

# Moves the Enemy Jet
def enemy_movement():
    global y_hostile
    global x_hostile
        
    # Moves the enemy jet, similar to player jet
    if hostile_heading == "NORTH" and y_hostile > 0:
        y_hostile -= 1
    elif hostile_heading == "SOUTH" and y_hostile < GRID_DIM-1:
        y_hostile += 1
    elif hostile_heading == "WEST" and x_hostile > 0:
        x_hostile -= 1
    elif hostile_heading == "EAST" and x_hostile < GRID_DIM-1:
        x_hostile += 1
    else:
        # Turns the enemy when it hits a border
        enemy_turn()


# Turns the Enemy Jet in a random, non-current heading
def enemy_turn():
    global hostile_heading
    
    change_heading = ["NORTH", "SOUTH", "EAST", "WEST"]
    change_heading.remove(hostile_heading)
    hostile_heading = r.choice(change_heading)
    #print(hostile_heading)


# Gives the enemy a random chance to turn in an direction to simulate real player movement
def turn_chance():
    global hostile_tiles_flew

    chance = bool(r.getrandbits(1))
    if chance == True:
        enemy_turn()
        hostile_tiles_flew = 0
        

# Enemy Patrol Mode (Enemy will move around the map without acknowledging the player)
def enemy_ai_search():
    enemy_movement()
    # Random Turning after 5 tiles to simulate realistic flying
    if hostile_tiles_flew >= 5:
        turn_chance()


# Gives the Enemy a detection field to locate the player (dist_points)
# Pathlength/finding Concept; initially set to high value
pathlength = 10
def enemy_ai_detect():
    global x_goal, y_goal
    global hostile_heading
    global pathlength
    # Uses Pythagorean Theorum to calculate distance between jets
    x_path = abs(x_jet-x_hostile)
    y_path = abs(y_jet-y_hostile)  
    pathlength = math.sqrt(x_path**2 + y_path**2)
    #print("X:", x_path, "Y:", y_path, "Length:", pathlength)

    # Defining the target for the enemy to get to in order to shoot missiles
    if heading == 'NORTH':
        # Sets the goal / following range for the hostile
        y_goal = y_jet + 1
        x_goal = x_jet
    if heading == 'SOUTH':
        y_goal = y_jet - 1
        x_goal = x_jet
    if heading == 'WEST':
        x_goal = x_jet + 1
        y_goal = y_jet 
    if heading == 'EAST':
        x_goal = x_jet - 1
        y_goal = y_jet
    
    #print("X_Goal:", x_goal, "Y_Goal", y_goal)

    # Enemy Manuevers to meet defined goals (see if 3.5 or 4 is better)
    if pathlength <= 3.5:
        if x_hostile < x_goal:
            hostile_heading = 'EAST'
        elif x_hostile > x_goal:
            hostile_heading = 'WEST'
        elif y_hostile > y_goal:
            hostile_heading = 'NORTH'
        elif y_hostile < y_goal:
            hostile_heading = 'SOUTH'


# Draws the Enemy Missile
def draw_hostile_missile():
    # Defining Global List (missile) within function
    global hostile_missile
    
    # direction (local var) defines the filename of the missile, using string concatenation
    direction = 'images/missile_'+hostile_missile[0].lower()+'.png'

    if hostile_missile[4] == 'E':
        direction = 'images/explosion.png'
        
    # defines new vars (x_missile, y_missile) for setting the missile's x and y locations to appropriate tiles
    x_missile = hostile_missile[1] * img_w
    y_missile = hostile_missile[2] * img_h
    
    # calling actual pythonGraph function to draw the image
    pg.draw_image(direction, x_missile, y_missile, img_w, img_h)        


# Standalone funciton for missile movement (similar to player missile code)
def enemy_missile():
    global hostile_missile
    if bool(hostile_missile) == True:
        if hostile_missile[0] == "NORTH":
            hostile_missile[2] -= 1
        elif hostile_missile[0] == "SOUTH":
            hostile_missile[2] += 1
        elif hostile_missile[0] == "WEST":
            hostile_missile[1] -= 1
        elif hostile_missile[0] == "EAST":
            hostile_missile[1] += 1

        # Updates the number of tiles that the missile has flown
        hostile_missile[3] += 1
        # A lot happens here... checks if missile has flown for more than 4 tiles (explodes if true and calls the function to show the correct image)
        # When the missile has flown for 5 (theoretical) tiles, the missile list is set to empty
        if hostile_missile[3] == 4:
            hostile_missile[4] = 'E'
        elif hostile_missile[3] == 5:
            hostile_missile = []


# Detects various collision properties to end game
def collision_detection():
    global jet_collision, hostile_collision
    global jet_alive, hostile_alive
    global missile, hostile_missile
    
    if bool(hostile_missile) == True and hostile_missile[1] == x_jet and hostile_missile[2] == y_jet:
        # Jet Shot Down
        jet_collision = 1
        jet_alive = False
    elif bool(missile) == True and missile[1] == x_hostile and missile[2] == y_hostile:
        # Enemy Shot Down
        hostile_collision = 1
        hostile_alive = False
    elif (x_jet == x_hostile and y_jet == y_hostile) or ((heading in ['EAST', 'WEST'] and hostile_heading in ['EAST', 'WEST'] and heading != hostile_heading) or (heading in ['NORTH', 'SOUTH'] and hostile_heading in ['NORTH', 'SOUTH'] and heading != hostile_heading)) and pathlength < 1:
        # Plane Crash (Assumed Kamikaze)
        jet_collision = 2
        jet_alive = False
    elif jet_tank <= 0:
        # Technically not a collision, but named so to keep consistency with ending game
        jet_collision = 3
        jet_alive = False


def hostile_update():
    # Defining all global vars
    global hostile_update_time
    global hostile_missile_update
    global hostile_tiles_flew
    global hostile_missile

    # ----------------------------------------- Hostile Update -----------------------------------------
    # Implements the time module to have "real-time" animations; conditional updates the hostile jet animation if enough time has passed.
    if time.time()>hostile_update_time + UPDATE_INTERVAL_IN_SECONDS:
        hostile_update_time = time.time()
        #Calls functions to move, turn, detect the player, and chase
        enemy_ai_search()
        enemy_ai_detect()
        hostile_tiles_flew += 1

    # Enemy shoots missile if aligned with goals and within range; this avoids missile spam and seemingly unnecessary fire
    if ((x_hostile == x_goal and y_hostile in range(y_goal-2, y_goal+2)) or (x_hostile in range(x_goal-2, x_goal+2) and y_hostile == y_goal)) and hostile_missile == [] and pathlength <= 4:
        hostile_missile = [hostile_heading, x_hostile, y_hostile, 0, 'MS']

    if time.time()>hostile_missile_update + (0.5* UPDATE_INTERVAL_IN_SECONDS):
        hostile_missile_update = time.time()
        enemy_missile()


# 5. CALLING CREATING WORLD & FUNCTIONS

# INTERMISSION FOR SOME CREATIVE QUALITY OF LIFE IMPROVEMENTS
# Determines whether the actual game (where you're actively playing) has been started or not (set to false by default). 
initialize = False
# Stores all movement options in a list
movement_options = ['up','down','left','right']
# Score variable (all games have scores...)
score = 0
# Determine whether a music file has been played (used for end game sounds)
music_played = False
# Options for music. Music from Metal Gear Solid and Final Fantasy VII
music_options = ['custom_music/mgs_battle.mp3', 'custom_music/ff_battle.mp3']


# Randomizes spawn placement on the map
def spawn_placement():
    def player_placement():
        # Makes 2 empty lists, appends values 0-14 to them, and selects a random value to set player spawn 
        x_tile_options = []
        y_tile_options = []
        global x_jet, y_jet
        for i in range(GRID_DIM):
            x_tile_options.append(i)
            y_tile_options.append(i)

        x_jet = r.choice(x_tile_options)
        y_jet = r.choice(y_tile_options)

    def enemy_placement():
        x_tile_options = []
        y_tile_options = []
        global x_hostile, y_hostile
        for i in range(GRID_DIM):
            x_tile_options.append(i)
            y_tile_options.append(i)
        # When spawning the enemy, it will not spawn on the player's position
        x_tile_options.remove(x_jet) 
        y_tile_options.remove(y_jet)

        x_hostile = r.choice(x_tile_options)
        y_hostile = r.choice(y_tile_options)
    
    player_placement()
    enemy_placement()


# Creative Idea for keeping the player's score throughout rounds
# Tracks the last key pressed to avoid score abuse
key_pressed_before = "up"
def game_score():
    global score, key_pressed_before
    if pg.get_pressed_key() in movement_options and pg.get_pressed_key() != str(key_pressed_before):
        score += 0.5
        key_pressed_before = pg.get_pressed_key()
    if jet_collision in [1,2,3]:
        score -= 25
    elif hostile_collision == 1:
        score += 50


# Creative Idea limiting the player's visibility
fog = 0
fog_value = "OFF"
def fog_of_war():
    global fog
    # Visibility range for the jet
    visibility = 3
    x_sight = range(x_jet-visibility, x_jet+visibility+1)
    y_sight = range(y_jet-visibility, y_jet+visibility+1)
    # Works like draw_world() by drawing images over map, but leaving the jet's surrounding blank
    for col in range(len(WORLD)):
        for row in range(len(WORLD)):
        # Calling draw_tile to draw the indivual tiles and locations while iterating.
            if row in x_sight and col in y_sight:
                pass
            else:
                pg.draw_image('custom_images/fog.png', row*img_w, col*img_h, img_w+1, img_h+1)


# Creative Idea making the player consider fuel levels and dying if fuel is empty (0)
jet_tank = 100
fuel_color = ["GREEN", "YELLOW", "RED"]
fuel_tracker = 1
def jet_fuel():
    global jet_tank, fuel_color, fuel_tracker, fuel
    if jet_tank >= 66:
        color_indicator = 0
    elif jet_tank >= 33:
        color_indicator = 1
    else:
        color_indicator = 2 

    # Draws the jet's fuel level
    pg.draw_rectangle(0*img_w, (GRID_DIM-0.5)*img_h, (GRID_DIM-10)*img_w, GRID_DIM*img_h, "BLACK", False)
    pg.draw_rectangle(0.1*img_w, (GRID_DIM-0.4)*img_h, ((jet_tank/(GRID_DIM+5))-0.1)*img_w, (GRID_DIM-0.1)*img_h, fuel_color[color_indicator], True)
    # Tops off fuel if above 75 full, adds 25 fuel to the jet's fuel
    if x_jet == fuel[0] and y_jet == fuel[1]:
        if jet_tank > 75:
            jet_tank = 100
        else:
            jet_tank += 25
        fuel = [r.choice(range(GRID_DIM-1)),r.choice(range(GRID_DIM-1))]


# Spawns in the fuel tank at random locations
fuel = [r.choice(range(GRID_DIM-1)),r.choice(range(GRID_DIM-1))]
def fuel_spawn():
    global jet_tank, fuel
    pg.draw_image("custom_images/gas.png",fuel[0]*img_w, fuel[1]*img_h, img_w, img_h)


# End Game Function for detecting collsions and running commands associated with victory or defeat
def end_game():
    global jet_collision, hostile_collision
    global music_played, score
    global jet_tank
    if jet_collision == 1:
        pg.draw_text("BOOM!!!! YOU DIED!!", 5.85*img_w, 5.75*img_h, "RED", 30)
        if music_played == False:
            pg.play_sound_effect('custom_music/player_death.wav')
            music_played = True
    elif hostile_collision == 1:
        pg.draw_text("VICTORY!!! YOU KILLED THE HOSTILE!!!", 4.5*img_w, 5.75*img_h, "RED", 30)
        if music_played == False:
            pg.play_sound_effect('custom_music/player_win.wav')
            music_played = True
    elif jet_collision == 2:
        pg.draw_text("KAMIKAZE!!!! YOU DIED!!", 5.75*img_w, 5.75*img_h, "RED", 30)
        if music_played == False:
            pg.play_sound_effect('custom_music/player_death.wav')
            music_played = True
    elif jet_collision == 3:
        pg.draw_text("OUT OF GAS! GOING DOWN!!", 5.4*img_w, 5.75*img_h, "RED", 30)
        if music_played == False:
            pg.play_sound_effect('custom_music/player_death.wav')
            music_played = True
            jet_tank = 100


# Creative Idea for providing a start screen and pre-game
def start_screen():
    global fog_value
    pg.clear_window("WHITE")
    draw_world()
    pg.draw_rectangle(0, 5*img_h, GRID_DIM*img_w, 9*img_h,"WHITE",True)
    pg.draw_text("Ace Combat 0: Grounded Skies", 5.25*img_w, 5.25*img_h, 36)
    pg.draw_text("Play Game", 6.65*img_w, 6.25*img_h, 28)
    pg.draw_text("Instructions", 6.5*img_w, 7.3*img_h, 28)
    pg.draw_text("Quit Game", 6.6*img_w, 8.3*img_h, 28)
    pg.draw_text("Fog of War: " + fog_value, 11.5*img_w, 7*img_h, 14)
    pg.draw_text("Press 'F' to toggle.", 11.5*img_w, 7.5*img_h, 14)


# Adds round splash screen before each round lasting 4 seconds
intermission = True
round_game = 1
round_update = time.time()
round_time_counter = 0
def round_screen():
    global intermission, round_game, round_update, round_time_counter
    if round_time_counter < 5:
        pg.clear_window("BLACK")
        pg.draw_text("ROUND: " + str(round_game), 6.25*img_w, 6.5*img_h, "WHITE", 48)
    else:
        intermission = False
    if time.time()>round_update + UPDATE_INTERVAL_IN_SECONDS:
        round_update = time.time()
        round_time_counter += 1
 

# Allows for menmu movement to either play the game, view instructions, quit (close the window), or toggle fog_of_war()
menu_selection = 0
def main_menu():
    global menu_selection
    global instructions
    global fog, fog_value
    if menu_selection == 0:
        start_screen()
        pg.draw_rectangle(5*img_w, 6.15*img_h, 10*img_w, 6.6*img_h, "BLACK", False)
    elif menu_selection == 1:
        start_screen()
        pg.draw_rectangle(5*img_w, 7.2*img_h, 10*img_w, 7.65*img_h, "BLACK", False)
        if pg.key_pressed('enter') == True or pg.key_pressed('return') == True:
            instructions = True
    elif menu_selection == 2:
        start_screen()
        pg.draw_rectangle(5*img_w, 8.2*img_h, 10*img_w, 8.65*img_h, "BLACK", False)
        if pg.key_pressed('enter') == True or pg.key_pressed('return') == True:
            pg.close_window()

    if pg.key_pressed('down') == True:
        menu_selection += 1
    elif pg.key_pressed('up') == True:
        menu_selection -= 1
    if menu_selection >= 3:
        menu_selection = 0
    elif menu_selection <= -1:
        menu_selection = 2

    if pg.key_pressed('f') == True:
        fog += 1
        if fog > 1:
            fog = 0
        if fog == 0:
            fog_value = "OFF"
        elif fog == 1:
            fog_value = "ON"


# Displays the instruction menu if the player opens the menu
instructions = False
def instruction_menu():
    global menu_selection, instructions
    if instructions == True:
        pg.clear_window("WHITE")
        draw_world()
        pg.draw_rectangle(0, 5*img_h, GRID_DIM*img_w, 9*img_h,"WHITE",True)
        pg.draw_text("Ace Combat 0: Grounded Skies", 5.25*img_w, 5.25*img_h, 36)
        pg.draw_text("Instructions:", 6.7*img_w, 6*img_h, 28)
        pg.draw_text("Use the Arrow Keys Keys to move!", 5.25*img_w, 6.5*img_h, 28)
        pg.draw_text("Use the SPACEBAR to shoot missiles!", 5*img_w, 6.95*img_h, 28)
        pg.draw_text("Press ESCAPE to Pause the Game!", 5.2*img_w, 7.35*img_h, 28)
        pg.draw_text("Press ESCAPE to Go Back", 5.75*img_w, 8.5*img_h, 28)

        if pg.key_pressed('escape') == True:
            menu_selection = 0
            instructions = False
            main_menu()


# Adds a pause function while playing the game; player can resume, go back to menu screen, or quit the game
paused = False
pause_selection = 0
def pause_menu():
    global pause_selection, paused
    pg.clear_window("BLACK")
    pg.draw_text("Paused", 6.5*img_w, 5.25*img_h, "WHITE", 40)
    pg.draw_text("Resume", 6.75*img_w, 6.3*img_h, "WHITE", 24)
    pg.draw_text("Back to Main Menu", 6.12*img_w, 7.3*img_h, "WHITE", 24)
    pg.draw_text("Quit Game", 6.6*img_w, 8.3*img_h, "WHITE", 24)

    if pause_selection == 0:
        pg.draw_rectangle(5.85*img_w, 6.05*img_h, 8.65*img_w, 6.75*img_h, "WHITE", False)
    elif pause_selection == 1:
        pg.draw_rectangle(5.85*img_w, 7.05*img_h, 8.65*img_w, 7.75*img_h, "WHITE", False)
    elif pause_selection == 2:
        pg.draw_rectangle(5.85*img_w, 8.05*img_h, 8.65*img_w, 8.75*img_h, "WHITE", False)
    
    if pg.key_pressed('down') == True:
        pause_selection += 1
    elif pg.key_pressed('up') == True:
        pause_selection -= 1
    if pause_selection >= 3:
        pause_selection = 0
    elif pause_selection <= -1:
        pause_selection = 2


# Plays main menu music (had trouble playing anywhere else); music from Top Gun
intro_played = False
def intro_music():
    global intro_played
    if intro_played == False:
        pg.play_music('custom_music/intro.mp3')
        intro_played = True


# Stores all main gameplay functions in a function for organization
def gameplay_functions():
    global fog
    draw_world()
    # Calling Functions for hostile jet AI
    draw_hostile()
    hostile_update()
    # Calling Functions for player jet
    listen_keyboard()
    draw_jet()
    update()

    if bool(missile) == True:
        draw_missile()
    if bool(hostile_missile) == True:
        draw_hostile_missile()
    fuel_spawn()
    # Call Fog of War
    if fog == True:
        fog_of_war()
    elif fog == False:
        pass
    jet_fuel()
    # Call for collision detection to end the game
    collision_detection()
    # Call for keeping the player's score
    game_score()
    pg.draw_text("Score: " + str(score), 13*img_w, 0, "YELLOW", 26)
    draw_hud(x_jet, y_jet)
    

# Creative Idea for allowing players to play multiple times without running the code again; resets the initial value for variables and respawns the jets
def reset():
    global jet_collision, hostile_collision, jet_alive, hostile_alive, music_played
    global missile, hostile_missile
    global initialize
    global jet_tank
    global pathlength
    global round_time_counter, intermission

    initialize = True
    spawn_placement()
    missile = []
    hostile_missile = []
    jet_collision = 0
    hostile_collision = 0
    jet_alive = True
    hostile_alive = True
    music_played = False
    jet_tank = 100
    pathlength = 10
    round_time_counter = 0
    intermission = True

    pg.clear_window("BLACK")
    pg.play_music(r.choice(music_options))
    

# Opening window and setting title
pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)
pg.set_window_title("ACE COMBAT 0: GROUNDED SKIES")
# Creates the animation loop; draws the world and jet while listening for key inputs and updating accordingly (also displays the hud)
while pg.window_not_closed():
    # Runs reset() when the player requests to play the game
    if pg.key_pressed('enter') == True or pg.key_pressed('return') == True and initialize == False and menu_selection == 0:
        reset()

    # displays the pre-game screen if the player hasn't started the game (default when running the code)
    if initialize == False and instructions == False:
        main_menu()
    elif initialize == False and instructions == True:
        instruction_menu()
    if initialize == False:
        intro_music()

    # Starts the gameplay loop (reset() handles most values)
    if jet_alive == True and hostile_alive == True and initialize == True and menu_selection == 0 and paused == False:
        if intermission == True:
            round_screen()
        if intermission == False:
            gameplay_functions()
        intro_played = True
        #pg.draw_circle(x_hostile*img_w, y_hostile*img_h, 3*img_w, "RED", False)
        #pg.draw_line(x_jet*img_w, y_jet*img_h, x_hostile*img_w, y_hostile*img_h, "BLUE")
        if pg.key_pressed('escape') == True:
            paused = True

    # Displays the pause menu and allows player selection
    if paused == True:
        pause_menu()
        if pg.key_pressed('enter') == True or pg.key_pressed('return') == True and pause_selection == 0:
            paused = False
            gameplay_functions()
        elif pg.key_pressed('enter') == True or pg.key_pressed('return') == True and pause_selection == 1:
            paused = False
            pg.stop_music()
            initialize = False
            intro_played = False
            round_game = 1
            pg.clear_window("WHITE")
            main_menu()
            score = 0
        elif pg.key_pressed('enter') == True or pg.key_pressed('return') == True and pause_selection == 2:
            pg.close_window()

    # checks if a collision has occurred and runs end_game commands
    elif jet_alive == False or hostile_alive == False:
        pg.stop_music()
        pg.draw_rectangle(0, 5*img_h, GRID_DIM*img_w, 9*img_h,"WHITE",True)
        pg.draw_text("Press ENTER/RETURN to Play Again!", 5*img_w, 7*img_h, 28)
        pg.draw_text("Press ESCAPE to Exit", 5.9*img_w, 7.75*img_h, 28)
        end_game()

        # Allows players to either play again or close the window via key presses
        if pg.key_pressed('enter') == True or pg.key_pressed('return') == True:
            reset()
            round_game += 1
        elif pg.key_pressed('escape') == True:
            pg.close_window()

    pg.update_window()

# Quick Disclaimer: I primarily coded in VSCode and ran the final version in Thonny
# When using the "Exit Game" options in Thonny, the window doesn't close as expected; however, it does in VSCode.
