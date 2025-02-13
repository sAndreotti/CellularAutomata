import pygame
import random

from config import *

# Initialize tiles and tile map
tiles = []
tile_map = []
old_tile_map = []

# Load textures
tile_set = {}
alpha = 255


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
    tile_set["BAG"] = pygame.image.load("textures/bag.png")

    # Monsters
    # Load monster texture
    tile_set["MONSTER"] = pygame.image.load("textures/monster.png")


def load_tiles(tile_name: str):
    global alpha
    tile_set[tile_name] = pygame.image.load("textures/Tile_" + str(tile_name) + ".png").convert_alpha()
    # Alpha can be modified for future implementations
    if DEPTH:
        alpha = 192

    tile_set[tile_name].set_alpha(alpha)


def to_tile_set():
    global tile_map, old_tile_map

    if DEPTH:
        old_tile_map = tile_map

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
                    if random.random() < 0.05:
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
                    left = is_wall(i - 1, j)  # Left cell
                    right = is_wall(i + 1, j)  # Right cell
                    up = is_wall(i, j - 1)  # Up cell
                    down = is_wall(i, j + 1)  # Down cell

                    set_wall_type(coord, left, right, up, down)

                else:
                    # Cell is at margin
                    if i == 0 and j == 0:
                        # left up
                        right = is_wall(i + 1, j)  # Right cell
                        down = is_wall(i, j + 1)  # Down cell
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
                            right = is_wall(i + 1, j)  # Right cell
                            up = is_wall(i, j - 1)  # Up cell
                            down = is_wall(i, j + 1)  # Down cell
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


def is_solid(x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return True  # Treat out-of-bounds tiles as solid (walls)
    if tiles[x + y * w] not in [VOID, ISOLATED, GROUND, GROUND_STONE, GROUND_BONES]:
        return tiles[x + y * w]  # Only check the tiles list for solidity
    else:
        return False


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


def iterate_tiles():
    """
    Function that make an iteraction for all the terrain cells
    """

    global tiles
    new_tiles = []
    for j in range(h):
        for i in range(w):
            # Add the new tile to the grid
            new_tiles.append(iterate(i, j))

    tiles = new_tiles


def iterate_tiles_randomly():
    """
    Function that make an iteraction for all the terrain cells in random order
    """

    global tiles
    new_tiles = []

    # Create a list of all cell coordinates
    cell_coords = [(i, j) for j in range(h) for i in range(w)]
    random.shuffle(cell_coords)  # Shuffle the list

    for i, j in cell_coords:
        # Add the new tile to the grid
        new_tiles.append(iterate(i, j))

    tiles = new_tiles  # Update the tiles


def iterate(i: int, j: int):
    """
    Function that actually calculate the state for the cells
    """

    new_tile = []
    # Ensure tiles at the margins remain walls
    if i == 0 or i == w - 1 or j == 0 or j == h - 1:
        return True  # Solid (wall)
    else:
        if RULE == 1:
            # Rule 1: A cell becomes solid if it has 5 or more solid neighbors
            num = num_walls_around(i, j)
            new_tile = num >= 5
        elif RULE == 2:
            # Rule 2: A cell becomes solid if it has exactly 5 solid neighbors
            num = num_walls_around(i, j)
            new_tile = num == 5
        elif RULE == 3:
            # Rule 3: A cell becomes solid if it has 3 or more solid neighbors in a 5x5 area
            new_tile = num_walls_in_area(i, j, 5) >= 3
        elif RULE == 4:
            # Rule 4: A cell becomes solid if it has at least 2 solid neighbors in a 3x3 area
            new_tile = num_walls_in_area(i, j, 3) >= 2
        elif RULE == 5:
            # Rule 5: A cell becomes solid if it has more than 6 solid neighbors
            num = num_walls_around(i, j)
            new_tile = num > 6
        elif RULE == 6:
            # Rule 6: A cell becomes solid if it has fewer than 2 solid neighbors
            num = num_walls_around(i, j)
            new_tile = num < 2
        elif RULE == 7:
            # Rule 7: A cell becomes solid if it has an even number of solid neighbors
            num = num_walls_around(i, j)
            new_tile = num % 2 == 0
        elif RULE == 8:
            # Rule 8: A cell becomes solid if it has a prime number of solid neighbors
            # Better results with 3 and 5
            num = num_walls_around(i, j)
            new_tile = num in [2, 3, 5, 7]

        return new_tile


def num_walls_around(x, y):
    num = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_solid(x + i, y + j):
                num += 1
    return num


def num_walls_in_area(x, y, radius):
    count = 0
    for i in range(x - radius, x + radius + 1):
        for j in range(y - radius, y + radius + 1):
            if is_solid(i, j):
                count += 1
    return count


def wall_count():
    # Count how much walls there are
    wall_count = 0

    for j in range(h):
        for i in range(w):
            if is_wall(i, j):
                wall_count += 1

    return wall_count
