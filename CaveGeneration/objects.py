import json
import random

from config import *
import terrain

GROUND_BONES = 109
GROUND_STONE = 107
GROUND = 45
VOID = 30
ISOLATED = 11

def place_chests():
    chest_grid = [False] * (w * h)  # Initialize chest grid
    for j in range(h):
        for i in range(w):
            # Check if the tile is ground and not already a chest
            if terrain.tile_map[i + j * w] in [GROUND, GROUND_BONES, GROUND_STONE] and not chest_grid[i + j * w]:
                is_suitable = True

                # Check if away from walls
                directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                for dx, dy in directions:
                    for k in range(1, 3):
                        nx, ny = i + (dx*k), j + (dy*k)
                        if 0 < nx < w-1 and 0 < ny < h-1:
                            # Into boundaries
                            tile = terrain.tiles[nx + ny * w]

                            if not tile:
                                # it is not near a wall
                                is_suitable = is_suitable and True
                            else:
                                is_suitable = is_suitable and False

                # See if there is a chest in radius of 5
                has_chest = False
                radius = RADIUS

                for x in range(i - radius, i + radius + 1):
                    for y in range(j - radius, j + radius + 1):
                        # Check if the cell is within the grid bounds
                        if (0 <= x < w) and (0 <= y < h):
                            # Calculate the distance from the center cell (x, y)
                            distance = max(abs(x - i), abs(y - j))
                            if distance <= radius:
                                # Add the cell's coordinates and solidity to the list
                                has_chest = has_chest or chest_grid[x + y * w]

                if is_suitable and not has_chest:
                    chest_grid[i + j * w] = terrain.tile_set["CHEST"]

                # if it it a chest it has chance to spawn little bags
                radius = 1
                for x in range(i - radius, i + radius + 1):
                    for y in range(j - radius, j + radius + 1):
                        # Check if the cell is within the grid bounds
                        if (0 <= x < w) and (0 <= y < h):
                            # Calculate the distance from the center cell (x, y)
                            distance = max(abs(x - i), abs(y - j))
                            # If the tile is in distance and the origin is a chest
                            if distance <= radius and chest_grid[i + j * w] and not terrain.is_solid(x, y):
                                # Probabiliry to spawn a bag
                                if random.random() < 0.05:
                                    chest_grid[x + y * w] = terrain.tile_set["BAG"]

    return chest_grid

def save_chests_to_json(chest_grid, filename="map.json"):
    """
    Saves the chest locations to a JSON file.
    """
    chest_layer = {
        "name": "Chests",
        "tiles": []
    }
    for j in range(h):
        for i in range(w):
            if chest_grid[i + j * w]:
                chest_layer["tiles"].append({
                    "id": "CHEST",
                    "x": i,
                    "y": j
                })
    with open(filename, "w") as f:
        json.dump({"layers": [chest_layer]}, f, indent=4)
    print(f"Chest locations saved to {filename}")