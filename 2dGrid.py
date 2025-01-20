import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class CellularAutomaton:
    def __init__(self, grid_size, initial_state=None):
        self.grid_size = grid_size
        self.grid = initial_state if initial_state is not None else np.zeros((grid_size, grid_size), dtype=int)
        self.neighborhood_levels = []
        self.dead_count = np.zeros((grid_size, grid_size), dtype=int)  # Track how many times each cell is dead

    def add_neighborhood(self, size):
        """Add a neighborhood level based on specified size."""
        self.neighborhood_levels.append(size)

    def get_neighborhood(self, x, y, level):
        """Return the neighborhood cells at a specified level for cell (x, y)."""
        size = self.neighborhood_levels[level]
        half_size = size // 2
        neighborhood = self.grid[max(0, x - half_size): min(self.grid_size, x + half_size + 1),
                       max(0, y - half_size): min(self.grid_size, y + half_size + 1)]
        return neighborhood

    def apply_rules(self, cell, neighborhood):
        """Define how a cell's state changes based on its neighborhood."""
        live_neighbors = np.sum(neighborhood) - cell  # Subtract cell itself
        if cell == 1 and (live_neighbors < 2 or live_neighbors > 3):
            return 0  # Cell dies
        elif cell == 0 and live_neighbors == 3:
            return 1  # Cell becomes alive
        return cell  # Otherwise, no change

    def update(self):
        """Apply rules to the entire grid based on neighborhoods."""
        new_grid = self.grid.copy()
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = self.grid[x, y]
                for level in range(len(self.neighborhood_levels)):
                    neighborhood = self.get_neighborhood(x, y, level)
                    new_state = self.apply_rules(cell, neighborhood)
                    new_grid[x, y] = new_state  # Apply the new state
        # Update dead count
        self.dead_count += (self.grid == 0).astype(int)
        self.grid = new_grid

    def display_graphically(self, iteration, mode="state"):
        """Graphically display the grid state or dead count."""
        if mode == "state":
            cmap = LinearSegmentedColormap.from_list('binary', ['white', 'black'])
            data = self.grid
            title = f"Iteration {iteration}"
        elif mode == "dead_count":
            cmap = LinearSegmentedColormap.from_list('grayscale', ['white', 'black'])
            data = self.dead_count
            title = "Dead Cell Count (Darker = More Deaths)"

        plt.figure(figsize=(6, 6))
        plt.imshow(data, cmap=cmap, origin='upper')
        plt.title(title)
        plt.axis('off')
        #plt.colorbar(label='Death Count' if mode == "dead_count" else 'State')
        plt.show()


# Sample usage
grid_size = 10
initial_state = np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.9, 0.1])
ca = CellularAutomaton(grid_size, initial_state=initial_state)
ca.add_neighborhood(3)  # Level 0 (Moore neighborhood)
ca.add_neighborhood(5)  # Level 1

# Run iterations and visualize
iterations = 5
for i in range(iterations):
    print(f"Iteration {i + 1}")
    ca.display_graphically(iteration=i + 1)
    ca.update()

# Display dead cell count visualization
ca.display_graphically(iteration=iterations, mode="dead_count")
