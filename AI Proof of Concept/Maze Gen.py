import random
from collections import deque
from PIL import Image, ImageDraw

# Constants for maze dimensions
WIDTH, HEIGHT = 177, 177 # Maze dimensions (will be adjusted to odd if even)

# Ensure WIDTH and HEIGHT are odd
if WIDTH % 2 == 0:
    WIDTH += 1
if HEIGHT % 2 == 0:
    HEIGHT += 1

# Directions for movement
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left

# Maze symbols
WALL = '#'
PATH = ' '
START = 'S'
END = 'E'
VISITED = '.'

# Colors for the image
COLORS = {
    WALL: (0, 0, 0),        # Black for walls
    PATH: (255, 255, 255),  # White for paths
    START: (0, 255, 0),     # Green for start
    END: (255, 0, 0),       # Red for end
    VISITED: (0, 0, 255),   # Blue for visited path
}

# Calculate cell size dynamically based on maze size
def calculate_cell_size(width, height):
    # Smaller mazes have larger cells, larger mazes have smaller cells
    # You can adjust the scaling factor as needed
    scaling_factor = 500  # Higher values make cells larger for smaller mazes
    return max(1, scaling_factor // max(width, height))

CELL_SIZE = calculate_cell_size(WIDTH, HEIGHT)

def generate_maze(width, height):
    # Initialize the maze with walls
    maze = [[WALL for _ in range(width)] for _ in range(height)]

    # Start point (top-left corner)
    start = (1, 1)
    maze[start[1]][start[0]] = START

    # End point (bottom-right corner)
    end = (width - 2, height - 2)
    maze[end[1]][end[0]] = END

    # List of frontier cells
    frontiers = []
    frontiers.append((start[0], start[1]))

    while frontiers:
        # Choose a random frontier cell
        x, y = random.choice(frontiers)
        frontiers.remove((x, y))

        # Check neighbors to carve a path
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == WALL:
                # Carve a path
                maze[ny][nx] = PATH
                maze[(y + ny) // 2][(x + nx) // 2] = PATH
                # Add the new cell to frontiers
                frontiers.append((nx, ny))

    # Ensure the end point is accessible
    # Check if any of the end's neighbors are paths
    end_x, end_y = end
    for dx, dy in DIRECTIONS:
        nx, ny = end_x + dx, end_y + dy
        if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == PATH:
            break
    else:
        # If no path is found, carve a path to the end
        # Choose a random direction to carve a path
        dx, dy = random.choice(DIRECTIONS)
        nx, ny = end_x + dx, end_y + dy
        if 0 <= nx < width and 0 <= ny < height:
            maze[ny][nx] = PATH

    # Ensure the start and end points are preserved
    maze[start[1]][start[0]] = START
    maze[end[1]][end[0]] = END

    return maze, start, end

def is_solvable(maze, start, end):
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
                if maze[ny][nx] != WALL and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return False, []

def draw_maze(maze, path=None):
    # Create a blank image
    img_width = len(maze[0]) * CELL_SIZE
    img_height = len(maze) * CELL_SIZE
    img = Image.new("RGB", (img_width, img_height), color=COLORS[WALL])
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            # Calculate the pixel coordinates
            x1 = x * CELL_SIZE
            y1 = y * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            # Fill the cell with the appropriate color
            if path and (x, y) in path:
                color = COLORS[VISITED]
            elif cell == START:
                color = COLORS[START]
            elif cell == END:
                color = COLORS[END]
            elif cell == PATH:
                color = COLORS[PATH]
            else:
                color = COLORS[WALL]

            # Draw the cell
            draw.rectangle([x1, y1, x2 - 1, y2 - 1], fill=color)

    return img

# Maximum number of attempts to generate a solvable maze
MAX_ATTEMPTS = 10
attempts = 0

# Generate and check mazes until a solvable one is found or max attempts are reached
while attempts < MAX_ATTEMPTS:
    attempts += 1
    maze, start, end = generate_maze(WIDTH, HEIGHT)
    solvable, path = is_solvable(maze, start, end)
    if solvable:
        print(f"Maze is solvable! Displaying the maze (Attempt {attempts}).")
        # Draw the maze
        img = draw_maze(maze, path)
        img.show()
        break
    else:
        print(f"Maze is not solvable. Attempt {attempts} of {MAX_ATTEMPTS}.")

if attempts >= MAX_ATTEMPTS:
    print(f"Failed to generate a solvable maze after {MAX_ATTEMPTS} attempts.")


