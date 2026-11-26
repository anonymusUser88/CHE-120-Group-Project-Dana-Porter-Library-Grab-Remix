#Department of Chemical Engineering, Faculty of Engineering
#University of Waterloo
#26/11/2026
#MW = Marcus Wright, MS = Michael Small - Original Comments

#SH = Sethumi Hapuarachchi
#MF = Manal Fatima
#IM = Isabella Madduma
#EY = Ethan Yee

#MW: Imports all the necessary modules
import pygame , sys
from pygame import *
from sys import exit

#SH: Imports only the randint function from the random library
import random

#MW defines all the variables
ground_y=0
ground_x=0
pygame.init()
screen = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()
tile_size = 90
player_pos = 1 #Tracks the position of the player, and thus, changes what the picture of the player's sprite is
moveSpeed = 20
score = 0
start_time = 0
timesPlayed = 0
lives = 3
collected_presents = []
tile_list = []
present_index = 0 #SH - Tracks what present the user is trying to find; is used in many of the functions
#SH - The list below tracks whether each present should appear
#There is one extra variable in this list, and all associated ones so the functions we created below can work
present_appearances = [True, False, False, False, False, False, False, False]

#MW game state variables
introStart = True
controlStart = None
floor1Start = None
how_to_play_start = None
startOver = False

#MW caption for game window
pygame.display.set_caption("A Quackful Christmas")

#MW imports all of the images and image rectangles for the game
#MW floor design for the game
ground = pygame.image.load("new_blank_map.png").convert_alpha()
ground=pygame.transform.scale(ground, (52*tile_size,53*tile_size))
ground_rect = ground.get_rect(topleft = (-7*tile_size,-18*tile_size))

#MW presentshelf tile images
outer_wall = pygame.image.load('outer_wall.png')
inner_wall = pygame.image.load('inner_wall.png').convert_alpha()
ice_block = pygame.image.load('ice.png').convert_alpha()
tree_img = pygame.image.load('tree.png').convert_alpha()
rock_img =pygame.image.load('rock.png').convert_alpha()
bench_down =pygame.image.load('bench_down.png').convert_alpha()
bench_right =pygame.image.load('bench_right.png').convert_alpha()
bench_left = pygame.image.load("bench_left.png").convert_alpha()
bench_up = pygame.image.load("bench_up.png").convert_alpha()
streetlamp_img = pygame.image.load("streetlamp.png").convert_alpha()

#MW player forward postion image and rectangle
player_forward = pygame.image.load("santa_up.png").convert_alpha()
player_forward = pygame.transform.scale(player_forward, (70,70))
player_rect = player_forward.get_rect(center= (600,400))
player_forward_rect = player_forward.get_rect(center= (600,400))

#MW player back postion image and rectangle
player_back = pygame.image.load("santa_down.png").convert_alpha()
player_back = pygame.transform.scale(player_back, (70,70))
player_back_rect = player_back.get_rect(center= (600,400))

#MW player left postion image and rectangle
player_left = pygame.image.load("santa_left.png").convert_alpha()
player_left = pygame.transform.scale(player_left, (70,70))
player_left_rect = player_left.get_rect(center= (600,400))

#MW player right postion image and rectangle
player_right = pygame.image.load("santa_right.png").convert_alpha()
player_right = pygame.transform.scale(player_right, (70,70))
player_right_rect = player_right.get_rect(center= (600,400))

#SH - Heart lives image and rectangle
full_heart = pygame.image.load("full_heart.png").convert_alpha()
full_heart = pygame.transform.scale(full_heart, (70, 70))
full_heart_rect = full_heart.get_rect(topright = (0, 730))

#Goose image and rectangle *****
enemy = pygame.image.load("goose_right.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (tile_size, tile_size))
enemy_rect = enemy.get_rect(topright = (800,-1000))

#MS - Random Present Generator
#After initiallizing the present images, I scaled them up to the same size as the tiles.
blue_present = pygame.image.load('blue_present.png')
blue_present = pygame.transform.scale(blue_present, (tile_size, tile_size))
orange_present = pygame.image.load('orange_present.png')
orange_present = pygame.transform.scale(orange_present, (tile_size, tile_size))
green_present = pygame.image.load('green_present.png')
green_present = pygame.transform.scale(green_present, (tile_size, tile_size))
yellow_present = pygame.image.load('yellow_present.png')
yellow_present = pygame.transform.scale(yellow_present, (tile_size, tile_size))
teal_present = pygame.image.load('teal_present.png')
teal_present = pygame.transform.scale(teal_present, (tile_size, tile_size))
red_present = pygame.image.load('red_present.png')
red_present = pygame.transform.scale(red_present, (tile_size, tile_size))
purple_present = pygame.image.load('purple_present.png')
purple_present = pygame.transform.scale(purple_present, (tile_size, tile_size))

#MS - Using the rectangle method, I set six different positions for each of the 7 presents.
#Using the random module, each of these functions will choose one of the six different positions and place the present on the set coordinates.
#SH - Originally, the game had different functions to set the position for each of the presents. 
#We decided to consolidate some of them into one function that takes in different parameters 

#SH - Lists of the random positions for each present
blue_present_random_positions = [(1305,1390),(-495,3010),(2385,405),(2025,675),(1845,-585),(2385,1935)]

orange_present_random_positions = [(-495, -1490),(315, -230),(1000, 895),(2115, -230),(3465, 40),(1800, 1900)]

green_present_random_positions = [(-270,3060),(2000,3035),(3300,3050),(2450,540),(3300,-1530),(800,-1260)]

yellow_present_random_positions = [(-270,-3060),(2000,900),(2800,-100),(500,200),(1800,1900),(220,1260)]

teal_present_random_positions = [(-270,3060),(2000,3035),(3300,3050),(2450,540),(3300,-1530),(800,-1260)]

red_present_random_positions = [(220,1260),(1800,1900),(500,200),(2800,-100),(1000,900),(-300,-1260)]

purple_present_random_positions = [(800,-1260),(3300,-1530),(2450,540),(3300,3050),(2000,3035),(-270,3060)]

#SH - A function that initializes the position of a present; its parameters are the present, and the associated list of potential positions.
#The function chooses a random position from the associated list, and returns the rectangle of the present at that position.
def initialize_present_position(present, potential_present_positions):
    final_position = random.choice(potential_present_positions)
    return present.get_rect(center = final_position)

#MS - These are the varables assigned to whatever present positions the above functions choose.
#These will be called later in the game loop.
random_blue_present = initialize_present_position(blue_present, blue_present_random_positions)
random_orange_present = initialize_present_position(orange_present, orange_present_random_positions)
random_green_present = initialize_present_position(green_present, green_present_random_positions)
random_yellow_present = initialize_present_position(yellow_present, yellow_present_random_positions)
random_teal_present = initialize_present_position(teal_present, teal_present_random_positions)
random_red_present = initialize_present_position(red_present, red_present_random_positions)
random_purple_present = initialize_present_position(purple_present, purple_present_random_positions)

#SH - Two lists that contain the image of the present, and the rectangle of the present at the assigned position
#Once again, each list has an extra element
present_image_list = [blue_present, orange_present, green_present, yellow_present, teal_present, red_present, purple_present, purple_present]
random_present_list = [random_blue_present, random_orange_present, random_green_present, random_yellow_present, random_teal_present, random_red_present, random_purple_present, random_purple_present]

#MW imports fonts and defines word objects and rectangles for each word object
font_size_80 = pygame.font.Font('my_font.ttf', 80)
TitleSurface = font_size_80.render('A Quackful Christmas', True, "Black", "White") 
TitleSurfaceRect = TitleSurface.get_rect() 
TitleSurfaceRect.center = (600, 300)

font_size_60 = pygame.font.Font('my_font.ttf', 60)
StartGame = font_size_60.render('Start Game', True, "Black", "White")
StartGameRect = StartGame.get_rect() 
StartGameRect.center = (600, 600)

font_size_40 = pygame.font.Font('my_font.ttf', 40)

#MS - These are the fonts and messages for the how to play screen.
#These fonts are converted to rectangles so they can be placed acurately on the screen.
How_To_Play = font_size_40.render('How to Play', True, 'Black', 'Grey')
How_To_Play_Rect = How_To_Play.get_rect(center = (600,100))

Next_Button = font_size_40.render('Next', True, 'Black', 'Yellow')
Next_Button_Rect = Next_Button.get_rect(center = (1100,700))

Instructions_1 = font_size_40.render('Press the \"a\", \"s\", \"w\" and \"d\" keys to move.', True, 'Black', 'Grey')
Instructions_1_Rect = Instructions_1.get_rect(center = (600,300))

Instructions_2 = font_size_40.render('Collect all 7 presents as fast as possible.', True, 'Black', 'Grey')
Instructions_2_Rect = Instructions_2.get_rect(center = (600,400))

Instructions_3 = font_size_40.render('To pick up a present, press the \"e\" key.', True, 'Black', 'Grey')
Instructions_3_Rect = Instructions_3.get_rect(center = (600,500))

#SH - Text for the winning screen
You_Won_Message = font_size_80.render('You Won!', True, "Black", "White") 
You_Won_Message_Rect = You_Won_Message.get_rect() 
You_Won_Message_Rect.center = (600, 150)

textSurfaceObj4 = font_size_80.render('Would You Like to Play Again?', True, "Black", "White") 
textRectObj4 = textSurfaceObj4.get_rect() 
textRectObj4.center = (600, 300)

textSurfaceObj5 = font_size_80.render('Yes', True, "Black", "White") 
textRectObj5 = textSurfaceObj5.get_rect() 
textRectObj5.center = (300, 600)

textSurfaceObj6 = font_size_80.render('No', True, "Black", "White") 
textRectObj6 = textSurfaceObj6.get_rect() 
textRectObj6.center = (900, 600)

#Text for the losing screen
You_Lost_Message = font_size_80.render('You Lost D:', True, "White", "Black") 
You_Lost_Message_Rect = You_Lost_Message.get_rect() 
You_Lost_Message_Rect.center = (600, 150)

textSurfaceObj8 = font_size_80.render('Would You Like to Play Again?', True, "White", "Black") 
textRectObj8 = textSurfaceObj8.get_rect() 
textRectObj8.center = (600, 300)

textSurfaceObj9 = font_size_80.render('Yes', True, "White", "Black") 
textRectObj9 = textSurfaceObj9.get_rect() 
textRectObj9.center = (300, 600)

TitleSurface0 = font_size_80.render('No', True, "White", "Black") 
TitleSurfaceRect0 = TitleSurface0.get_rect() 
TitleSurfaceRect0.center = (900, 600)

#initializes all the game sound effects and the game music
pickUpSound = pygame.mixer.Sound('item-equip-6904.mp3') 
pygame.mixer.music.load('Distant-Sky-Epic-Hybrid-Music-chosic.com_.mp3')
#plays the game music in a infinite loop
pygame.mixer.music.play(-1, 0.0)



#MW function that blits (render sprites onto a background - SH) the intro screen
def intro():
    #MW fills screen and blits two text objects
    screen.fill('White')
    screen.blit(TitleSurface, TitleSurfaceRect) 
    screen.blit(StartGame, StartGameRect) 

#MS - This is the function that blits all the how to play fonts and messages onto the screen.
def how_to_play():
    screen.fill('Grey')
    screen.blit(How_To_Play, How_To_Play_Rect)
    screen.blit(Next_Button, Next_Button_Rect)
    screen.blit(Instructions_1, Instructions_1_Rect) 
    screen.blit(Instructions_2, Instructions_2_Rect)
    screen.blit(Instructions_3, Instructions_3_Rect)

#MS - This is the function that, when called, remindes the player to click e to pick up a present.
def click_e():
    font = pygame.font.Font('my_font.ttf', 40)
    e_button = font.render('click E to pick up', False, (0,0,0))
    e_button_rect = e_button.get_rect(center = (400,400))
    screen.blit(e_button, e_button_rect)

#MW displays a timer on the screen while the game is running 
def display_score():
    #MW calculates the time the level attempt started by substracting the total time by the time at which the start button was pressed
    #MW is then divided by 1000 to get seconds from miliseconds and it is rounded to two decimal places
    current_time = round((pygame.time.get_ticks()-start_time)/1000,1)
    #MW defines text objects for the score value and blits it onto the screen
    score_surf = font_size_80.render(str(current_time), False , "Black")
    score_rect = score_surf.get_rect (topright = (1150,0))
    screen.blit(score_surf, score_rect)
    #MW returns current time
    return current_time

#MW moves the screen to make it seem like te player is moving
def drawFloor10(ground_x, ground_y, moveSpeed):
    #MW takes three int values, ground_x which is the x component of the movement, ground_y which is the y portion of the movement, and moveSpeed which is the speed at which the screen moves when the player presses the movement keys
    #MW moves all the different objects in the game as the player presses movement keys to simulates player movement
    #MW Moves the ground rectangles
    ground_rect.y += ground_y
    ground_rect.x += ground_x
    
    #SH - Moves the enemy *****
    enemy_rect.x += ground_x 
    enemy_rect.y += ground_y 
    
    #MW moves the present item rectangles
    for i in range(7):
        random_present_list[i].x += ground_x
        random_present_list[i].y += ground_y
    
    #Moves every tile in the map matrix
    for tile in tile_list:
        #moves x component of tile rectangle
        tile[1].x += ground_x
        #moves y component of tile rectangle
        tile[1].y += ground_y
        
    #MW checks if there is a collision between the player and one the map tiles
    for tile in tile_list:
        
        #MW checks for the collision
        if player_rect.colliderect(tile[1]):
            #MW if the x component of movement is less than zero all the objects are moved to the right to keep the objects in their original positions as they should not move if the player collides with a tile
            if ground_x < 0:
                ground_rect.x += moveSpeed
                for i in range(7):
                    random_present_list[i].x += moveSpeed
                enemy_rect.x += moveSpeed #*****
                
            #MW if the x component of movement is more than zero all the objects are moved to the left to keep the objects in their original positions as they should not move if the player collides with a tile
            elif ground_x > 0:
                ground_rect.x -= moveSpeed
                for i in range(7):
                    random_present_list[i].x -= moveSpeed
                enemy_rect.x -= moveSpeed #*****
            
            #MW if the y component of movement is less than zero all the objects are moved to down to keep the objects in their original positions as they should not move if the player collides with a tile
            if ground_y < 0:
                ground_rect.y += moveSpeed
                for i in range(7):
                    random_present_list[i].y += moveSpeed
                enemy_rect.y += moveSpeed #*****
            
            #MW if the y component of movement is more than zero all the objects are moved to the left to to keep the objects in their original positions as they should not move if the player collides with a tile
            elif ground_y > 0:
                ground_rect.y -= moveSpeed
                for i in range(7):
                    random_present_list[i].y -= moveSpeed
                enemy_rect.y -= moveSpeed #*****
            
            
            for tile in tile_list:
                #MW if the x component of movement is less than zero all the tiles are moved to the right to move the player object out of collision
                if ground_x < 0:
                    tile[1].x += moveSpeed
                #MW if the x component of movement is more than zero all the tiles are moved to the left to move the player object out of collision
                elif ground_x > 0:
                    tile[1].x -= moveSpeed
                #MW if the x component of movement is less than zero all the tiles are moved to down to move the player object out of collision
                if ground_y < 0:
                    tile[1].y += moveSpeed
                #MW if the y component of movement is more than zero all the tiles are moved up to move the player object out of collision
                elif ground_y > 0:
                    tile[1].y -= moveSpeed 
    
    #MW blits the ground img to the screen as the first layer
    screen.blit(ground,ground_rect)
    
    #MW blits all the map tiles to the screen to generate the map
    for tile in tile_list:
        screen.blit(tile[0],tile[1])
    
#MW changes the player postion depending on what the direction the player should appear to be moving
def movePlayer(player_pos, ground_x, ground_y):
    
    #Changes the player image that is blit onto the screen depending on the direction they are moving
    if ground_x < 0:
        screen.blit(player_right,player_right_rect)
        player_pos = 1
    
    elif ground_x > 0:
        screen.blit(player_left,player_left_rect)
        player_pos = 2
        
    elif ground_y < 0:
        screen.blit(player_back,player_back_rect) 
        player_pos = 3
    
    elif ground_y > 0:
        screen.blit(player_forward,player_forward_rect)
        player_pos = 4
    
    #MW if the player is not moving their last position is what is blit onto the screen
    else:
        if player_pos == 1:
            screen.blit(player_right,player_right_rect)
        
        elif player_pos == 2:
            screen.blit(player_left,player_left_rect)
        
        elif player_pos == 3:
            screen.blit(player_back,player_back_rect)
        
        elif player_pos == 4:
            screen.blit(player_forward,player_forward_rect)
    
    #MW returns the player positon so that it can be reset with the new value
    return player_pos

#SH - This function responds to whether the random present appearance variable is true or false. If true, the present is blitted onto the screen.
#This was originally made of functions for each present, but now it is in one
def presentAppearance():
    if present_appearances[present_index]:
        screen.blit(present_image_list[present_index], random_present_list[present_index])
        #MS - The function tells the player to click e to pick the present up. This only occurs if the player has played once. 
        if player_rect.colliderect(random_present_list[present_index]) and timesPlayed == 0:
            click_e()

#MS - This function blits the collected presents in the top of the screen.
def showPresents(collected_presents):
    for i in range(len(collected_presents)):
        collected_presents[i][1].x = i* tile_size
        collected_presents[i][1].y = 0
        screen.blit(collected_presents[i][0],collected_presents[i][1])
        
#SH - Blits the hearts shouwing the number of lives in the bottom left corner
def showLives():
    for i in range(lives):
        full_heart_rect.x = 1120 - i*80
        full_heart_rect.y = 700
        screen.blit(full_heart, full_heart_rect)

#SH - Blits the enemy onto the screen *****
def showEnemy():
    screen.blit(enemy, enemy_rect)

#MS - This matrix-list makes up the entirety of the map. 
#It is a really efficient way to blit hundreds of objects without taking up hundreds of lines of code.
#This is really useful when programing colisions. When the player colides with a solid tile, the entire matrix-map is moved.
#In a collision, this moves every element at the same time in the same direction as the player so it appears like the player isn't moving at all.
world_data = [
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
[2, 3, 3, 3, 3, 3, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 5, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 6, 6, 0, 6, 6, 6, 0, 6, 6, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 0, 6, 6, 0, 6, 6, 0, 4, 0, 6, 6, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 7, 0, 0, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 9, 9, 0, 4, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 2, 2, 2, 1, 2],
[2, 1, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 4, 1, 2, 2, 2, 1, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 4, 4, 5, 4, 4, 4, 4, 4, 4, 0, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 3, 3, 3, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 3, 3, 3, 0, 0, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 3, 2],
[2, 3, 3, 3, 3, 3, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 2],
[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],]
#SH - A list of the different background elements
background_elements = [outer_wall, inner_wall, ice_block, tree_img, rock_img, bench_down, bench_right, bench_left, bench_up, streetlamp_img]

#MW initializes the map
def init_map():
    #MW negative number so that the map is offset to the left
    row_count =-19
    #MW checks each row in the map matrix
    for row in world_data:
        #MW negative number so that the map is offset up
        col_count = -7 
        #MW checks each element in a row of the map matrix
        for tile in row:
            if tile > 0:
                #MW sets the image that is associated with the number one in the map matrix
                img = pygame.transform.scale(background_elements[tile-1], (tile_size, tile_size))
                #MW sets the rectangle for the image with coordinates that correspond to the col_count and row_count and tile size
                img_rect = img.get_rect(topright = (col_count*tile_size,row_count*tile_size))
                #MW creates a tile image with the image and reactangle
                tile = (img, img_rect)
                #MW appends the tile to the list of all tiles for the map matrix
                tile_list.append(tile)
            
            #MW adds one to column count each time it runs through a element in a row as it is now in the column to the right
            col_count += 1
        #MW adds one to the row count each time it runs through an entire row as it is now one row down
        row_count += 1
    #MW resets the column and row count
    row_count = 0
    col_count = 0
    
init_map()

#MW while True game loop
while True:
    #MW for loop that checks events that occur on the display
    for event in pygame.event.get():
        #MW if the x button at the top of the screen is pressed then the game ends
        if event.type == pygame.QUIT:
            pygame.quit()
        #MW if a button is pressed
        if event.type == pygame.KEYDOWN:
            #MW if the a button is pressed then the x portion of movement is set to the movespeed
            if event.key == pygame.K_a: 
                ground_x=moveSpeed
            #MW if the d button is pressed then the x portion of movement is set to the negative movespeed    
            elif event.key == pygame.K_d:
                ground_x=-moveSpeed
            #MW if the w button is pressed then the y portion of movement is set to the movespeed    
            elif event.key == pygame.K_w: 
                ground_y=moveSpeed
            #MW if the s button is pressed then the y portion of movement is set to the negative movespeed      
            elif event.key == pygame.K_s: 
                ground_y=-moveSpeed
                
        #MW if a button that was pressed is no longer pressed        
        if event.type == pygame.KEYUP:
            #MW sets the x and y components of movement to zero so the player stop moving if the key that was unpressed was w, a, s, or d
            if event.key == pygame.K_a:
                ground_x=0       
            elif event.key == pygame.K_d:
                ground_x=0     
            elif event.key == pygame.K_w: 
                ground_y=0     
            elif event.key == pygame.K_s: 
                ground_y=0
        
        #MS - This checks if the player collides with the present 
        if player_rect.colliderect(random_present_list[present_index]) and present_appearances[present_index]:
            #MS - This first part checks if a key is being pressed
            if event.type == pygame.KEYDOWN:
                #MS - This check determines if the e key is being pressed.
                if event.key == pygame.K_e:
                    pickUpSound.play() 
                    present_appearances[present_index] = False
                    present_appearances[present_index + 1] = True
                    collected_presents.append([present_image_list[present_index],random_present_list[present_index]])
                    present_index+=1
        
        #SH - Checks if the user collides with the enemy *****
        if player_rect.colliderect(enemy_rect):
            lives-=1
            enemy_rect.x -= 250
            
        #MW checks if the user pressed the screen            
        if event.type == pygame.MOUSEBUTTONDOWN:
            #MW checks if the user pressed the start button in the intro
            if StartGameRect.collidepoint(event.pos):
                #MW allows the how to play section of the game to start and the intro section to end
                how_to_play_start = True
                introStart = False
            #MW checks if the user pressed the play again button    
            elif textRectObj5.collidepoint(event.pos) or textRectObj9.collidepoint(event.pos): 
                #starts the game over
                startOver = True
            #MW check if they pressed the no button when asked if they want to restart the game    
            elif textRectObj6.collidepoint(event.pos) or TitleSurfaceRect0.collidepoint(event.pos):
                #MW quits the game
                pygame.quit() 
            #MS - Turns off the how_to_play_start function that I initialized above.
            elif Next_Button_Rect.collidepoint(event.pos):
                controlStart = True
                how_to_play_start = False
                start_time = pygame.time.get_ticks()
    
    #MW checks a boolean variable for whether or not the intro should be blit onto the screen            
    if introStart:
        intro() #Then, the related function is called
        
    #MW - The same applies to the how to play portion of the game    
    elif how_to_play_start:
        how_to_play()
        
    #MW - And for the main portion of the game to be initiated
    elif controlStart:
        #MW fills the screen a base layer grey
        screen.fill("Grey")
        #MW calls upon all the necessary function for the game to run
        drawFloor10(ground_x, ground_y, moveSpeed)
        player_pos = movePlayer(player_pos, ground_x, ground_y)
        presentAppearance()
        #MW shows all the present you collected at the top left corner of your screen
        showPresents(collected_presents)
        #MW gets the score value
        score = display_score()
        showEnemy() #*****
        #SH - Shows the user's lives in the bottom left
        showLives()
    
    #SH - Checks if the player lost all their lives
    if lives == 0:
        controlStart = False
        
        screen.fill('Black')
        screen.blit(You_Lost_Message,You_Lost_Message_Rect)
        screen.blit(textSurfaceObj8,textRectObj8)
        screen.blit(textSurfaceObj9,textRectObj9)
        screen.blit(TitleSurface0,TitleSurfaceRect0)
        
        #MW reinitializes all the variables so that the game can start again at the exact same state
        if startOver:
            #MW makes it so the user isnt prompted with press e too pick a present in their second playthrough
            timesPlayed +=1
            #MW gets new start time 
            start_time = pygame.time.get_ticks()
            ground_rect.x = -7*tile_size
            ground_rect.y = -18*tile_size
            #MW clears the tile list as their coordinates were all moved around by the player
            tile_list.clear()
            #MW recreates the map
            init_map()
            
            #SH - resets present apperance so that the first present is once again the only present on the map
            present_appearances = [True, False, False, False, False, False, False, False]
            present_index = 0
            controlStart = True
            score = 0
            lives = 3 
            
            #MW resets all the presents you collected and resets all of the random presents
            collected_presents.clear()
            random_blue_present = initialize_present_position(blue_present, blue_present_random_positions)
            random_orange_present = initialize_present_position(orange_present, orange_present_random_positions)
            random_green_present = initialize_present_position(green_present, green_present_random_positions)
            random_yellow_present = initialize_present_position(yellow_present, yellow_present_random_positions)
            random_teal_present = initialize_present_position(teal_present, teal_present_random_positions)
            random_red_present = initialize_present_position(red_present, red_present_random_positions)
            random_purple_present = initialize_present_position(purple_present, purple_present_random_positions)
            random_present_list = [random_blue_present, random_orange_present, random_green_present, random_yellow_present, random_teal_present, random_red_present, random_purple_present, random_purple_present]
            enemy_rect = enemy.get_rect(topright = (800,-1000)) #SH - Resets the position of the enemy (Will need to change) *****
            startOver = False
        
    #MW checks if all the presents were collected
    if len(collected_presents)==7:
        #MW stop the game functions from running
        controlStart=False
        
        #MW gets the outro screen and asks the user if they want to play again
        screen.fill('White')
        screen.blit(You_Won_Message,You_Won_Message_Rect)
        screen.blit(textSurfaceObj4,textRectObj4)
        screen.blit(textSurfaceObj5,textRectObj5)
        screen.blit(textSurfaceObj6,textRectObj6)
        
        #MW blits how long it took you to collect all the presents
        score_message = font_size_80.render(f'your score: {score}',False,"Green")
        score_message_rect = score_message.get_rect(center = (600,450)) 
        screen.blit(score_message,score_message_rect)
        
        if startOver:
            timesPlayed +=1
            start_time = pygame.time.get_ticks()
            ground_rect.x = -7*tile_size
            ground_rect.y = -18*tile_size
            tile_list.clear()
            init_map()
        
            present_appearances = [True, False, False, False, False, False, False, False]
            present_index = 0
            controlStart = True
            score = 0
            lives = 3 
            
            collected_presents.clear()
            random_blue_present = initialize_present_position(blue_present, blue_present_random_positions)
            random_orange_present = initialize_present_position(orange_present, orange_present_random_positions)
            random_green_present = initialize_present_position(green_present, green_present_random_positions)
            random_yellow_present = initialize_present_position(yellow_present, yellow_present_random_positions)
            random_teal_present = initialize_present_position(teal_present, teal_present_random_positions)
            random_red_present = initialize_present_position(red_present, red_present_random_positions)
            random_purple_present = initialize_present_position(purple_present, purple_present_random_positions)
            random_present_list = [random_blue_present, random_orange_present, random_green_present, random_yellow_present, random_teal_present, random_red_present, random_purple_present, random_purple_present]
            enemy_rect = enemy.get_rect(topright = (800,-1000)) #*****
            startOver = False
            
    #MW updates the screen        
    pygame.display.update()
    #MW sets tick count to 60
    clock.tick(60)
