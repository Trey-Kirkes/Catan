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
OFFSET_Y = 125

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
    "ore": (59, 59, 58),
    "desert": (228, 197, 132),
    "sea": (20, 80, 250)
}

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

def generate_board():
    board = [[(0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, "")], 
            [(0, ""), (0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, "")]]
    return board

def check_constraints(board, x, y, value):
    # Check if the value conflicts with the constraints in the same row
    if 6 in board[y] or 8 in board[y]:
        if value == 6 or value == 8:
            # Check if the previous position in the row contains 6 or 8
            if x > 0 and (board[y][x - 1] == 6 or board[y][x - 1] == 8):
                return False

    # Check if the value conflicts with the constraints in the previous row
    if y > 0:
        prev_row = board[y - 1]
        if x > 0 and (x - 1) < len(prev_row) and (prev_row[x - 1] == 6 or prev_row[x - 1] == 8):
            if value == 6 or value == 8:
                return False
        if x < len(prev_row) and (prev_row[x] == 6 or prev_row[x] == 8):
            if value == 6 or value == 8:
                return False
        if x < len(prev_row) - 1 and (x + 1) < len(prev_row) and (prev_row[x + 1] == 6 or prev_row[x + 1] == 8):
            if value == 6 or value == 8:
                return False

    return True

def fill_board(board, numbers, resource_list):
    for y in range(len(board)):
        for x in range(len(board[y])):
            valid_numbers = [num for num in numbers if check_constraints(board, x, y, num)]
            if not valid_numbers:
                return False  # No valid number for this cell
            board[y][x] = random.choice(valid_numbers)
            numbers.remove(board[y][x])
    
    random.shuffle(resource_list)
    index = 0
    for row in board:
        for i in range(len(row)):
            if row[i] == 1:
                row[i] = (row[i], "desert", resource_colors["desert"])
            else:
                resource = resource_list[index]
                row[i] = (row[i], resource, resource_colors[resource])
                index += 1


    return True

def assign_resources(hex_centers, board):

    for lst in board:
        while lst:
            center = hex_centers.pop()
            number, resource, color = lst.pop()  

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

    return board


def print_board(board):
    for row in board:
        print(row)

def visualize_board():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()

def main():
    
    numbers = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12]

    resource_list = ["wood", "wood", "wood", "wood", "wood", "wood",
                     "sheep", "sheep", "sheep", "sheep", "sheep", "sheep",
                     "brick", "brick", "brick", "brick", "brick",
                     "wheat", "wheat", "wheat", "wheat", "wheat", "wheat",
                     "ore", "ore", "ore", "ore", "ore"
                    ]
    
    board = generate_board()

    while not fill_board(board, numbers.copy(), resource_list.copy()):
        board = generate_board()  # Reset the board

    print("Successfully filled the board:")
    print_board(board)

    hex_centers = calculate_hex_centers()
    assign_resources(hex_centers, board)

    visualize_board()

if __name__ == "__main__":
    main()

