#controller.py
import socket
import json
import csv
import os
from game_state import GameState
from bot import Bot
import sys

LOG_FILE = 'game_data.csv'

class DataLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file_exists = os.path.isfile(self.filename)
        if not self.file_exists:
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                # write header row
                header = [
                    'timer', 'fight_result', 'has_round_started', 'is_round_over',
                    'p1_id', 'p1_health', 'p1_x', 'p1_y', 'p1_jumping', 'p1_crouching',
                    'p1_in_move', 'p1_move_id',
                    'p1_btn_up', 'p1_btn_down', 'p1_btn_right', 'p1_btn_left', 'p1_btn_Y', 'p1_btn_B', 'p1_btn_X', 'p1_btn_A', 'p1_btn_L', 'p1_btn_R',
                    'p2_id', 'p2_health', 'p2_x', 'p2_y', 'p2_jumping', 'p2_crouching',
                    'p2_in_move', 'p2_move_id',
                    'p2_btn_up', 'p2_btn_down', 'p2_btn_right', 'p2_btn_left', 'p2_btn_Y', 'p2_btn_B', 'p2_btn_X', 'p2_btn_A', 'p2_btn_L', 'p2_btn_R'
                ]
                writer.writerow(header)

    def log(self, game_state, command):
        row = [
            game_state.timer, game_state.fight_result, game_state.has_round_started, game_state.is_round_over,
            game_state.player1.player_id, game_state.player1.health, game_state.player1.x_coord, game_state.player1.y_coord,
            game_state.player1.is_jumping, game_state.player1.is_crouching, game_state.player1.is_player_in_move, game_state.player1.move_id,
            game_state.player1.player_buttons.up, game_state.player1.player_buttons.down,
            game_state.player1.player_buttons.right, game_state.player1.player_buttons.left,
            game_state.player1.player_buttons.Y, game_state.player1.player_buttons.B,
            game_state.player1.player_buttons.X, game_state.player1.player_buttons.A,
            game_state.player1.player_buttons.L, game_state.player1.player_buttons.R,
            game_state.player2.player_id, game_state.player2.health, game_state.player2.x_coord, game_state.player2.y_coord,
            game_state.player2.is_jumping, game_state.player2.is_crouching, game_state.player2.is_player_in_move, game_state.player2.move_id,
            game_state.player2.player_buttons.up, game_state.player2.player_buttons.down,
            game_state.player2.player_buttons.right, game_state.player2.player_buttons.left,
            game_state.player2.player_buttons.Y, game_state.player2.player_buttons.B,
            game_state.player2.player_buttons.X, game_state.player2.player_buttons.A,
            game_state.player2.player_buttons.L, game_state.player2.player_buttons.R
        ]
        with open(self.filename, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)


def connect(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    client_socket, _ = server_socket.accept()
    print("Connected to game!")
    return client_socket


def send(client_socket, command):
    payload = json.dumps(command.object_to_dict()).encode()
    client_socket.sendall(payload)


def receive(client_socket):
    data = client_socket.recv(4096)
    return GameState(json.loads(data.decode()))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['1','2']:
        print("Usage: python controller.py [1|2]")
        sys.exit(1)
    port = 9999 if sys.argv[1] == '1' else 10000
    client_socket = connect(port)

    bot = Bot()
    logger = DataLogger(LOG_FILE)

    current_state = None
    while current_state is None or not current_state.is_round_over:
        current_state = receive(client_socket)
        cmd = bot.fight(current_state, sys.argv[1])
        # log before sending to capture the state and selected action
        logger.log(current_state, cmd)
        send(client_socket, cmd)

    print(f"Round finished. Data logged to {LOG_FILE}.")

if __name__ == '__main__':
    main()
