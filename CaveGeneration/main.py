import json
import random

import pygame
import terrain
from CaveGeneration.monsters import save_monsters_to_json, monster_grid, place_monsters
from config import *
from CaveGeneration.objects import place_chests, save_chests_to_json

show_text = False


def setup():
    global tiles, chest_grid
    terrain.tiles = []
    chest_grid = [False] * (w * h)

    for j in range(h):
        for i in range(w):
            # Ensure tiles at the margins are always walls
            if i == 0 or i == w - 1 or j == 0 or j == h - 1:
                terrain.tiles.append(True)  # Solid (wall)
            else:
                solid = random.random() < INITIAL_PROB
                terrain.tiles.append(solid)
    terrain.to_tile_set()


def draw(screen):
    global show_text
    screen.fill((24, 20, 37))

    # Draw the grid
    for j in range(h):
        for i in range(w):
            tile = terrain.tile_map[i + j * w]
            img = terrain.tile_set[tile]
            screen.blit(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))

            if terrain.old_tile_map and DEPTH:
                tile = terrain.old_tile_map[i + j * w]
                img = terrain.tile_set[tile]
                screen.blit(pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))

            # Draw chests
            if chest_grid[i + j * w] == terrain.tile_set["CHEST"]:
                chest_img = terrain.tile_set["CHEST"]
                screen.blit(pygame.transform.scale(chest_img, (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))
            elif chest_grid[i + j * w] == terrain.tile_set["BAG"]:
                bag_img = terrain.tile_set["BAG"]
                screen.blit(pygame.transform.scale(bag_img, (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))

            if monster_grid[i + j * w] == terrain.tile_set["MONSTER"]:
                monster_img = terrain.tile_set["MONSTER"]
                screen.blit(pygame.transform.scale(monster_img, (TILE_SIZE, TILE_SIZE)), (i * TILE_SIZE, j * TILE_SIZE))

    # Draw the save button to the right of the grid
    save_button = pygame.Rect(GRID_WIDTH + 10, (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (65, 53, 102), save_button)
    font = pygame.font.Font(None, 36)
    text = font.render("Save Image", True, (192, 203, 220))
    screen.blit(text, (GRID_WIDTH + 20, (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + 10))

    # Draw the save button
    save_file_button = pygame.Rect(GRID_WIDTH + 10, (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + 10 + BUTTON_HEIGHT,
                                   BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (65, 53, 102), save_file_button)
    font = pygame.font.Font(None, 36)
    text2 = font.render("Save Map", True, (192, 203, 220))
    screen.blit(text2, (GRID_WIDTH + 20, (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + 20 + BUTTON_HEIGHT))

    if show_text:
        text3 = font.render("Walls stable", True, (192, 203, 220))
        screen.blit(text3, (GRID_WIDTH + 20, (WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 - 20 - BUTTON_HEIGHT))

    pygame.display.flip()


def save_grid_to_json():
    layers = [tile_list("Layer_0"), save_chests_to_json(), save_monsters_to_json()]

    # If it is enabled save also previous layer
    if DEPTH:
        layer = {
            "name": "Layer_10",
            "tiles": []
        }
        for j in range(h):
            for i in range(w):
                tile_id = terrain.old_tile_map[i + j * w]
                layer["tiles"].append({
                    "id": str(tile_id),
                    "x": i,
                    "y": j
                })
        layers.append(layer)

    with open("output/map.json", "w") as f:
        json.dump({"layers": layers}, f, indent=4)

    print("Saved grid to map.json")


def tile_list(layer_name):
    layer = {
        "name": layer_name,
        "tiles": []
    }
    for j in range(h):
        for i in range(w):
            tile_id = terrain.tile_map[i + j * w]
            layer["tiles"].append({
                "id": str(tile_id),
                "x": i,
                "y": j
            })

    return layer


def save_image(screen):
    # Save only the grid area (not the button) as an image file
    grid_surface = screen.subsurface(pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT))
    pygame.image.save(grid_surface, "output/map.png")
    print("Image saved as map.png")


def main():
    global chest_grid, show_text, monster_grid
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Cellular Automata Cave Generation")
    clock = pygame.time.Clock()

    actual_walls = 0
    terrain.preload()
    setup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if the save button is clicked
                mouse_pos = pygame.mouse.get_pos()
                if GRID_WIDTH + 10 <= mouse_pos[0] <= GRID_WIDTH + 10 + BUTTON_WIDTH and (
                        WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 <= mouse_pos[1] <= (
                        WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + BUTTON_HEIGHT:
                    print("Saving image...")
                    save_image(screen)
                elif GRID_WIDTH + 10 <= mouse_pos[0] <= GRID_WIDTH + 10 + BUTTON_WIDTH and (
                        WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + BUTTON_HEIGHT <= mouse_pos[1] <= (
                        WINDOW_HEIGHT - BUTTON_HEIGHT) // 2 + (2 * BUTTON_HEIGHT):
                    print("Saving map...")
                    save_grid_to_json()
                else:
                    if UPDATE_MODE == "RANDOM":
                        terrain.iterate_tiles_randomly()
                    else:
                        terrain.iterate_tiles()

                    terrain.to_tile_set()
                    chest_grid = place_chests()
                    monster_grid = place_monsters(chest_grid)

                    if actual_walls == terrain.wall_count():
                        show_text = True
                    else:
                        actual_walls = terrain.wall_count()

        draw(screen)
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
