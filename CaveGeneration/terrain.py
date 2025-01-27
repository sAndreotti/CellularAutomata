import pygame
import random

from pandas.core.arrays.datetimes import objects_to_datetime64ns

from config import *
import objects

# Set tile sprites
GROUND_BONES = 109
GROUND_STONE = 107
GROUND = 45
VOID = 30
ISOLATED = 11

CON_U = 24
CON_U2 = 49
CON_U3 = 65
CON_U4 = 101

CON_D = 13
CON_D2 = 9
CON_D3 = 79
CON_D4 = 80
CON_D5 = 81

CON_L = 28
CON_L2 = 53
CON_L3 = 75
CON_L4 = 89
CON_L5 = 93
CON_L6 = 99

CON_R = 26
CON_R2 = 51
CON_R3 = 86
CON_R4 = 91
CON_R5 = 97

CON_LR = 4
CON_LR2 = 5
CON_LR3 = 6
CON_LR4 = 59
CON_LR5 = 59
CON_LR6 = 60
CON_LR7 = 77
CON_LR8 = 98

CON_UD = 19
CON_UD2 = 23
CON_UD3 = 33
CON_UD4 = 37
CON_UD5 = 44
CON_UD6 = 48

CON_UR = 57
CON_UL = 61

CON_DR = 3
CON_DL = 7

CON_LUR = 27
CON_LDR = 52
CON_LUD = 87
CON_URD = 88

CON_LURD = 92

# Initialize tiles and tile map
tiles = []
tile_map = []

# Load textures
tile_set = {}

# Texture variants
U_LIST = [CON_U, CON_U2, CON_U3, CON_U4]
D_LIST = [CON_D, CON_D2, CON_D3, CON_D4, CON_D5]
R_LIST = [CON_R, CON_R2, CON_R3, CON_R4, CON_R5]
L_LIST = [CON_L, CON_L2, CON_L3, CON_L4, CON_L5, CON_L6]

LR_LIST = [CON_LR, CON_LR2, CON_LR3, CON_LR4, CON_LR5, CON_LR6, CON_LR7, CON_LR8]
UD_LIST = [CON_UD, CON_UD2, CON_UD3, CON_UD4, CON_UD5, CON_UD6]


def preload():
    # Load tiles
    tile_list = [GROUND_BONES, GROUND_STONE, GROUND, VOID, ISOLATED, CON_U, CON_U2, CON_U3, CON_U4, CON_D, CON_D2,
                 CON_D3, CON_D4, CON_D5, CON_L, CON_L2, CON_L3, CON_L4, CON_L5, CON_L6, CON_R, CON_R2, CON_R3, CON_R4,
                 CON_R5, CON_LR, CON_LR2, CON_LR3, CON_LR4, CON_LR5, CON_LR6, CON_LR7, CON_LR8, CON_UD, CON_UD2,
                 CON_UD3, CON_UD4, CON_UD5, CON_UD6, CON_UR, CON_UL, CON_DR, CON_DL, CON_LUR, CON_LDR, CON_LUD,
                 CON_URD, CON_LURD]

    for tile in tile_list:
        load_tiles(tile)

    # Objects
    # Load chest texture
    tile_set["CHEST"] = pygame.image.load("textures/chest.png")

def load_tiles(tile_name: str):
    tile_set[tile_name] = pygame.image.load("textures/Tile_" + str(tile_name) + ".png").convert_alpha()

def to_tile_set():
    global tile_map
    tile_map = []
    for j in range(h):
        for i in range(w):
            # Ensure border cells are walls or VOID
            if i == 0 or i == w - 1 or j == 0 or j == h - 1:
                # Border cells are always walls or VOID
                if num_walls_around(i, j) == 9:
                    tile_map.append(VOID)
                else:
                    tile_map.append(ISOLATED)
            else:
                solid = is_solid(i, j)
                if solid:
                    # Check if the cell is completely surrounded by walls (VOID)
                    if num_walls_around(i, j) == 9:
                        tile_map.append(VOID)
                    else:
                        # Assign a general wall type (e.g., ISOLATED) during initial generation
                        tile_map.append(ISOLATED)
                else:
                    if random.random() < 0.02:
                        if random.random() < 0.5:
                            tile_map.append(GROUND_STONE)
                        else:
                            tile_map.append(GROUND_BONES)
                    else:
                        tile_map.append(GROUND)

    # After generating the tile map, analyze and update wall types
    update_sprites()

def update_sprites():
    for j in range(h):
        for i in range(w):
            if is_wall(i, j):
                coord = i + j * w
                # If not is at the margins
                if not (i == 0 or i == w - 1 or j == 0 or j == h - 1):
                    left = is_wall(i-1, j) # Left cell
                    right = is_wall(i+1, j) # Right cell
                    up = is_wall(i, j-1) # Up cell
                    down = is_wall(i, j+1) # Down cell

                    set_wall_type(coord, left, right, up, down)

                else:
                    # Cell is at margin
                    if i == 0 and j == 0:
                        # left up
                        right = is_wall(i+1, j) # Right cell
                        down = is_wall(i, j+1) # Down cell
                        set_wall_type(coord, False, right, False, down)
                    elif i == w - 1 and j == 0:
                        # right up
                        left = is_wall(i - 1, j)  # Left cell
                        down = is_wall(i, j + 1)  # Down cell
                        set_wall_type(coord, left, False, False, down)
                    elif i == 0 and j == h - 1:
                        # left down
                        right = is_wall(i + 1, j)  # Right cell
                        up = is_wall(i, j - 1)  # Up cell
                        set_wall_type(coord, False, right, up, False)
                    elif i == w - 1 and j == h - 1:
                        # right down
                        left = is_wall(i - 1, j)  # Left cell
                        up = is_wall(i, j - 1)  # Up cell
                        set_wall_type(coord, left, False, up, False)
                    else:

                        # One margin
                        if i == 0:
                            # left most
                            right = is_wall(i+1, j) # Right cell
                            up = is_wall(i, j-1) # Up cell
                            down = is_wall(i, j+1) # Down cell
                            set_wall_type(coord, False, right, up, down)

                        elif i == w - 1:
                            # right most
                            left = is_wall(i - 1, j)  # Left cell
                            up = is_wall(i, j - 1)  # Up cell
                            down = is_wall(i, j + 1)  # Down cell
                            set_wall_type(coord, left, False, up, down)

                        elif j == 0:
                            # top most
                            left = is_wall(i - 1, j)  # Left cell
                            right = is_wall(i + 1, j)  # Right cell
                            down = is_wall(i, j + 1)  # Down cell
                            set_wall_type(coord, left, right, False, down)

                        elif j == h - 1:
                            # down most
                            left = is_wall(i - 1, j)  # Left cell
                            right = is_wall(i + 1, j)  # Right cell
                            up = is_wall(i, j - 1)  # Up cell
                            set_wall_type(coord, left, right, up, False)

def is_wall(i, j):
    if (tile_map[i + j * w] == VOID or tile_map[i + j * w] == GROUND_STONE or
            tile_map[i + j * w] == GROUND_BONES or tile_map[i + j * w] == GROUND):
        return False
    else:
        return True

def set_wall_type(coord, left, right, up, down):
    # Full connected
    if left and right and up and down:
        tile_map[coord] = CON_LURD
    else:
        # Three connected
        if left and right and up:
            tile_map[coord] = CON_URD
        elif left and right and down:
            tile_map[coord] = CON_LDR
        elif up and right and down:
            tile_map[coord] = CON_URD
        elif up and left and down:
            tile_map[coord] = CON_LUD
        else:
            # Corners
            if left and up:
                tile_map[coord] = CON_UL
            elif left and down:
                tile_map[coord] = CON_DL
            elif right and down:
                tile_map[coord] = CON_DR
            elif right and up:
                tile_map[coord] = CON_UR
            else:
                # Two connected
                if left and right:
                    tile_map[coord] = random.choice(LR_LIST)
                elif up and down:
                    tile_map[coord] = random.choice(UD_LIST)
                else:
                    # One connected
                    if left:
                        tile_map[coord] = random.choice(L_LIST)
                    elif right:
                        tile_map[coord] = random.choice(R_LIST)
                    elif up:
                        tile_map[coord] = random.choice(U_LIST)
                    elif down:
                        tile_map[coord] = random.choice(D_LIST)

def is_solid(x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return True  # Treat out-of-bounds tiles as solid (walls)
    if tiles[x + y * w] not in [VOID, ISOLATED, GROUND, GROUND_STONE, GROUND_BONES]:
        return tiles[x + y * w]  # Only check the tiles list for solidity
    else:
        return False

def iterate_tiles():
    global tiles
    new_tiles = []
    for j in range(h):
        for i in range(w):
            # Ensure tiles at the margins remain walls
            if i == 0 or i == w - 1 or j == 0 or j == h - 1:
                new_tiles.append(True)  # Solid (wall)
            else:
                # If True = wall
                num = num_walls_around(i, j)
                new_tile = num >= N_WALL
                new_tiles.append(new_tile)
    tiles = new_tiles

def num_walls_around(x, y):
    num = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_solid(x + i, y + j):
                num += 1
    return num

def wall_count():
    # Count how much walls there are
    wall_count = 0

    for j in range(h):
        for i in range(w):
            if is_wall(i, j):
                wall_count += 1

    return wall_count