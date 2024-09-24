import tic_tac_toe
import pygame
import threading
import socket
import re
 

class Client:
    def __init__(self):
        self.turn = False
        self.running = True
        self.player = "O"
        self.opponent = "X"

        self.grid = tic_tac_toe.Grid()
        self.surface = self.grid.set_my_window("client")

    def create_thread(self, target):
        thread_gen = threading.Thread(target=target, daemon=True)
        thread_gen.start()

    def received_data(self):
        while True:
            data = self.client.recv(1024).decode()

            if re.match(r'new', data):
                self.grid.reset()
                self.turn = False

            elif re.match(r'\d.\d$', data):
                data = data.split('.')
                x, y = int(data[0]), int(data[1])
                self.grid.set_cell_value(x, y, self.opponent)
                self.turn = True

    
    def game(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 12345))
        
        self.create_thread(self.received_data)

                
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.grid.game_over and self.turn:
                    pos = pygame.mouse.get_pos()
                    x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
                    self.grid.get_mouse(x_pos, y_pos, self.player)

                    if self.grid.switch:
                        data = '{}.{}'.format(x_pos, y_pos).encode()
                        self.client.send(data)
                        self.turn = False
                
                if self.grid.win_case(self.player):
                    data = "new"
                    self.user.send(data.encode())
                    print(f"Player {self.player} wins!")
                    self.grid.reset()
                    self.turn = False


            self.surface.fill(tic_tac_toe.BG_COLOR)
            self.grid.draw(self.surface)
            pygame.display.update()


client = Client()
client.game()

