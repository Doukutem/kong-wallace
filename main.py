#Blitting tutorial

#3rd party modules
import sys
import pygame
import tcod

#game files
import constants as con

#Tip: break things up into lots of functions!
#Pseudoprogramming is helpful for organizing thoughts.

#This is where everything happens.
'''Structs'''
class struct_Tile:
    def __init__(self, block_path):
        self.block_path = block_path


'''Objects'''
class obj_Actor:
    #i.e.(self, position x, position y, "human", "human.png", component defaults...)
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x #map address
        self.y = y #map address
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        #multiply sprite size by cell size and draw
        SURFACE_MAIN.blit(self.sprite, (self.x*con.CELL_WIDTH, self.y*con.CELL_HEIGHT))
    


'''Components'''
class com_Creature:
    '''
    Creatures have health, can damage other objects by attacking them. Can also die.
    '''
    #i.e. ("tommy", )
    def __init__(self, name_instance, hp = 10, death_function = None):
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def take_damage(self, damage):
        self.hp -= damage
        print(self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp))
        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)
    def move(self, dx, dy):
        tile_is_wall = (GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True)
        target = map_check_for_creature(self.owner.x + dx, self.owner.y + dy, self.owner)
        #if object exists at position and is not itself, then make it a target
        
            
        if target:
            self.attack(target, 3)

        #take in a difference of x and y relative to the actor, consult map to see if it is blocked
        if not tile_is_wall:
            #if it isn't blocked, then move by adding dx,dy to actor position
            self.owner.x += dx
            self.owner.y += dy
    def attack(self, target, damage):
        
        print(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!")
        
        target.creature.take_damage(damage)
class ai_Test:
    '''Once per turn, execute ai instructions.'''
    def take_turn(self):
        #ai test. every round the object chooses a random direction to move to, or stay still
        self.owner.creature.move(tcod.random_get_int(0, -1, 1), tcod.random_get_int(0, -1, 1))

def death_monster(monster):
    '''On death, most monsters stop moving.'''

    print(monster.creature.name_instance + " is dead!")

    monster.creature = None
    monster.ai = None

# class com_Item:

# class com_Container:


'''Map'''
def map_create():
    # Nested list comprehension (creates an array of struct_tile con.MAP_WIDTH wide by con.MAP_HEIGHT tall)
    new_map = [[struct_Tile(False) for y in range(0, con.MAP_HEIGHT)] for x in range(0, con.MAP_WIDTH)]
    # new_map tile at (x=10, y=10) is going to be a wall 
    new_map[10][10].block_path = True
    # new_map tile at (x=10, y=15) is going to be a wall 
    new_map[10][15].block_path = True

    #block top [x][0] and bottom [x][con.MAP_HEIGHT-1] borders off
    for x in range(con.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][con.MAP_HEIGHT-1].block_path = True

    #block left [0][y] and right [con.MAP_WIDTH-1][y] borders off
    for y in range(con.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[con.MAP_WIDTH-1][y].block_path = True
    return new_map

def map_check_for_creature(x, y, exclude_object = None):
    target = None
    
    if exclude_object:
        #check objectlist to find creature at that location that isn't excluded
        for object in GAME_OBJECTS:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and
                object.creature):

                target = object

            if target:
                return target
    else:
        #check objectlist to find any creature at that location
        for object in GAME_OBJECTS:
            if (object.x == x and
                object.y == y and
                object.creature):

                target = object

            if target:
                return target


'''Drawing'''
def draw_game():
    '''This function contains all screen draws.'''
    global SURFACE_MAIN
    #clear the surface
    SURFACE_MAIN.fill(con.COLOR_DEFAULT_BG)

    #draw the map
    draw_map(GAME_MAP)
    #draw all objects
    for obj in GAME_OBJECTS:
        obj.draw()
    
    #update the display with flip
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, con.MAP_WIDTH):
        for y in range(0, con.MAP_HEIGHT):
            if map_to_draw[x][y].block_path:
                #draw wall surfaces onto main surface, positions marked by map coordinates
                SURFACE_MAIN.blit(con.S_WALL, (x * con.CELL_WIDTH, y * con.CELL_HEIGHT))
            else:
                #draw floor surfaces everywhere else
                SURFACE_MAIN.blit(con.S_FLOOR, (x * con.CELL_WIDTH, y * con.CELL_HEIGHT))


'''Game Loop'''
def game_main_loop():
    '''In this function, we loop the main game'''
    game_quit = False
    player_action = "no-action"
    while not game_quit:

        #handle keys
        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True
        
        elif player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()
        #draw the game
        draw_game()

    #quit the game, cleanup
    pygame.quit()
    exit()

def game_initialize():
    '''This function initializes the main window, and pygame'''
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS
    #initialize pygame
    pygame.init()
    #(x,y) tuple represents window dimensions
    SURFACE_MAIN = pygame.display.set_mode((con.CELL_WIDTH*con.MAP_WIDTH, 
                                            con.CELL_HEIGHT*con.MAP_HEIGHT))

    GAME_MAP = map_create()
    creature_com1 = com_Creature("greg", death_function = death_monster)
    PLAYER = obj_Actor(1, 1, "python", con.S_PLAYER, creature = creature_com1)

    creature_com2 = com_Creature("jackie", death_function = death_monster)
    ai_com = ai_Test()
    ENEMY = obj_Actor(15, 15, "crab", con.S_ENEMY, creature = creature_com2, ai = ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]

def game_handle_keys():
    #1. get player input

    #this collects all the events that have occurred recently
    events_list = pygame.event.get()   
    #2. process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                return "player-moved"

            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                return "player-moved"

            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                return "player-moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                return "player-moved"
    return "no-action"


'''Main method'''
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
