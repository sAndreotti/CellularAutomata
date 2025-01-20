import numpy as np
import tkinter as tk
from scipy.ndimage import generic_filter


class MorphozoicCA:
    def __init__(self, grid_size, neighborhood_size=3, n_states=2):
        self.grid_size = grid_size
        self.grid = np.random.randint(0, n_states, (grid_size, grid_size))
        self.neighborhood_size = neighborhood_size
        self.n_states = n_states
        self.rules = {}  # Map morphogens to actions

    def initialize_rules(self, rules):
        """
        Define metamorphs as mappings from morphogens to cell actions.
        :param rules: dict with morphogen (tuple) as keys and new states as values.
        """
        self.rules = rules

    def get_morphogen(self, neighborhood):
        """
        Calculate a morphogen for a neighborhood.
        Represent it as a histogram of state densities.
        """
        hist = np.zeros(self.n_states)
        for state in range(self.n_states):
            hist[state] = np.sum(neighborhood == state)
        return tuple(hist)

    def apply_rules(self, neighborhood):
        """
        Determine the new state based on the rules.
        :param neighborhood: Flattened 1D array of the neighborhood.
        """
        # Reshape the flattened array into a 2D neighborhood
        size = self.neighborhood_size
        neighborhood = neighborhood.reshape((size, size))
        morphogen = self.get_morphogen(neighborhood)
        # Default to the current cell state if no rule matches
        center_cell = neighborhood[size // 2, size // 2]
        return self.rules.get(morphogen, center_cell)

    def calculate_next_state(self):
        """
        Calculate the next state for each cell without modifying the current grid.
        """
        size = self.neighborhood_size
        next_grid = generic_filter(
            self.grid,
            self.apply_rules,
            size=(size, size),
            mode='wrap'
        )
        return next_grid

    def step(self):
        """
        Perform one synchronized update step.
        """
        self.grid = self.calculate_next_state()


class MorphozoicGUI:
    def __init__(self, root, ca, cell_size=20, delay=1000):
        """
        Initialize the GUI for the Morphozoic Cellular Automaton.
        :param root: Tkinter root window.
        :param ca: Morphozoic Cellular Automaton instance.
        :param cell_size: Size of each cell in the grid.
        :param delay: Delay (in ms) between transitions.
        """
        self.root = root
        self.ca = ca
        self.cell_size = cell_size
        self.delay = delay
        self.running = False
        self.iteration = 0  # Track the current iteration

        # Configure canvas size based on the grid
        self.canvas = tk.Canvas(
            root,
            width=ca.grid_size * cell_size,
            height=ca.grid_size * cell_size,
            bg="white"
        )
        self.canvas.pack()

        # Control frame for buttons and iteration counter
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        # Start button
        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Iteration counter
        self.iteration_label = tk.Label(self.control_frame, text=f"Iteration: {self.iteration}")
        self.iteration_label.pack(side=tk.LEFT, padx=10)

        # Stop button
        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Draw the initial grid
        self.draw_grid()

    def draw_grid(self):
        """
        Draw the grid on the canvas.
        """
        self.canvas.delete("all")  # Clear previous grid
        for i in range(self.ca.grid_size):
            for j in range(self.ca.grid_size):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size

                # Use colors to represent cell states
                state = self.ca.grid[i, j]
                color = "black" if state == 1 else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def update(self):
        """
        Update the grid, redraw it, and update the iteration counter.
        """
        if self.running:
            self.ca.step()  # Update the automaton state
            self.iteration += 1  # Increment the iteration counter
            self.iteration_label.config(text=f"Iteration: {self.iteration}")  # Update the label
            self.draw_grid()  # Redraw the grid
            self.root.after(self.delay, self.update)  # Schedule the next update

    def start(self):
        """
        Start the automaton.
        """
        if not self.running:
            self.running = True
            self.update()

    def stop(self):
        """
        Stop the automaton.
        """
        self.running = False


# Main Program
if __name__ == "__main__":
    grid_size = 40
    ca = MorphozoicCA(grid_size, neighborhood_size=3, n_states=2)

    # Example rule: cells surrounded by a majority of state 1 become state 1
    example_rules = {
        (8, 1): 1,  # Example morphogen to state mapping
        (4, 5): 0  # Default is to stay unchanged
    }
    ca.initialize_rules(example_rules)

    # Create the GUI
    root = tk.Tk()
    root.title("Morphozoic Cellular Automaton")
    gui = MorphozoicGUI(root, ca)

    # Run the Tkinter event loop
    root.mainloop()
