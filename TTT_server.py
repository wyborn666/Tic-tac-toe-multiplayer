import tic_tac_toe
import pygame
import threading
import socket

connection_success = False
user, address = None, None

grid = tic_tac_toe.Grid()
surface = grid.set_my_window("Server")


def create_thread(target):
    thread_gen = threading.Thread(target=target, daemon=True)
    thread_gen.start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(1)


def received_data():
    global turn
    while True:
        data = user.recv(1024).decode()
        data = data.split('.')
        x, y = int(data[0]), int(data[1])
        #x, y - coordinates of opponent's move
        #turn_status - current turn status
        turn = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, opponent)
        print(data)

def connection():
    global user, address, connection_success
    user, address = server.accept()
    connection_success = True
    received_data()


turn = True
running = True
player = "X"
opponent = "O"

create_thread(connection)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and connection_success and turn:
            pos = pygame.mouse.get_pos()
            x_pos, y_pos = pos[0] // int(tic_tac_toe.WIDTH / 3), pos[1] // int(tic_tac_toe.HEIGHT / 3)
            grid.get_mouse(x_pos, y_pos, player)


            data = '{}.{}'.format(x_pos, y_pos)
            user.send(data.encode())
            turn = False


    surface.fill(tic_tac_toe.BG_COLOR)
    grid.draw(surface)
    pygame.display.update()