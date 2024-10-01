import tic_tac_toe
import pygame
import threading
import socket
import re
import struct

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
ANY = "0.0.0.0"
 

class Client:
    def __init__(self):
        self.turn = False
        self.running = True
        self.connection_success = False
        self.player = "O"
        self.opponent = "X"
        self.available_servers = {}


        self.grid = tic_tac_toe.Grid()
        self.surface = self.grid.set_my_window("client")

    def create_thread(self, target):
        thread_gen = threading.Thread(target=target, daemon=True)
        thread_gen.start()

    def listen_for_servers(self):
        while True:
            data, addr = self.mltClient.recvfrom(1024)
            server_info = data.decode()
            if server_info not in self.available_servers:
                self.available_servers[server_info] = addr
                print(f"Found server: {server_info} at {addr}")

    def received_data(self):
        while True:
            data = self.client.recv(1024).decode()

            if re.match(r'new', data):
                self.grid.reset()
                self.turn = False

            elif re.match(r'\d.\d.\d$', data):
                data = data.split('.')
                x, y, condition = int(data[0]), int(data[1]), int(data[2])
                self.grid.set_cell_value(x, y, self.opponent)
                if condition:
                    self.grid.score_wins_x += 1
                self.turn = True
    '''
    def main_menu(self):
        self.mltClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mltClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mltClient.bind((ANY, MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.mltClient.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Searching for servers...")

        self.create_thread(self.listen_for_servers)

        print("\nAvailable servers:")
        for i, server in enumerate(self.available_servers):
            print(f"{i + 1}. {server}")

        choice = int(input("Select server number to connect to: ")) - 1
        selected_server = list(self.available_servers.keys())[choice]
        server_ip, server_port = selected_server.split(':')
        server_port = int(server_port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")
        
        self.create_thread(self.received_data)
    '''
    
    def game(self):
        self.mltClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mltClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mltClient.bind((ANY, MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.mltClient.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Searching for servers...")

        self.create_thread(self.listen_for_servers)

        print("\nAvailable servers:")
        for i, server in enumerate(self.available_servers):
            print(f"{i + 1}. {server}")

        choice = int(input("Select server number to connect to: ")) - 1
        selected_server = list(self.available_servers.keys())[choice]
        server_ip, server_port = selected_server.split(':')
        server_port = int(server_port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))
        print(f"Connected to server {server_ip}:{server_port}")
        
        self.create_thread(self.received_data)
                
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.turn and not self.grid.game_over:
                    pos = pygame.mouse.get_pos()
                    x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
                    self.grid.get_mouse(x_pos, y_pos, self.player)

                    if self.grid.switch:
                        if self.grid.win_case(self.player):
                            self.grid.score_wins_o += 1

                        data = '{}.{}.{}'.format(x_pos, y_pos, self.grid.condition).encode()
                        self.client.send(data)
                        self.turn = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.grid.game_over:
                        data = "new"
                        self.client.send(data.encode())
                        self.grid.reset()
            
            self.surface.fill(tic_tac_toe.BG_COLOR)
            self.grid.draw(self.surface)

            if self.grid.game_over or self.grid.win_case(self.opponent) or self.grid.draw_case():
                self.grid.update_score_and_display(self.surface,self.player)

            pygame.display.update()

pygame.init()
client = Client()
client.game()

