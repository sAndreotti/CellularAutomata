from mesa import Model, Agent
from mesa.space import SingleGrid  # Use SingleGrid
from mesa.time import SimultaneousActivation
import random

class Cell(Agent):
    def __init__(self, unique_id, model, state):
        super().__init__(unique_id, model)
        self.state = state  # State can be 0 or 1 (or more complex states)

    def get_nested_neighborhood(self, levels):
        """Get the nested neighborhood for the cell."""
        neighborhood = []
        for level in range(levels):
            # Get neighbors at each level (radius = level + 1)
            neighbors = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=True, radius=level + 1
            )
            neighborhood.append(neighbors)
        return neighborhood

    def step(self):
        nested_neighborhood = self.get_nested_neighborhood(levels=3)
        # Example: Conway's Game of Life rules
        live_neighbors = sum(neighbor.state for neighbor in nested_neighborhood[0])
        if self.state == 1:
            if live_neighbors < 2 or live_neighbors > 3:
                self.state = 0
        else:
            if live_neighbors == 3:
                self.state = 1

class MorphozoicModel(Model):
    def __init__(self, width, height, initial_alive_prob=0.2):
        self.grid = SingleGrid(width, height, torus=True)  # Use SingleGrid
        self.schedule = SimultaneousActivation(self)

        # Create cells
        for x in range(width):
            for y in range(height):
                # Randomly initialize cells as alive (1) or dead (0)
                state = 1 if random.random() < initial_alive_prob else 0
                cell = Cell((x, y), self, state)  # Set initial state
                self.grid.place_agent(cell, (x, y))
                self.schedule.add(cell)

    def step(self):
        self.schedule.step()