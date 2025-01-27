# Constants

# Map size
w, h = 50, 50
GRID_WIDTH, GRID_HEIGHT = 600, 600  # Size of the grid area

# Number of wall to keep it
N_WALL = 5

# Radius for chest to spawn
#RADIUS = 7
RADIUS = int(w/10)

# Window sizes
BUTTON_WIDTH, BUTTON_HEIGHT = 160, 40  # Size of the button
WINDOW_WIDTH = GRID_WIDTH + BUTTON_WIDTH + 20  # Total window width (grid + button + padding)
WINDOW_HEIGHT = GRID_HEIGHT  # Window height remains the same
TILE_SIZE = GRID_WIDTH // w