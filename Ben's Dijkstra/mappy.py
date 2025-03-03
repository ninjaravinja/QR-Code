import random


def generate_maze(width, height, removed=10):
    # Initialize the maze with walls (1s)
    maze = [[1 for _ in range(width)] for _ in range(height)]
    # Start carving passages from (1, 1)
    start_x, start_y = 1, 1
    maze[start_x][start_y] = 0
    # Stack to hold the cells to explore
    stack = [(start_x, start_y)]
    # Directions: up, right, down, left
    directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
    while stack:
        x, y = stack[-1]  # Get the current position
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            # Randomly choose a neighbor
            nx, ny = random.choice(neighbors)
            # Remove the wall between the current cell and the chosen neighbor
            maze[(x + nx) // 2][(y + ny) // 2] = 0
            # Mark the chosen neighbor as visited and add it to the stack
            maze[nx][ny] = 0
            stack.append((nx, ny))
        else:
            # If no unvisited neighbors, backtrack by popping from the stack
            stack.pop()
    # Ensure the entrance (0, 1) and exit (height-1, width-2) are open
    maze[0][1] = 0
    maze[height-1][width-2] = 0


    if (height * width // 2) < removed:
        print("removed is bigger")
        removed = (height * width) / 2.22

    print("removed:", removed)
    print("total size:", height * width)
    for i in range(removed):
        x, y = random.randint(0, height-1), random.randint(0, width-1)
        while maze[x][y] != 1:
            x, y = random.randint(0, height-1), random.randint(0, width-1)
        maze[x][y] = 0

    return maze

if __name__ == "__main__":

    width, height, removed = 30, 30, 100
    maze = generate_maze(width, height, removed)

    for row in maze:
        print("".join(str(cell) for cell in row))