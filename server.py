# server.py

import socket
import threading
import time

class Server:
    def __init__(self, port: int, ipAddress: str):
        self.HEADER = 64
        self.PORT = port
        self.SERVER = ipAddress
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.MSGLENGTH: int = 1024

        self.HEARTBEAT_RECIEVE_MSG: str = "* PING"
        self.HEARTBEAT_SEND_MSG: str = "* PONG"
        self.HEARTBEAT_FREQUENCY: str = '10000'

        self.socket: socket.socket = self.create_socket(self.ADDR)

        self.active_connections: list(socket.socket) = []

    def create_socket(self, ADDR):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(ADDR)
        return sock

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        timeout = (int(self.HEARTBEAT_FREQUENCY) / 1000) * 2
        conn.settimeout(timeout)

        t = threading.Thread(target=self.send_pong, args=(conn))
        t.start()

        connected = True
        while connected:
            try:
                msg = conn.recv(self.MSGLENGTH)
                msg = msg.decode(self.FORMAT, errors='ignore')
                # if msg != "* PING":
                #     print("[DISCONNECTED]: Adapter received unexpected response from agent. Closing connection.")
                #     self.active_connections.remove(conn)
                #     connected - False
                if msg == self.DISCONNECT_MESSAGE:
                    print(f"[DISCONNECTED]: Closing connection to {addr}")
                    self.active_connections.remove(conn)
                    connected = False
                else:
                    print(f"[{addr}] {msg}")

                ### * If messages from the agent are sent with a header of specified length
                # msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                # if msg_length:
                #     msg_length = int(msg_length)
                #     msg = conn.recv(msg_length).decode(self.FORMAT)
                #     if msg == self.DISCONNECT_MESSAGE:
                #         connected = False
                #     print(f"[{addr}] {msg}")
                ### *
            except socket.timeout:
                conn.close()
                self.active_connections.remove(conn)
                print(f"[DISCONNECTED] Server did not receive a response from {addr}. Closing connection.")

    def send_pong(self, conn):
        for conn in self.active_connections:
            pong_msg = str(self.HEARTBEAT_SEND_MSG).encode(self.FORMAT)
            conn.send(pong_msg)
            time.sleep(10)


    def send(self, msg: str):
        data_message = msg.encode(self.FORMAT)

        for conn in self.active_connections:
            conn.send(data_message)

        ### If the message to the agent requires a header of a specified length
        # msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        # send_length += b' ' * (self.HEADER - len(send_length))
        # self.socket.send(send_length)
        ###


    def start(self):
        print("[STARTING] server is starting...")
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        self.socket.listen()
        while True:
            [conn, addr] = self.socket.accept()
            connect_msg = str(self.HEARTBEAT_SEND_MSG + ' ' + self.HEARTBEAT_FREQUENCY).encode(self.FORMAT)
            conn.send(connect_msg)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            self.active_connections.append(conn)
            print(f"[ACTIVE CONNECTIONS] {len(self.active_connections)}")