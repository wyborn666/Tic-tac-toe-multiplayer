import pygame
import tic_tac_toe
import threading
import socket

grid = tic_tac_toe.Grid()
surface = grid.set_my_window("client")

def create_thread(target):
    thread_gen = threading.Thread(target=target, daemon=True)
    thread_gen.start()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

def received_data():
    global turn
    while True:
        data = client.recv(1024).decode()
        data = data.split('.')
        x, y = int(data[0]), int(data[1])
        #x, y - coordinates of opponent's move
        turn = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, opponent)
        print(data)


create_thread(received_data)

turn = False
running = True
opponent = "X"
player = "O"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over and turn:
            pos = pygame.mouse.get_pos()
            x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
            grid.get_mouse(x_pos, y_pos, player)

            data = '{}.{}'.format(x_pos, y_pos).encode()
            client.send(data)
            turn = False


    surface.fill(tic_tac_toe.BG_COLOR)
    grid.draw(surface)
    pygame.display.update()

