import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constraints 
WIDTH, HEIGHT = 1440, 960
HEX_SIZE = 80  # Hexagon size
HEX_SPACING = 1.5  # Spacing between hexagons
OFFSET_X = 720 # Centering the board in the Pygame window
OFFSET_Y = 240
BOARDER_CENTER = (WIDTH // 2, HEIGHT // 2)
BOARDER_SIZE = min(WIDTH, HEIGHT) * 0.5  # Adjust the size of the Boarder, its just one large blue hexagon

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (79, 166, 235)
TAN = (225, 200, 125)

# Resources and their color codes
resource_colors = {
    "wood": (34, 139, 34),
    "sheep": (117, 210, 43),
    "brick": (179, 89, 0),
    "wheat": (210, 194, 43),
    "ore": (59, 59, 58),
    "desert": (228, 197, 132)
}

# Color list for random ports
color_list = [WHITE, resource_colors["wheat"], resource_colors["ore"], WHITE, resource_colors["sheep"], WHITE, WHITE, resource_colors["brick"], resource_colors["wood"]]

# User input function to generate a game based on specific likings on a Catan Board 
user_input = input("Would you like to play with standard or random Harbours? \n")

# Create a Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Base Catan: 3-4 Players with Ports")

# This function generates the Hexagon that represents the boarder where the ports are located 
def hex_boarder(center, size):
    angle = 360 / 6
    boarder_points = []
    for i in range(6):
        x = center[0] + size * math.cos(math.radians(i * angle))
        y = center[1] + size * math.sin(math.radians(i * angle))
        boarder_points.append((x, y))

    return boarder_points

# The lines that are generated here are section off the boarder to make it look like 6 different frames pieces. Truthfully just for aesthetics
def connection_lines():

    bc_points = [[[510, 197], [420, 143]],
                 [[860, 50], [860, 200]],
                 [[1069, 440], [1169, 382]],
                 [[930, 760], [1025, 815]],
                 [[578.5, 800], [578.5, 900]],
                 [[370, 520], [231, 600]]]
    
    while bc_points:
        line = bc_points.pop()
        pygame.draw.line(screen, BLACK, line[0], line[1], 2)

# Generates the smaller hexes that will become the resource tiles.
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
    row_lengths = [3, 4, 5, 4, 3]

    for row, row_length in enumerate(row_lengths):
        y = row * (HEX_SIZE * 1.5) + OFFSET_Y
        x_start = OFFSET_X - (row_length - 1) * (HEX_SIZE * math.sqrt(3) + HEX_SPACING) / 2

        for col in range(row_length):
            x = x_start + col * (HEX_SIZE * math.sqrt(3) + HEX_SPACING)
            hex_centers.append((x, y))

    return hex_centers 

# This function stores tuples that give have a resource type and number attached. The 0 and "" represent and empty tuple.
def generate_board():

    board = [[(0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, "")], 
            [(0, ""), (0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, ""), (0, "")],
            [(0, ""), (0, ""), (0, "")]]
    
    return board

# Makes sure 'board' does not store the number 6 or 8 next to eachother. (Catan Specific rule)
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

# This function pulls from our resource and number lists to fill each tuple in board
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
                row[i] = (row[i], "desert", resource_colors["desert"]) # The number '1' in the board tuple must only ever get assigned the desert
            else:
                resource = resource_list[index]
                row[i] = (row[i], resource, resource_colors[resource])
                index += 1


    return True

# Assigns the resource from board to the hexagons generated by hexagon points, adds the color and the number tokens as well.
def assign_resources(hex_centers, board):

    for lst in board:
        while lst:
            center = hex_centers.pop()
            number, resource, color = lst.pop()  

            if resource == "desert":
                pygame.draw.polygon(screen, color, hexagon_points(center, HEX_SIZE), 0) # The desert will not get a number token.
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

# Simple Function to add triangles with different colors to represent the trading ports.
def create_ports(user_input):

    points = [[[510, 192], [510, 122], [572, 157]],
              [[789, 194], [789, 122], [725, 157]],
              [[935, 278], [999, 315], [999, 240]],
              [[1075, 518], [1075, 442], [1140, 480]],
              [[935, 682], [999, 645], [999, 720]],
              [[789, 767], [789, 838], [725, 804]],
              [[510, 768], [510, 838], [572, 804]],
              [[435, 563], [435, 638], [370, 600]],
              [[435, 397], [435, 322], [370, 360]]]
    
    while points:
        if user_input == "random":
            random.shuffle(color_list)   # If user input is "random," Then shuffle the color list for the ports. (In line 34) 
            port = points.pop()
            color = color_list.pop()  
        elif user_input == "standard":                
            port = points.pop()          # If user input is "standard," Then it will put the port colors in order of the list, which will match
            color = color_list.pop()     # the way the 5th edition board has them laid out. 
        pygame.draw.polygon(screen, color, port)
        pygame.draw.polygon(screen, BLACK, port, 2)

def print_board(board):
    for row in board:
        print(row)

# Basic Pygame visuals
def visualize_board():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()

def main():
    
    numbers = [1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

    resource_list = ["wood", "wood", "wood", "wood",
                     "sheep", "sheep", "sheep", "sheep",
                     "brick", "brick", "brick",
                     "wheat", "wheat", "wheat", "wheat",
                     "ore", "ore", "ore"
                    ]
    
    board = generate_board()

    while not fill_board(board, numbers.copy(), resource_list.copy()):
        board = generate_board()  # Reset the board if board breaks the rules of check_constraints.

    pygame.draw.polygon(screen, BLUE, hex_boarder(BOARDER_CENTER, BOARDER_SIZE), 0)
    connection_lines()
    #print_board(board) # Uncomment if you want to see the printed statements from generate board.

    hex_centers = calculate_hex_centers()
    assign_resources(hex_centers, board)
    create_ports(user_input)

    visualize_board()

if __name__ == "__main__":
    main()
