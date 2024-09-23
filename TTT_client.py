import pygame
import tic_tac_toe
import threading
import socket

icon = pygame.image.load("models//icon.png")

surface = pygame.display.set_mode((tic_tac_toe.WIDTH, tic_tac_toe.HEIGHT))
pygame.display.set_caption("Client")
pygame.display.set_icon(icon)

def create_thread(target):
    thread_gen = threading.Thread(target=target, daemon=True)
    thread_gen.start()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

def received_data():
    while True:
        data = client.recv(1024).decode()
        data = data.split('.')
        x, y = int(data[0]), int(data[1])
        #x, y - coordinates of opponent's move
        #turn_status - current turn status

        print(data)


create_thread(received_data)

running = True
grid = tic_tac_toe.Grid()
opponent = "X"
player = "O"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
            grid.get_mouse(x_pos, y_pos, player)

            data = '{}.{}'.format(x_pos, y_pos).encode()
            client.send(data)


    surface.fill(tic_tac_toe.BG_COLOR)
    grid.draw(surface)
    pygame.display.update()