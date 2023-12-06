import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1440, 960
HEX_SIZE = 70  # Hexagon size
HEX_SPACING = 1.5  # Spacing between hexagons
OFFSET_X = 720
OFFSET_Y = 160

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (20, 80, 250)
TAN = (225, 200, 125)

# Resources and their color codes
resource_colors = {
    "wood": (34, 139, 34),
    "sheep": (117, 210, 43),
    "brick": (179, 89, 0),
    "wheat": (210, 194, 43),
    "ore": (19, 19, 18),
    "desert": (228, 197, 132),
    "sea": (20, 80, 250)
}

# Resources and their desired counts
resource_counts = {
    "wood": 6,
    "sheep": 6,
    "brick": 5,
    "wheat": 6,
    "ore": 5,
    "desert": 2,
    "sea": 0
}

# Numbers for token generation
number_list = [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12]

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
    points = hexagon_points(center, size)
    pygame.draw.polygon(screen, WHITE, points, 2)

# Function to calculate hexagon centers based on grid pattern
def calculate_hex_centers():
    hex_centers = []
    row_lengths = [3, 4, 5, 6, 5, 4, 3]

    for row, row_length in enumerate(row_lengths):
        y = row * (HEX_SIZE * 1.5) + OFFSET_Y
        x_start = OFFSET_X - (row_length - 1) * (HEX_SIZE * math.sqrt(3) + HEX_SPACING) / 2

        for col in range(row_length):
            x = x_start + col * (HEX_SIZE * math.sqrt(3) + HEX_SPACING)
            hex_centers.append((x, y))

    return hex_centers

# Calculating the distance between two hex centers
def distance(hex1, hex2):
    x1, y1 = hex1 
    x2, y2 = hex2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Creating and randomizing the hexagons. The function will randomly assign each hex center a resource from resource_counts
def assign_resources(hex_centers, resource_counts):
    
    random.shuffle(number_list)
    hex_mapping = []
    
    for resource, count in resource_counts.items():
        for _ in range(count):
            if resource == "desert":
                hex_mapping.append((resource, _, resource_colors[resource]))
            else:
                number = number_list.pop()
                hex_mapping.append((resource, number, resource_colors[resource]))

    random.shuffle(hex_mapping)

    for center in hex_centers:
        resource, number, color = hex_mapping.pop()

        if resource == "desert" or resource == "sea":
            pygame.draw.polygon(screen, color, hexagon_points(center, HEX_SIZE), 0) 
        else:
            pygame.draw.polygon(screen, color, hexagon_points(center, HEX_SIZE), 0)
            pygame.draw.circle(screen, TAN, center, 20, 0)
            font = pygame.font.Font(None, 36)
            if number == 6 or number == 8:
                text = font.render(str(number), True, (200, 0, 0))
            else:
                text = font.render(str(number), True, (0, 0, 0))
            text_rect = text.get_rect(center=center)
            screen.blit(text, text_rect)
    
        draw_hexagon(center, HEX_SIZE)

    return hex_mapping


# Main loop
running = True
hex_centers = calculate_hex_centers()
hex_mapping = assign_resources(hex_centers, resource_counts)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
