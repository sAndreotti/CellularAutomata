import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class CellularAutomaton:
    def __init__(self, grid_size, initial_state=None):
        self.grid_size = grid_size
        self.grid = initial_state if initial_state is not None else np.zeros((grid_size, grid_size), dtype=float)
        self.dead_count = np.zeros((grid_size, grid_size), dtype=int)
        self.previous_states = []  # For historical transitions

    def get_neighborhood(self, x, y, size):
        """Return the neighborhood cells for a given size."""
        half_size = size // 2
        return self.grid[max(0, x - half_size): min(self.grid_size, x + half_size + 1),
                         max(0, y - half_size): min(self.grid_size, y + half_size + 1)]

    def apply_conway_rules(self, cell, neighborhood):
        """Conway's Game of Life rules."""
        live_neighbors = np.sum(neighborhood) - cell
        if cell == 1 and (live_neighbors < 2 or live_neighbors > 3):
            return 0  # Cell dies
        elif cell == 0 and live_neighbors == 3:
            return 1  # Cell becomes alive
        return cell  # Otherwise, no change

    def apply_probabilistic_rules(self, cell, neighborhood, prob=0.1):
        """Probabilistic transitions."""
        if np.random.rand() < prob:
            return 1 - cell  # Flip state with given probability
        return cell

    def apply_continuous_rules(self, cell, neighborhood):
        """Continuous state transitions based on average."""
        avg_state = np.mean(neighborhood)
        return avg_state  # Smooth transition to average value

    def apply_historical_rules(self, cell, x, y, history_weight=0.2):
        """Historical transitions using memory of past states."""
        if len(self.previous_states) == 0:
            return cell  # No history yet
        past_average = np.mean([state[x, y] for state in self.previous_states])
        return cell * (1 - history_weight) + past_average * history_weight

    def update(self, rule_type="conway", **kwargs):
        """Update the grid synchronously based on a specific rule type."""
        new_grid = self.grid.copy()  # Next state of the grid
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                cell = self.grid[x, y]
                neighborhood = self.get_neighborhood(x, y, size=3)  # Example size
                if rule_type == "conway":
                    new_grid[x, y] = self.apply_conway_rules(cell, neighborhood)
                elif rule_type == "probabilistic":
                    new_grid[x, y] = self.apply_probabilistic_rules(cell, neighborhood)
                elif rule_type == "continuous":
                    new_grid[x, y] = self.apply_continuous_rules(cell, neighborhood)
                elif rule_type == "historical":
                    new_grid[x, y] = self.apply_historical_rules(cell, x, y)
        # Update historical states
        if rule_type == "historical":
            self.previous_states.append(self.grid.copy())
            if len(self.previous_states) > 5:  # Keep limited history
                self.previous_states.pop(0)
        # Update the main grid
        self.grid = new_grid
        # Update dead count
        self.dead_count += (self.grid == 0).astype(int)

    def display_grid(self, title="Cellular Automaton Grid"):
        """Display the grid."""
        plt.imshow(self.grid, cmap='viridis', origin='upper')
        plt.title(title)
        plt.colorbar()
        plt.axis('off')
        plt.show()

    def display_3d_bars(self):
        """Display the dead cell count as a 3D bar plot."""
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        x = np.arange(self.grid_size)
        y = np.arange(self.grid_size)
        x, y = np.meshgrid(x, y)  # Create grid for positions
        x = x.flatten()
        y = y.flatten()
        z = np.zeros_like(x)  # Start height of the bars is 0
        dx = dy = 1  # Width and depth of the bars
        dz = self.dead_count.flatten()  # Heights based on dead count

        ax.bar3d(x, y, z, dx, dy, dz, shade=True, color='gray', edgecolor='black')

        ax.set_xlabel('X (Cell Position)')
        ax.set_ylabel('Y (Cell Position)')
        ax.set_zlabel('Death Count')
        ax.set_title('Dead Cell Count (3D Visualization)')

        plt.show()


# Sample usage
grid_size = 10
initial_state = np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.7, 0.3])
ca = CellularAutomaton(grid_size, initial_state)

# Test different rules with synchronous updates
rules = ["conway", "probabilistic", "continuous", "historical"]
rule = "historical"
print(f"Applying {rule} rules...")
for i in range(5):  # Run for 5 iterations
    ca.update(rule_type=rule, prob=0.5, history_weight=0.3)
    ca.display_grid(title=f"Rule: {rule}, Iteration {i + 1}")

# Display 3D bar plot of dead cell count
ca.display_3d_bars()
