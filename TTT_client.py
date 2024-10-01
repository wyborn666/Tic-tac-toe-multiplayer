import tic_tac_toe
import pygame
import threading
import socket
import struct
import sys
from tic_tac_toe import Button

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 5007
ANY = "0.0.0.0"
BLACK = (0, 0, 0)

class Client:
    def __init__(self):
        self.turn = False
        self.running = True
        self.player = "O"
        self.opponent = "X"
        self.available_servers = {}
        self.selected_server = ""
        self.server_connected = False
        self.y_offset = 50
        self.in_server_selection = True

        self.grid = tic_tac_toe.Grid()
        self.surface = self.grid.set_my_window("Client")

        self.connect_button_image = pygame.Surface((100, 30))
        self.connect_button_image.fill((255, 255, 255))
        self.connect_button = Button(30, self.y_offset + 400, self.connect_button_image, 1, text="Connect")

    def create_thread(self, target):
        thread_gen = threading.Thread(target=target, daemon=True)
        thread_gen.start()

    def listen_for_servers(self):
        while True:
            data, addr = self.mltClient.recvfrom(1024)
            server_info = data.decode()
            if server_info not in self.available_servers:
                self.available_servers[server_info] = addr
                #print(f"Found server: {server_info} at {addr}")

    def received_data(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
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

    def draw_server_selection(self):
        self.surface.fill(tic_tac_toe.MENU_COLOR)
        self.y_offset = 50

        font_small = pygame.font.Font(None, 30)

        for i, server in enumerate(self.available_servers):
            server_text = f"{i + 1}. {server}"
            text_surface = font_small.render(server_text, True, BLACK)
            self.surface.blit(text_surface, (50, self.y_offset))
            self.y_offset += 30

        input_prompt = font_small.render("Enter server number to connect: ", True, BLACK)
        self.surface.blit(input_prompt, (30, self.y_offset + 30))

        server_input_surface = font_small.render(self.selected_server, True, BLACK)
        self.surface.blit(server_input_surface, (350, self.y_offset + 30))

        # Draw button
        self.connect_button.update(self.surface, pygame.mouse.get_pos())

    def handle_server_selection_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.selected_server = self.selected_server[:-1]
            elif event.key == pygame.K_RETURN:
                self.connect_to_selected_server()
            else:
                self.selected_server += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button click
            self.connect_button.proc_event(event)
            if self.connect_button.is_click:
                self.connect_to_selected_server()

    def connect_to_selected_server(self):
        if self.selected_server.isdigit():
            selected_index = int(self.selected_server) - 1
            if 0 <= selected_index < len(self.available_servers):
                server_info = list(self.available_servers.keys())[selected_index]
                server_ip, server_port = server_info.split(':')
                server_port = int(server_port)

                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((server_ip, server_port))
                self.create_thread(self.received_data)

                #print(f"Connected to {server_ip}:{server_port}")
                self.server_connected = True
                self.in_server_selection = False  # Switch to game mode

    def game(self):
        self.mltClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mltClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mltClient.bind((ANY, MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.mltClient.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.create_thread(self.listen_for_servers)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.in_server_selection:
                    self.handle_server_selection_event(event)
                else:
                    self.handle_game_event(event)

            self.surface.fill((10, 100, 100))
            if self.in_server_selection:
                self.draw_server_selection()
            else:
                self.grid.draw(self.surface)

                if self.grid.game_over or self.grid.win_case(self.opponent) or self.grid.draw_case():
                    self.grid.update_score_and_display(self.surface, self.player)

            pygame.display.update()

    def handle_game_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.turn and not self.grid.game_over:
            pos = pygame.mouse.get_pos()
            x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
            self.grid.get_mouse(x_pos, y_pos, self.player)

            if self.grid.switch:
                if self.grid.win_case(self.player):
                    self.grid.score_wins_o += 1

                data = f'{x_pos}.{y_pos}.{self.grid.condition}'.encode()
                try:
                    self.client.send(data)
                    self.turn = False
                except Exception as e:
                    sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.grid.game_over:
                data = "new"
                self.client.send(data.encode())
                self.grid.reset()

pygame.init()
client = Client()
client.game()
