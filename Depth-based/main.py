import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Parameters
width, height = 100, 100  # Grid dimensions
iterations = 1000  # Total number of simulation steps
cell_size = 5  # Size of each cell in pixels
rule = "Majority r9"  # Default rule (can be changed)

# Initialize the grid randomly (0 = dead, 1 = alive)
grid = np.random.choice([0, 1], size=(width, height), p=[0.5, 0.5])  # 50% alive, 50% dead

# Initialize the depth grid to track how many times a cell has died
depth_grid = np.zeros((width, height), dtype=int)


def count_alive_neighbors(grid, x, y):
    """Count the number of alive neighbors for a cell at (x, y)."""
    alive = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            nx, ny = x + i, y + j
            if 0 <= nx < width and 0 <= ny < height:
                alive += grid[nx, ny]
    return alive


def update_grid(grid, depth_grid, rule):
    """Update the grid synchronously based on the selected rule."""
    new_grid = np.copy(grid)  # Create a copy to store the new states
    new_depth_grid = np.copy(depth_grid)  # Create a copy to store the new depth states
    for x in range(width):
        for y in range(height):
            alive_neighbors = count_alive_neighbors(grid, x, y)
            if rule.startswith("Majority"):
                # Majority rule: Cell survives if n > N, is born if n > N
                try:
                    N = int(rule.split("r")[1])  # Extract N from the rule name
                except (IndexError, ValueError):
                    N = 5  # Default value if extraction fails
                if grid[x, y] == 1:
                    if alive_neighbors > N:
                        new_grid[x, y] = 1  # Survive
                    else:
                        new_grid[x, y] = 0  # Die
                        new_depth_grid[x, y] += 1  # Increment depth if cell dies
                else:
                    if alive_neighbors > N:
                        new_grid[x, y] = 1  # Born
                    else:
                        new_grid[x, y] = 0  # Remain dead
            elif rule.startswith("Caves"):
                # Caves rule: Cell survives if n > N - 1, is born if n > N
                try:
                    N = int(rule.split("r")[1])  # Extract N from the rule name
                except (IndexError, ValueError):
                    N = 5  # Default value if extraction fails
                if grid[x, y] == 1:
                    if alive_neighbors > N - 1:
                        new_grid[x, y] = 1  # Survive
                    else:
                        new_grid[x, y] = 0  # Die
                        new_depth_grid[x, y] += 1  # Increment depth if cell dies
                else:
                    if alive_neighbors > N:
                        new_grid[x, y] = 1  # Born
                    else:
                        new_grid[x, y] = 0  # Remain dead
            elif rule == "Diamoeba":
                # Diamoeba rule: Cell survives if n > 5, is born if n in {3, 5, 6, 7, 8}
                if grid[x, y] == 1:
                    if alive_neighbors > 5:
                        new_grid[x, y] = 1  # Survive
                    else:
                        new_grid[x, y] = 0  # Die
                        new_depth_grid[x, y] += 1  # Increment depth if cell dies
                else:
                    if alive_neighbors in {3, 5, 6, 7, 8}:
                        new_grid[x, y] = 1  # Born
                    else:
                        new_grid[x, y] = 0  # Remain dead
            elif rule == "Coral":
                # Coral rule: Cell survives if n > 4, is born if n = 3
                if grid[x, y] == 1:
                    if alive_neighbors > 4:
                        new_grid[x, y] = 1  # Survive
                    else:
                        new_grid[x, y] = 0  # Die
                        new_depth_grid[x, y] += 1  # Increment depth if cell dies
                else:
                    if alive_neighbors == 3:
                        new_grid[x, y] = 1  # Born
                    else:
                        new_grid[x, y] = 0  # Remain dead
    return new_grid, new_depth_grid


def create_image_from_grid(depth_grid):
    """Convert the depth grid into an image for display."""
    # Normalize depth values for coloring
    if np.max(depth_grid) > 0:
        normalized_depth = depth_grid / np.max(depth_grid)
    else:
        normalized_depth = depth_grid

    # Invert the depth values (optional: swap black and white)
    normalized_depth = 1 - normalized_depth  # Uncomment this line to invert colors

    # Scale the grid to the desired cell size
    scaled_grid = np.kron(normalized_depth, np.ones((cell_size, cell_size)))

    # Convert to an image
    image = Image.fromarray(np.uint8(scaled_grid * 255), mode='L')
    return ImageTk.PhotoImage(image)


def update_frame():
    """Update the grid and display it in the GUI."""
    global grid, depth_grid, canvas, photo, rule
    grid, depth_grid = update_grid(grid, depth_grid, rule)

    # Create an image from the depth grid
    photo = create_image_from_grid(depth_grid)

    # Update the canvas with the new image
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Schedule the next update
    root.after(1000, update_frame)  # Update every 1 second (1000 milliseconds)


# Set up the Tkinter GUI
root = tk.Tk()
root.title("Cellular Automata Terrain Generator")

# Create a canvas to display the grid
canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
canvas.pack()

# Start the animation
update_frame()

# Run the Tkinter event loop
root.mainloop()