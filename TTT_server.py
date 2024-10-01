import tic_tac_toe
import pygame
import threading
import socket
import struct
import time
import sys

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
SERVER_PORT = 1234
SERVER_IP = socket.gethostbyname(socket.getfqdn())
BLACK = (0, 0, 0)

class Server:
    def __init__(self):
        self.user, self.address = None, None
        self.connection_success = False
        self.reset_var = False
        self.turn = True
        self.running = True
        self.player = "X"
        self.opponent = "O"

        self.grid = tic_tac_toe.Grid()
        self.surface = self.grid.set_my_window("Server")
    
    def create_thread(self, target):
        thread_gen = threading.Thread(target=target, daemon=True)
        thread_gen.start()

    def announce_server(self):
        mltSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mltSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
        while True:
            message = f"{SERVER_IP}:{SERVER_PORT}"
            mltSocket.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
            time.sleep(5)

    def connection(self):
        self.user, self.address = self.server.accept()
        self.connection_success = True
        self.received_data()

    def received_data(self):
        while True:
            try:
                data = self.user.recv(1024).decode()
                if data == "new":
                    self.grid.reset()
                    self.turn = False
                else:
                    x, y, condition = map(int, data.split('.'))
                    self.grid.set_cell_value(x, y, self.opponent)
                    if condition:
                        self.grid.score_wins_x += 1
                    self.turn = True
            except Exception as e:
                self.running = False

    def main_menu(self):
        self.create_thread(self.announce_server)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((SERVER_IP, SERVER_PORT))
        self.server.listen(1)
        
        self.create_thread(self.connection)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            font_small = pygame.font.Font(None, 60)

            self.surface.fill(tic_tac_toe.MENU_COLOR)
            self.surface.blit(self.grid.waiting_for_connection, (90, 90))
            
            text = font_small.render("Waiting for connection", True, BLACK)
            self.surface.blit(text, (24, 30))


            pygame.display.update()
            if self.connection_success:
                running = False
                self.game()

    def game(self):
        self.create_thread(self.announce_server)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.connection_success and self.turn and not self.grid.game_over:
        
                    pos = pygame.mouse.get_pos()
                    x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
                    self.grid.get_mouse(x_pos, y_pos, self.player)

                    if self.grid.switch:
                        if self.grid.win_case(self.player):
                            self.grid.score_wins_x += 1

                        data = '{}.{}.{}'.format(x_pos, y_pos, self.grid.condition)
                        try:
                            self.user.send(data.encode())
                            self.turn = False
                        except Exception as e:
                            sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.grid.game_over:
                        data = "new"
                        self.user.send(data.encode())
                        self.grid.reset()
                        self.turn = True
            
            self.surface.fill(tic_tac_toe.BG_COLOR)
            self.grid.draw(self.surface)

            if self.grid.game_over or self.grid.win_case(self.opponent) or self.grid.draw_case():
                self.grid.update_score_and_display(self.surface,self.player)

            pygame.display.update()


pygame.init()
serv = Server()
serv.main_menu()