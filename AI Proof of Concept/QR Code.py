import qrcode
import numpy as np
from collections import deque
from PIL import Image, ImageDraw
import random
import string

# Constants for maze dimensions
QR_CODE_VERSION = 2  # QR code version (1 = 21x21, 2 = 25x25, etc.)
QR_CODE_SIZE = 21 + 4 * (QR_CODE_VERSION - 1)  # Size of the QR code
FINDER_PATTERN_SIZE = 7  # Size of the finder patterns (7x7)

# Directions for movement
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left

# Colors for the image
COLORS = {
    '#': (0, 0, 0),        # Black for walls
    ' ': (255, 255, 255),  # White for paths
    'S': (0, 255, 0),      # Green for start
    'E': (255, 0, 0),      # Red for end
    '.': (0, 0, 255),      # Blue for visited path
}

def generate_random_string(length=10):
    """Generate a random string of letters and numbers."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_qr_code(data, size):
    """Generate a QR code and convert it to a binary grid."""
    qr = qrcode.QRCode(
        version=QR_CODE_VERSION - 1,  # QR code version (0 = version 1, 1 = version 2, etc.)
        box_size=1,  # Size of each box in pixels
        border=0,    # No border
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))  # Resize to desired dimensions
    return np.array(img) == 0  # Convert to binary grid (True = black, False = white)

def interpret_qr_code_as_maze(qr_grid):
    """Convert a QR code grid into a maze representation."""
    maze = []
    for row in qr_grid:
        maze_row = []
        for cell in row:
            maze_row.append('#' if cell else ' ')  # Black = wall, White = path
        maze.append(maze_row)
    return maze

def is_solvable(maze, start, end):
    """Check if the maze is solvable using BFS."""
    queue = deque([start])
    visited = set()
    parent = {}

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            # Reconstruct the path
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return True, path

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                if maze[ny][nx] != '#' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return False, []

def draw_maze(maze, path=None):
    """Draw the maze as an image."""
    cell_size = 20  # Size of each cell in pixels
    img_width = len(maze[0]) * cell_size
    img_height = len(maze) * cell_size
    img = Image.new("RGB", (img_width, img_height), color=COLORS['#'])
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            # Calculate the pixel coordinates
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Fill the cell with the appropriate color
            if path and (x, y) in path:
                color = COLORS['.']
            elif (x, y) == start:
                color = COLORS['S']
            elif (x, y) == end:
                color = COLORS['E']
            else:
                color = COLORS[cell]

            # Draw the cell
            draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=color)

    return img

def get_edge_position(size, margin=1):
    """Get a random position near the edge of the maze."""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        return (random.randint(margin, size - margin - 1), margin)
    elif side == 'bottom':
        return (random.randint(margin, size - margin - 1), size - margin - 1)
    elif side == 'left':
        return (margin, random.randint(margin, size - margin - 1))
    elif side == 'right':
        return (size - margin - 1, random.randint(margin, size - margin - 1))

# Maximum number of attempts to generate a solvable maze
MAX_ATTEMPTS = 10
attempts = 0

# Generate and check mazes until a solvable one is found or max attempts are reached
while attempts < MAX_ATTEMPTS:
    attempts += 1

    # Generate a random string for the QR code data
    data = generate_random_string()
    print(f"Attempt {attempts}: Generating maze with data '{data}'...")

    # Generate a QR code
    qr_grid = generate_qr_code(data, QR_CODE_SIZE)

    # Interpret the QR code as a maze
    maze = interpret_qr_code_as_maze(qr_grid)

    # Set start and end points near the edges
    start = get_edge_position(QR_CODE_SIZE, margin=FINDER_PATTERN_SIZE + 1)
    end = get_edge_position(QR_CODE_SIZE, margin=FINDER_PATTERN_SIZE + 1)

    # Ensure start and end points are not the same
    while end == start:
        end = get_edge_position(QR_CODE_SIZE, margin=FINDER_PATTERN_SIZE + 1)

    # Set start and end points
    maze[start[1]][start[0]] = 'S'  # Start point
    maze[end[1]][end[0]] = 'E'      # End point

    # Check if the maze is solvable
    solvable, path = is_solvable(maze, start, end)

    if solvable:
        print("Maze is solvable! Displaying the maze.")
        # Draw the maze
        img = draw_maze(maze, path)
        img.show()
        img.save("./maze.png")
        break
    else:
        print("Maze is not solvable. Regenerating...")

if attempts >= MAX_ATTEMPTS:
    print(f"Failed to generate a solvable maze after {MAX_ATTEMPTS} attempts.")