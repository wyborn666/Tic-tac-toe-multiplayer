import tic_tac_toe
import pygame
import threading
import socket
import re


class Server:
    def __init__(self):
        self.connection_success = False
        self.user, self.address = None, None
        self.turn = True
        self.running = True
        self.player = "X"
        self.opponent = "O"

        self.grid = tic_tac_toe.Grid()
        self.surface = self.grid.set_my_window("Server")
    
    def create_thread(self, target):
        thread_gen = threading.Thread(target=target, daemon=True)
        thread_gen.start()

    def connection(self):
        self.user, self.address = self.server.accept()
        self.connection_success = True
        self.received_data()

    def received_data(self):
        while True:
            data = self.user.recv(1024).decode()

            if re.match(r'new', data):
                self.grid.reset()
                self.turn = True

            elif re.match(r'\d.\d$', data):
                data = data.split('.')
                x, y = int(data[0]), int(data[1])
                self.grid.set_cell_value(x, y, self.opponent)
                self.turn = True

    def game(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 12345))
        self.server.listen(1)
        
        self.create_thread(self.connection)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.connection_success and self.turn and not self.grid.game_over:
        
                    pos = pygame.mouse.get_pos()
                    x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
                    self.grid.get_mouse(x_pos, y_pos, self.player)

                    if self.grid.switch:
                        data = '{}.{}'.format(x_pos, y_pos)
                        self.user.send(data.encode())
                        self.turn = False
                
                if self.grid.win_case(self.player):
                    data = "new"
                    self.user.send(data.encode())
                    print(f"Player {self.player} wins!")
                    self.grid.reset()
                    self.turn = True
            
            self.surface.fill(tic_tac_toe.BG_COLOR)
            self.grid.draw(self.surface)
            pygame.display.update()

serv = Server()
serv.game()