import pygame
import pygame.freetype

WIDTH , HEIGHT = 300, 300
BG_COLOR = (10, 100, 100)
MENU_COLOR = (163, 172, 173)
LINES_COLOR = (255, 255, 255)


class Grid:
    
    def __init__(self):
        self.grid_lines = [((0, HEIGHT/3), (WIDTH, HEIGHT/3)), 
                           ((0, HEIGHT/3*2), (WIDTH, HEIGHT/3*2)),
                           ((WIDTH/3, 0), (WIDTH/3, HEIGHT)),
                           ((WIDTH/3*2, 0), (WIDTH/3*2, HEIGHT))]
        
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.switch = True
        self.winning_cells = []
        self.game_over = False

        self.x_symbol = pygame.image.load("models//X.png")
        self.o_symbol = pygame.image.load("models//O.png")
        self.x_symbol_win = pygame.image.load("models//X_win.png")
        self.o_symbol_win = pygame.image.load("models//O_win.png")
        self.icon = pygame.image.load("models//icon.png")
        self.font_winner = pygame.freetype.Font("models//SkrampCyr-Regular_0.ttf", 24)
        self.font_continue = pygame.freetype.Font("models//SkrampCyr-Regular_0.ttf", 20)

        self.x_symbol = pygame.transform.scale(self.x_symbol, ((WIDTH/3), (HEIGHT/3)))
        self.o_symbol = pygame.transform.scale(self.o_symbol, ((WIDTH/3), (HEIGHT/3)))
        self.x_symbol_win = pygame.transform.scale(self.x_symbol_win, ((WIDTH // 3), (HEIGHT // 3)))
        self.o_symbol_win = pygame.transform.scale(self.o_symbol_win, ((WIDTH // 3), (HEIGHT // 3)))

        self.score_wins_x = 0
        self.score_wins_o = 0
        self.condition = 0
         
    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (LINES_COLOR), line[0], line[1], width=5)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    if (x, y) in self.winning_cells:
                        surface.blit(self.x_symbol_win, (x * WIDTH / 3, y * HEIGHT / 3))
                    else:
                        surface.blit(self.x_symbol, (x * WIDTH/3, y * HEIGHT/3))

                elif self.get_cell_value(x, y) == "O":
                    if (x, y) in self.winning_cells:
                        surface.blit(self.o_symbol_win, ((x * WIDTH / 3, y * HEIGHT / 3)))
                    else:
                        surface.blit(self.o_symbol, (x * WIDTH / 3, y * HEIGHT / 3))

    def draw_client_menu(self, surface):
        pass

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
                self.winning_cells = [(0, row), (1, row), (2, row)]
                self.condition = 1
                return True

        for col in range(3):
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] == player:
                self.game_over = True
                self.winning_cells = [(col, 0), (col, 1), (col, 2)]
                self.condition = 1
                return True

        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == player:
            self.game_over = True
            self.winning_cells = [(0, 0), (1, 1), (2, 2)]
            self.condition = 1
            return True

        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == player:
            self.game_over = True
            self.winning_cells = [(2, 0), (1, 1), (0, 2)]
            self.condition = 1
            return True

        return False

    def draw_case(self):
        for row in self.grid:
            if 0 in row:
                return False
        self.game_over = True
        return True

    def print_grid(self):
        for row in self.grid:
            print(row)

    def reset(self):
        self.grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.condition = 0
        self.switch = True
        self.game_over = False
        self.winning_cells = []

    def update_score_and_display(self, surface, player):        
        text_surface_x, rect_x = self.font_winner.render(f"Player X: {self.score_wins_x}", (0, 0, 0))
        surface.blit(text_surface_x, (150, 250))

        text_surface_o, rect_o = self.font_winner.render(f"Player O: {self.score_wins_o}", (0, 0, 0))
        surface.blit(text_surface_o, (150, 300))


        text_surface, rect = self.font_continue.render("Press space to continue", (0, 0, 0))
        surface.blit(text_surface, (197, 450))

    def set_my_window(self, window_name):
        surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(window_name)
        pygame.display.set_icon(self.icon)
        return surface


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.is_click = False

    def update(self, screen, mouse_pos):
        screen.blit(self.image, self.rect.topleft)
        self.is_click = self.rect.collidepoint(mouse_pos)

    def proc_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_click:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))