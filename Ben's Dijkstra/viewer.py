import pygame  # for displaying the map + interactions
import time
import mappy  # generates the map
import sys
import multiprocessing

from pygame.examples.scrap_clipboard import screen

#from pygame.examples.sprite_texture import clock



"""
Hello,
This is my first pygame program.
it will use dijkstra's algorithm(not coded by me) to find the shortest path between the two points
that are selected by right and left clicking the map on a empty tile.
it will also use a random maze generator(not coded by me) to generate the map. iv changed this to
remove a customisable amount of walls from the map because its just cooler


"""
class Shared_Info:
    def __init__(self, screen_obj, clock, steps_flag, rainbow_flag):
        self.current_screen = screen_obj
        self.clock = clock
        self.steps_flag = steps_flag
        self.rainbow_flag = rainbow_flag


class Stats:
    def __init__(self, screen):

        self.screen = screen
        self.__stats_to_display = []

        self.__text_to_display = "data"
        self.__data_to_display = "text"

        self.font = pygame.font.SysFont(None, 24)

    def clear_stats(self):
        self.__stats_to_display = []

    def add_stat(self,text:list, data:list):
        self.__stats_to_display.append(f"""{text}: {data}""")

    def set_stats(self, text:list, data:list):
        total:list = []
        for i in range(len(text)):
            total.append(f"""{text[i]}: {data[i]:.0f}""")
        self.__stats_to_display = total

    def update(self):
        wall_surface = pygame.Surface([200, 150])
        wall_surface.fill((0,0,0))
        self.screen.blit(wall_surface, (self.screen.get_width()-200, 0))

        index = 0
        for text in self.__stats_to_display:
            stats_surface = self.font.render(text, True, (255,255,255))
            text_rect = stats_surface.get_rect()
            text_rect.topright = ((self.screen.get_width() - 10), (15*index))
            self.screen.blit(stats_surface, text_rect)
            index += 1

    def update_loop(self):
        while True:
            self.update()

class Viewer:
    def __init__(self, grid):
        # pygame stuff
        self.window_size = [500, 500]
        self.screen = pygame.display.set_mode(self.window_size, flags=pygame.RESIZABLE)
        self.screen_rgb = (100,100,100)
        pygame.display.set_caption('BWARD stuff v1.4')
        self.steps_flag = False
        self.rainbow_flag:bool = True  # pretty by default :3


        self.clock = pygame.time.Clock()
        self.target_fps = 144

        #self.shared_info_obj = Shared_Info(self.screen, self.clock, self.steps_flag, self.rainbow_flag)
        self.stats = Stats(self.screen)

        self.running = True

        #
        self.grid = grid
        self.best_path = [(None, None)]

        self.point1 = (None, None)
        self.point2 = (None, None)

        self.point1_rendered = (None, None)
        self.point2_rendered = (None, None)
        self.length_of_path = len(grid) - 1

        self.rgb = [255, 0, 255]
        self.target_rgb = [0, 165, 255]

        self.dijkstra_start_rgb = [255,0,0]
        self.dijkstra_target_rgb = [0,0,255]

        # A list for holding all events whilst stuff is being displayed slowly. preventing a crash.
        self.event_list = []

        #used for checking if the window has changed and will then re display the grid.
        self.had_window_changed = False

    def dijkstra(self,display=False, wait=0.0):
        # THIS PART IS NOT MY CODE IDK HOW THIS WORKS
        goal: tuple = self.point2
        start: tuple = self.point1

        #self.point1_rendered = None
        #self.point2_rendered = None

        if goal == (None, None) or start == (None, None):
            return (0, None)
        rows, cols = len(self.grid), len(self.grid[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[start[0]][start[1]] = 0
        came_from = {}  # Dictionary to track the path
        pq = [(0, start)]  # Manually managed priority queue: (distance, (row, col))
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        path_rgb = self.dijkstra_start_rgb
        target_path_rgb = self.dijkstra_target_rgb
        wall_surface = pygame.Surface(
            [self.screen.get_width() // len(self.grid[0]), self.screen.get_height() // len(self.grid)])

        rgb_mode = 0
        counter = 0
        color_cycle = [
            (255, 0, 0),  # Red
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 255, 255),  # Cyan
            (0, 0, 255),  # Blue
            (255, 0, 255)  # Magenta
        ]

        while pq:

            fps = f"{self.clock.get_fps():.0f}"
            self.stats.clear_stats()
            self.stats.add_stat("FPS", fps)
            self.stats.add_stat("target FPS", self.target_fps)
            self.stats.add_stat("rainbow_flag", self.rainbow_flag)
            self.stats.add_stat("steps flag", self.steps_flag)
            self.stats.add_stat("point1", self.point1)
            self.stats.add_stat("point2", self.point2)
            self.stats.add_stat("rendered point1", self.point1_rendered)
            self.stats.add_stat("rendered point2", self.point2_rendered)
            self.stats.update()

            self.handle_events()

            if not self.running:
                return self.length_of_path, None

            #if the window has changed then everything needs re rendering
            if self.had_window_changed:
                self.screen.fill(self.screen_rgb)
                self.__render_grid()
                self.__render_points()
                wall_surface = pygame.Surface(
                    [self.screen.get_width() // len(self.grid[0]), self.screen.get_height() // len(self.grid)])
                self.had_window_changed = False


            # Sort the list to find the element with the minimum distance
            pq.sort(key=lambda x: x[0])
            current_distance, (current_row, current_col) = pq.pop(0)  # Pop the smallFest element

            # ===== my edits to the algorithm start here======
            if goal != self.point2 or start != self.point1:
                print("diff points detected!")
                return self.length_of_path, None

            if self.steps_flag or display:
                if self.rainbow_flag:
                    counter += 1
                    if counter >= 100:
                        rgb_mode = (rgb_mode+1) % 6
                        target_path_rgb = color_cycle[rgb_mode]
                        counter = 0
                        self.length_of_path = 5

                rgb_change_per_step = self.calculate_rgb(target_path_rgb, path_rgb, len(self.grid))

                wall_surface.fill(path_rgb)

                path_rgb = self.apply_rgb_change(rgb_change_per_step, path_rgb)

                self.screen.blit(wall_surface, (current_col * wall_surface.get_width(), current_row * wall_surface.get_height()))
                if self.target_fps is not None:
                    self.clock.tick(self.target_fps)
                else:
                    self.clock.tick()

                pygame.display.flip()
                time.sleep(wait)


            # ===== my edits to the algorithm end here======

            if (current_row, current_col) == goal:
                # Reconstruct the path from end_goal to start
                path = []
                while (current_row, current_col) != start:
                    path.append((current_row, current_col))
                    current_row, current_col = came_from[(current_row, current_col)]
                path.append(start)
                path.reverse()

                self.point1_rendered = self.point1
                self.point2_rendered = self.point2

                return current_distance, path

            if current_distance > distances[current_row][current_col]:
                continue

            for dr, dc in directions:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                    if not self.grid[neighbor_row][neighbor_col]:  # Check if it's not a wall
                        new_distance = current_distance + 1

                        if new_distance < distances[neighbor_row][neighbor_col]:
                            distances[neighbor_row][neighbor_col] = new_distance
                            came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
                            pq.append((new_distance, (neighbor_row, neighbor_col)))
        return -1, None  # If goal is unreachable

    def __render_grid(self):
        wall_surface = pygame.Surface(
            [self.screen.get_width() // len(self.grid[0]), self.screen.get_height() // len(self.grid)]
        )

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.screen.blit(wall_surface, (x * wall_surface.get_width(), y * wall_surface.get_height()))

    def get_x_y(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        """from a given set of coordinates, return the x and y coordinates from the grid that the coords be on"""

        x_index = screen_x // (self.screen.get_width() // len(self.grid[0]))
        y_index = screen_y // (self.screen.get_height() // len(self.grid[0]))


        #  These try and excepts are to catch when the point selected is out of bounds
        #  due to the rounding error when creating the gridy :3
        try:  # testing the X axis
            self.grid[0][x_index]
        except IndexError:  # for when the user clicks off the board it will snap to the closest axis.
            x_index = len(self.grid[0]) - 1
            print("x_index",x_index)

        try:  # testing the Y axis
            self.grid[y_index]
        except IndexError:
            y_index = len(self.grid) - 1
            print("y_index", y_index)

        return x_index, y_index

    @staticmethod
    def calculate_rgb(target_rgb , current_rgb, length):
        rgb_change_per_step = []

        for i in range(3):
            color = ((target_rgb[i] - current_rgb[i]) / length)
            rgb_change_per_step.append(color)
        return rgb_change_per_step

    @staticmethod
    def apply_rgb_change(rgb_change, current_hrt):  # todo :3
        return [abs(rgb_change[0] + current_hrt[0]), abs(rgb_change[1] + current_hrt[1]), abs(rgb_change[2] + current_hrt[2])]

    def __render_path(self, wait=0):
        #the wait function is only impactful when its higher than (fps / 60) / 100 (idk if its 100 could be more)
        path_surface = pygame.Surface(
            [self.screen.get_width() / len(self.grid[0]), self.screen.get_height() / len(self.grid)])

        # the target_rgb can be edited in the __init__
        rgb = self.rgb
        rgb_change_per_step = self.calculate_rgb(self.target_rgb, rgb, self.length_of_path)  # this line took longer to code then it should have, smh my head

        # as the first condition will be met first it wont cause a error checking the second part
        if not self.best_path or self.best_path[0] == (None, None):
            return -1

        point: tuple = (0, 0)  # To stop pycharm annoying me and giving a lil yellow warning a couple lines down.
        for point in self.best_path:
            self.handle_events()

            if not self.running or ((self.point1_rendered is not None or self.point2_rendered is not None) and ((self.point1 != self.point1_rendered) or (self.point2 != self.point2_rendered))):
                return -1

            if self.had_window_changed:
                self.screen.fill(self.screen_rgb)
                self.__render_grid()
                self.__render_points()
                path_surface = pygame.Surface([self.screen.get_width() / len(self.grid[0]), self.screen.get_height() / len(self.grid)])
                self.had_window_changed = False

            # This is done here for the colour gradient
            path_surface.fill(rgb)

            # Actually renders the tile/surface
            self.screen.blit(path_surface, (point[1] * path_surface.get_width(), point[0] * path_surface.get_height()))

            if point != self.best_path[-1]:
                rgb = [abs(rgb[0] + rgb_change_per_step[0]), abs(rgb[1] + rgb_change_per_step[1]),
                       abs(rgb[2] + rgb_change_per_step[2])]
            else:
                print("BREAKING")
                break

            # Checking if the programme should wait a short amount of time before displaying the next tile/surface.
            if self.steps_flag:
                time.sleep(wait)
                if self.target_fps is not None:
                    self.clock.tick(self.target_fps)
                else:
                    self.clock.tick()

            pygame.display.flip()
        print("heeeeyyy pookie")
        self.point1_rendered = self.point1
        self.point2_rendered = self.point2
        print("rendered points", self.point1_rendered, self.point2_rendered)
        print("poinst just points", self.point1, self.point2)


    def __render_points(self):
        path_surface = pygame.Surface(
            [self.screen.get_width() // len(self.grid[0]), self.screen.get_height() // len(self.grid)])

        path_surface.fill((255, 165, 0))  # makes the tile/surface orange to show what has been selected

        if self.point1 != (None, None):
            self.screen.blit(path_surface,
                             (self.point1[1] * path_surface.get_width(), self.point1[0] * path_surface.get_height()))

        if self.point2 != (None, None):
            self.screen.blit(path_surface,
                             (self.point2[1] * path_surface.get_width(), self.point2[0] * path_surface.get_height()))

        self.handle_events()
        # for when either of the points are given a None value (im to lazy to go around and make sure the points are
        # valid)

    def on_left_click(self, x, y):
        """this will be used for more functionality when I can be asked to"""
        x_index, y_index = self.get_x_y(x, y)
        if self.grid[y_index][x_index] == 0:  # if its 0 then is not a wall thus valid
            if (y_index, x_index) != self.point2:  # If the other point is not already on that point
                self.point1 = y_index, x_index

    def on_right_click(self, x, y):
        """this will be used for more functionality when I can be asked to"""
        x_index, y_index = self.get_x_y(x, y)
        if self.grid[y_index][x_index] == 0:  # if its 0 then is not a wall thus valid
            if (y_index, x_index) != self.point1:  # If the other point is not already on that point
                self.point2 = y_index, x_index

    def gather_events(self):
        self.event_list = []
        for event in pygame.event.get():
            self.event_list.append(event)

    def handle_events(self):

        # Validating the event_list is not empty.

        if not self.event_list:
            self.gather_events()

        for event in self.event_list:

            if event.type == pygame.WINDOWRESIZED:
                self.had_window_changed = True

            # to handle pressing the lil X in the top right corner of the tab.
            if event.type == pygame.QUIT:
                self.running = False

            # For all mouse inputs
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 meaning left click, 2 being middle click, 3 being right click
                    self.on_left_click(event.pos[0], event.pos[1])

                # If middle mouse button or space is pressed(because it's hard to middle-click on a laptop)
                if event.button == 2:
                    self.steps_flag = not self.steps_flag

                if event.button == 3:
                    self.on_right_click(event.pos[0], event.pos[1])

            if event.type == pygame.KEYDOWN:
                # if middle mouse button or space is pressed(because it's hard to middle-click on a laptop)
                if event.key == pygame.K_SPACE:
                    self.steps_flag = not self.steps_flag

                if event.key == pygame.K_r:
                    self.rainbow_flag = not self.rainbow_flag
                    print("current rainbow value", self.rainbow_flag)
        self.event_list = []

    def run(self):
        """this is the main game loop, and it will handle the inputs from the screen."""

        while self.running and self.screen is not None:


            self.gather_events()
            self.handle_events()  # Could just leave handle_events() and remove gather_events() but it reads better yk.

            self.screen.fill(self.screen_rgb)  # This is the background color

            self.__render_grid()
            self.__render_points()

            dont_remake_path = True
            if (self.point1 != (None, None) and self.point2 != (None, None)) and (
                self.point1 != self.point1_rendered or self.point2 != self.point2_rendered):

                # Finds the shortest path between the 2 points
                print("starting dijskstra")
                self.length_of_path, self.best_path = self.dijkstra(display=True, wait=0)
                print("shortest path length:", self.length_of_path)
                dont_remake_path = False

            # used for de-bugging the statement above
            if (self.point1 != self.point1_rendered or self.point2 != self.point2_rendered) and (
                self.point1 != (None, None) and self.point2 != (None, None)):
                pass


            # just making sure it only renders valid data and not None data types
            if self.point1 != (None, None) and self.point2 != (None, None) and self.best_path is not None:
                # Checks if the path length is long enough to display
                if self.length_of_path >= 1:
                    # Checking if its valid and should not be change while being displayed leading to gaps at the end of the line
                    if len(self.best_path) >= 2 and not dont_remake_path:
                        # popping the first and last items in the best path, so it won't get rendered to save resources
                        self.best_path.pop(-1)
                        self.best_path.pop(0)

                    # setting these values here instead of after the rendering, so the point values don't change
                    # from the user selecting new points as its running.

                    #if self.steps_flag:
                    #    self.__render_path_steps(0.03)
                    #else:
                    self.__render_path(wait=0)

            #render_time = (time.time() - start_time) * 1000
            #fps = self.clock.get_fps()
            #self.stats.set_stats(["FPS"],[fps])
            #self.stats.update(self.screen)

            pygame.display.flip()
            if self.target_fps is not None:
                self.clock.tick(self.target_fps)
            else:
                self.clock.tick()

        pygame.quit()


if __name__ == '__main__':
    main_grid = mappy.generate_maze(100,100)

    pygame.init()
    viewer = Viewer(main_grid)
    viewer.run()

# FIXED: make a algorithm the generate the grid generative
# FIXED: fix error when clicking off the grid the rgb values break
# TODO : have a option to display the search algorithm in real time or slowed a lil
# TODO : have a range of search algorithms to select from.
# FIXED : fix when the length is too long that when its used to divide the RGB value rounds down
# FIXED : could right and left click the same tile for both the points to stay on the same tile
