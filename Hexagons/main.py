import pygame
import math
import random

# Hexagon settings
HEX_SIZE = 40  # Radius of the hexagon
WIDTH, HEIGHT = 1000, 800

# Colors for terrain types
TERRAIN_COLORS = {
    "desert": (255, 255, 153),  # Light yellow
    "hills": (204, 102, 0),     # Brown (brick)
    "forest": (0, 102, 0),      # Dark green (wood)
    "pasture": (153, 255, 153), # Light green (sheep)
    "fields": (255, 255, 0),    # Yellow (wheat)
    "mountains": (128, 128, 128), # Gray (ore)
}

# Resources corresponding to terrain types
TERRAIN_RESOURCES = {
    "hills": "brick",
    "forest": "wood",
    "pasture": "sheep",
    "fields": "wheat",
    "mountains": "ore",
    "desert": None,  # Desert produces no resources
}

# Numbers and their probabilities (2–12, excluding 7)
NUMBERS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]

def hex_to_pixel(q, r, size):
    """Convert axial coordinates (q, r) to pixel coordinates."""
    x = size * (3/2 * q)
    y = size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return (x + WIDTH // 2, y + HEIGHT // 2)  # Center the grid

def draw_hexagon(surface, q, r, size, terrain, number=None):
    """Draw a hexagon at axial coordinates (q, r) with a given terrain and number."""
    x, y = hex_to_pixel(q, r, size)
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        px = x + size * math.cos(angle_rad)
        py = y + size * math.sin(angle_rad)
        points.append((px, py))
    # Draw the filled hexagon
    pygame.draw.polygon(surface, TERRAIN_COLORS[terrain], points)
    # Draw the black border
    pygame.draw.polygon(surface, (0, 0, 0), points, 2)
    if number:
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(str(number), True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

def get_vertices(q, r, size):
    """Return the pixel coordinates of the 6 vertices of a hexagon."""
    x, y = hex_to_pixel(q, r, size)
    vertices = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        px = x + size * math.cos(angle_rad)
        py = y + size * math.sin(angle_rad)
        vertices.append((px, py))
    return vertices

def create_catan_grid():
    """Create a Catan-style hexagonal grid with terrain types and numbers."""
    # Define the axial coordinates for a Catan map (19 hexagons)
    grid = [
        (0, 0), (1, 0), (2, 0),
        (-1, 1), (0, 1), (1, 1), (2, 1),
        (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
        (-2, 3), (-1, 3), (0, 3), (1, 3),
        (-2, 4), (-1, 4), (0, 4)
    ]

    # Assign terrain types
    terrains = list(TERRAIN_COLORS.keys())
    terrain_counts = {
        "desert": 1,
        "hills": 3,
        "forest": 4,
        "pasture": 4,
        "fields": 4,
        "mountains": 3
    }
    terrain_list = []
    for terrain, count in terrain_counts.items():
        terrain_list.extend([terrain] * count)
    random.shuffle(terrain_list)

    # Assign numbers
    numbers = NUMBERS.copy()
    random.shuffle(numbers)

    # Create the grid with terrain and numbers
    catan_grid = {}
    desert_index = terrain_list.index("desert")
    for i, (q, r) in enumerate(grid):
        terrain = terrain_list[i]
        if terrain == "desert":
            catan_grid[(q, r)] = (terrain, None)  # Desert has no number
        else:
            catan_grid[(q, r)] = (terrain, numbers.pop(0))
    return catan_grid

def get_hexagons_for_vertex(vertex, grid):
    """Return the 3 hexagons that share a given vertex."""
    q, r = vertex
    # This is a simplified approach; you may need to adjust based on your grid layout
    adjacent = [
        (q, r),
        (q + 1, r),
        (q, r + 1),
    ]
    return [hexagon for hexagon in adjacent if hexagon in grid]

def draw_resource_info(surface, number, resources):
    """Draw the current number and agent's resources on the screen."""
    font = pygame.font.SysFont("Arial", 24)
    # Draw the current number
    number_text = font.render(f"Number: {number}", True, (0, 0, 0))
    surface.blit(number_text, (10, 10))
    # Draw the resources
    y_offset = 40
    for resource, count in resources.items():
        resource_text = font.render(f"{resource}: {count}", True, (0, 0, 0))
        surface.blit(resource_text, (10, y_offset))
        y_offset += 30

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Create a Catan-style grid
    catan_grid = create_catan_grid()

    # Initialize the agent's colony at a random vertex
    vertices = set()
    for (q, r) in catan_grid.keys():
        hex_vertices = get_vertices(q, r, HEX_SIZE)
        for vertex in hex_vertices:
            vertices.add(vertex)
    colony_position = random.choice(list(vertices))

    # Track the agent's resources
    resources = {
        "brick": 0,
        "wood": 0,
        "sheep": 0,
        "wheat": 0,
        "ore": 0,
    }

    # Initialize the current number
    current_number = None

    running = True
    tick_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate resource collection every 30 ticks
        tick_count += 1
        if tick_count >= 30:
            # Draw a random number between 2 and 12
            current_number = random.randint(2, 12)
            if current_number == 7:  # Skip 7 (no resource production on 7)
                current_number = random.randint(2, 12)
            # Check all hexagons adjacent to the colony's vertex
            hexagons = get_hexagons_for_vertex(colony_position, catan_grid)
            for (q, r) in hexagons:
                terrain, hex_number = catan_grid[(q, r)]
                if hex_number == current_number and terrain != "desert":
                    resource = TERRAIN_RESOURCES[terrain]
                    resources[resource] += 1
            tick_count = 0

        # Draw the grid
        screen.fill((255, 255, 255))  # Clear screen
        for (q, r), (terrain, number) in catan_grid.items():
            draw_hexagon(screen, q, r, HEX_SIZE, terrain, number)
        # Draw the colony
        pygame.draw.circle(screen, (255, 0, 0), colony_position, 5)
        # Draw the current number and resources
        draw_resource_info(screen, current_number, resources)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()