# Constants

# Map parameters
w, h = 50, 50  # Number of cells
GRID_WIDTH, GRID_HEIGHT = 600, 600  # Size of the grid area
INITIAL_PROB = 0.45  # Initial probability to spawn a wall
DEPTH = False  # Show the previous map, emulating depth

# Iteraction parameters
RULE = 1
UPDATE_MODE = "LINEAR"  # LINEAR = sequential update, RANDOM = Randomly update all cells

# Object Parameters
# RADIUS = 7
RADIUS = int(w / 10)  # Radius for chest to spawn
CHEST_PROB = 0.1  # Probability for chest to spawn
BAG_PROB = 0.45  # Probability for bags to spawn

# Monsters Parameters
MAX_MONSTERS = 3
MONSTER_RADIUS = 3  # Radius for monster to spawn
MONSTER_PROB = 0.2  # Probability to spawn a monster near chests

# Window sizes
BUTTON_WIDTH, BUTTON_HEIGHT = 160, 40  # Size of the button
WINDOW_WIDTH = GRID_WIDTH + BUTTON_WIDTH + 20  # Total window width (grid + button + padding)
WINDOW_HEIGHT = GRID_HEIGHT  # Window height
TILE_SIZE = GRID_WIDTH // w  # Size of a Tile

# Tiles Textures
GROUND_BONES = 109
GROUND_STONE = 107
GROUND = 45
VOID = 30
ISOLATED = 11

# U = Up, D = Down, L = Left, R = Right
# One wall connected Up
CON_U = 24
CON_U2 = 49
CON_U3 = 65
CON_U4 = 101

# One wall connected Down
CON_D = 13
CON_D2 = 9
CON_D3 = 79
CON_D4 = 80
CON_D5 = 81

# One wall connected Left
CON_L = 28
CON_L2 = 53
CON_L3 = 75
CON_L4 = 89
CON_L5 = 93
CON_L6 = 99

# One wall connected Right
CON_R = 26
CON_R2 = 51
CON_R3 = 86
CON_R4 = 91
CON_R5 = 97

# Two walls connected
# Two walls connected Left Right
CON_LR = 4
CON_LR2 = 5
CON_LR3 = 6
CON_LR4 = 59
CON_LR5 = 59
CON_LR6 = 60
CON_LR7 = 77
CON_LR8 = 98

# Two walls connected Up Down
CON_UD = 19
CON_UD2 = 23
CON_UD3 = 33
CON_UD4 = 37
CON_UD5 = 44
CON_UD6 = 48

# Two walls corner
CON_UR = 57
CON_UL = 61
CON_DR = 3
CON_DL = 7

# Three walls connected
CON_LUR = 27
CON_LDR = 52
CON_LUD = 87
CON_URD = 88

# Four walls connected
CON_LURD = 92

# Texture variants
U_LIST = [CON_U, CON_U2, CON_U3, CON_U4]
D_LIST = [CON_D, CON_D2, CON_D3, CON_D4, CON_D5]
R_LIST = [CON_R, CON_R2, CON_R3, CON_R4, CON_R5]
L_LIST = [CON_L, CON_L2, CON_L3, CON_L4, CON_L5, CON_L6]

LR_LIST = [CON_LR, CON_LR2, CON_LR3, CON_LR4, CON_LR5, CON_LR6, CON_LR7, CON_LR8]
UD_LIST = [CON_UD, CON_UD2, CON_UD3, CON_UD4, CON_UD5, CON_UD6]
