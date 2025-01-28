import random

from config import *
import terrain

monster_grid = [False] * (w * h)

def place_monsters(chest_grid):
    global monster_grid
    monster_grid = [False] * (w * h)  # Initialize new monster grid
    monster_per_chest = {}

    for j in range(h):
        for i in range(w):

            # Check if the tile is ground and not already occupied by objects or monsters
            if (terrain.tile_map[i + j * w] in [GROUND, GROUND_BONES, GROUND_STONE] and
                    not monster_grid[i + j * w] and not chest_grid[i + j * w]):

                # MONSTER PLACING
                #is_suitable = True

                # Check if away from walls
                #directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                #for dx, dy in directions:
                #    for k in range(1, 3):
                #        nx, ny = i + (dx*k), j + (dy*k)
                #        if 0 < nx < w-1 and 0 < ny < h-1:
                #            # Into boundaries
                #            tile = terrain.tiles[nx + ny * w]
                #
                #            if not tile:
                #                # it is not near a wall
                #                is_suitable = is_suitable and True
                #            else:
                #                is_suitable = is_suitable and False

                # See if there is a chest in radius of 5
                has_chest = False
                radius = MONSTER_RADIUS

                for x in range(i - radius, i + radius + 1):
                    for y in range(j - radius, j + radius + 1):
                        # Check if the cell is within the grid bounds
                        if (0 <= x < w) and (0 <= y < h):
                            # Calculate the distance from the center cell (x, y)
                            distance = max(abs(x - i), abs(y - j))
                            if distance <= radius:
                                # If there is a chest nearby and it has spawn probability
                                if chest_grid[x + y * w] == terrain.tile_set["CHEST"] and random.random() < MONSTER_PROB:
                                    has_chest = True
                                    if (x + y * w) in monster_per_chest:
                                        monster_per_chest[x + y * w] += 1
                                    else:
                                        monster_per_chest[x + y * w] = 1

                                    # It there are too many monsters it will not spawn
                                    if monster_per_chest[x + y * w] > MAX_MONSTERS:
                                        has_chest = False

                if has_chest:
                    monster_grid[i + j * w] = terrain.tile_set["MONSTER"]


    return monster_grid

def save_monsters_to_json():
    global monster_grid
    monster_layer = {
        "name": "Layer_2",
        "tiles": []
    }
    for j in range(h):
        for i in range(w):
            # Add monsters
            if monster_grid[i + j * w] == terrain.tile_set["MONSTER"]:
                monster_layer["tiles"].append({
                    "id": "MONSTER",
                    "x": i,
                    "y": j
                })


    return monster_layer