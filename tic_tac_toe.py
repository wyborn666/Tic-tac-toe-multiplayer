import socket
import pygame


WIDTH , HEIGHT = 700, 700
BG_COLOR = (10, 100, 100)
LINES_COLOR = (255, 255, 255)


class Grid:
    
    def __init__(self):
        self.grid_lines = [((0, HEIGHT/3), (WIDTH, HEIGHT/3)), 
                           ((0, HEIGHT/3*2), (WIDTH, HEIGHT/3*2)),
                           ((WIDTH/3, 0), (WIDTH/3, HEIGHT)),
                           ((WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT))]
        
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.switch = True

        self.x_symbol = pygame.image.load("models//X.png")
        self.y_symbol = pygame.image.load("models//O.png")
        self.icon = pygame.image.load("models//icon.png")

        self.x_symbol = pygame.transform.scale(self.x_symbol, ((WIDTH/3), (HEIGHT/3)))
        self.y_symbol = pygame.transform.scale(self.y_symbol, ((WIDTH/3), (HEIGHT/3)))
        
    
    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (LINES_COLOR), line[0], line[1], width=5)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(self.x_symbol, (x * WIDTH/3, y * HEIGHT/3))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(self.y_symbol, ((x * WIDTH/3, y * HEIGHT/3)))

    def get_cell_value(self, x, y):
        return self.grid[y][x]
    
    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.switch = True
            if player == "X":
                self.set_cell_value(x, y, "X")
            elif player == "O":
                self.set_cell_value(x, y, "O")
        else:
            self.switch = False

    def win_case(self, player):
        for row in range(3):
            if self.grid[row][0] == self.grid[row][1] == self.grid[row][2] == player:
                self.game_over = True
                return True

        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] == player:
                self.game_over = True
                return True

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == player:
            self.game_over = True
            return True

        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == player:
            self.game_over = True
            return True

        return False

    def draw_case(self):
        for row in self.grid:
            if 0 in row:
                return False
        return True

    def print_grid(self):
        for row in self.grid:
            print(row)

    def set_my_window(self, window_name):
        surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(window_name)
        pygame.display.set_icon(self.icon)
        return surface



