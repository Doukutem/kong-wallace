#Blitting tutorial

#3rd party modules
import sys
import pygame
import tcod

#game files
import constants

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
    def __init__(self, x, y, name_object, sprite, creature = None):
        self.x = x #map address
        self.y = y #map address
        self.sprite = sprite

        if creature:
            self.creature = creature
            creature.owner = self
    def draw(self):
        #multiply sprite size by cell size and draw
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))
    def move(self, dx, dy):
        #take in a difference of x and y relative to the actor, consult map to see if it is blocked
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            #if it isn't blocked, then move by adding dx,dy to actor position
            self.x += dx
            self.y += dy


'''Components'''
class com_Creature:
    '''
    Creatures have health, can damage other objects by attacking them. Can also die.
    '''
    #i.e. ("tommy", )
    def __init__(self, name_instance, hp = 10):
        self.name_instance = name_instance
        self.hp = hp


# class com_Item:

# class com_Container:

'''Map'''
def map_create():
    # Nested list comprehension (creates an array of struct_tile constants.MAP_WIDTH wide by constants.MAP_HEIGHT tall)
    new_map = [[struct_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]
    # new_map tile at (x=10, y=10) is going to be a wall 
    new_map[10][10].block_path = True
    # new_map tile at (x=10, y=15) is going to be a wall 
    new_map[10][15].block_path = True
    return new_map


'''Drawing'''
def draw_game():
    '''This function contains all screen draws.'''
    global SURFACE_MAIN
    #clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    #draw the map
    draw_map(GAME_MAP)
    #draw the character
    ENEMY.draw()
    PLAYER.draw()
    


    #update the display with flip
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path:
                #draw wall surfaces onto main surface, positions marked by map coordinates
                SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                #draw floor surfaces everywhere else
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


'''Game Loop'''

def game_main_loop():
    '''In this function, we loop the main game'''
    game_quit = False
    while not game_quit:
        #1. get player input

        #this collects all the events that have occurred recently
        events_list = pygame.event.get()
        
        #2. process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)
        


        #3. draw the game
        draw_game()

    #quit the game, cleanup
    pygame.quit()
    sys.exit

def game_initialize():
    '''This function initializes the main window, and pygame'''
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY
    #initialize pygame
    pygame.init()
    #(x,y) tuple represents window dimensions
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = map_create()
    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(0, 0, "python", constants.S_PLAYER, creature = creature_com1)

    creature_com2 = com_Creature("jackie")
    ENEMY = obj_Actor(15, 15, "crab", constants.S_ENEMY, creature = creature_com2)

'''Main method'''
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
