import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 960
HEX_SIZE = 80  # Hexagon size
HEX_SPACING = 1.5  # Spacing between hexagons
OFFSET_X = 720
OFFSET_Y = 240

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
wood = (34, 139, 34)
sheep = (117, 210, 43)
brick = (179, 89, 0)
wheat = (210, 194, 43)
ore = (19, 19, 18)
desert = (228, 197, 132)

# Resources
hex_counts = [
    ("wood", 4),
    ("sheep", 4),
    ("brick", 4),
    ("wheat", 3),
    ("ore", 3),
    ("desert", 1)
]

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal Grid")

def hexagon_points(center, size):
    angle = 360 / 6  # Angle between each vertex of the hexagon
    points = []
    for i in range(6):
        x = center[0] + size * math.sin(math.radians(i * angle))
        y = center[1] + size * math.cos(math.radians(i * angle))
        points.append((x, y))

    return points

# Define hexagon drawing function
def draw_hexagon(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center[0] + size * math.sin(angle_rad)
        y = center[1] + size * math.cos(angle_rad)
        points.append((x, y))
    pygame.draw.polygon(screen, black, points, 2)

# Function to calculate hexagon centers based on grid pattern
def calculate_hex_centers():
    hex_centers = []
    row_lengths = [3, 4, 5, 4, 3]

    for row, row_length in enumerate(row_lengths):
        y = row * (HEX_SIZE * 1.5) + OFFSET_Y
        x_start = OFFSET_X - (row_length - 1) * (HEX_SIZE * math.sqrt(3) + HEX_SPACING) / 2

        for col in range(row_length):
            x = x_start + col * (HEX_SIZE * math.sqrt(3) + HEX_SPACING)
            hex_centers.append((x, y))

    return hex_centers

def assign_resource(hex_centers, hex_counts, max_resource_count):
    resource_list = list(hex_counts.keys())
    random.shuffle(resource_list)

    hex_mapping = {}
    resource_count = {resource: 0 for resource in hex_counts}

    for center in hex_centers:
        if not resource_list:
            resource_list = list(hex_counts.keys())
            random.shuffle(resource_list)

        resource = resource_list.pop()
        if resource_count[resource] < max_resource_count:
            hex_mapping[center] = (resource, hex_counts[resource])
            resource_count[resource] += 1
    
    return hex_mapping

# Main loop
running = True
hex_centers = calculate_hex_centers()
hex_mapping = assign_resource(hex_centers, hex_counts, 4)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    for center in hex_centers:
        resource, color = hex_mapping.get(center, ("", (255, 255, 255)))
        pygame.draw.polygon(screen, color, hexagon_points(center, HEX_SIZE), 0)
        draw_hexagon(center, HEX_SIZE)

    pygame.display.flip()

pygame.quit()


