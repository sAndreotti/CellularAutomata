from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agent import MorphozoicModel

def cell_portrayal(cell):
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    if cell.state == 1:
        portrayal["Color"] = "black"
    else:
        portrayal["Color"] = "white"
    return portrayal

# Define the grid visualization
grid = CanvasGrid(cell_portrayal, 50, 50, 500, 500)

# Define the model parameters as a dictionary
model_params = {
    "width": 50,  # Width of the grid
    "height": 50,  # Height of the grid
    "initial_alive_prob": 0.2  # Probability of a cell starting as alive
}

# Create the server
server = ModularServer(
    MorphozoicModel,  # The model class
    [grid],           # Visualization elements (in this case, just the grid)
    "Morphozoic Model",  # Title of the visualization
    model_params      # Model parameters as a dictionary
)

# Launch the server
server.launch()