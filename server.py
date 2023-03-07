# server.py

import logging
import socket
import threading
import time
from client import Client

class Server:
    '''
     This class manages the sending of data to connected agents as well as the receiving and logging of information sent to the adapter
    '''
    def __init__(self, port: int, ipAddress: str):
        '''
        Constructs a server object.
        
        Args:
            port: int 
                port that the adapter data will be sent from
            ipAddress: str
                IP Address that adapter is located at
        '''
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.MSGLENGTH: int = 1024

        self.PORT = port
        self.SERVER = ipAddress
        self.ADDR = (self.SERVER, self.PORT)

        self.HEARTBEAT_RECIEVE_MSG: str = "* PING\n"
        self.HEARTBEAT_SEND_MSG: str = "* PONG"
        self.HEARTBEAT_FREQUENCY: str = '10000'

        self.socket: socket = self.create_socket(self.ADDR)

        self.active_connections: list = []

        self.logger = logging.getLogger("adapterLog")

    def create_socket(self, ADDR: tuple) -> (socket.socket):
        """
        Creates a socket object at the specified address

        Args:
            ADDR (tuple): ip address and port number

        Returns:
            socket: socket connection at specified address
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(ADDR)
            return sock
        except socket.error as e:
            self.logger.warn

    def handle_client(self, client: Client):
        
        # Sets the timeout counter for the socket to 2x the heartbeat frequency
        timeout = (int(self.HEARTBEAT_FREQUENCY) / 1000) * 2
        client.conn.settimeout(timeout)

        # Begins a thread for continually sending 'pong' to maintain connection with agent
        t = threading.Thread(target=self.send_pong, args=([client]))
        t.start()

        # Loops while the connection is established and records messages sent by the clients. Handles connection and timeout errors.
        while client.connected:
            try:
                msg = client.conn.recv(self.MSGLENGTH)
                msg = msg.decode(self.FORMAT, errors='ignore')
                if msg == self.DISCONNECT_MESSAGE:
                    client.close_connection()
                    print(f"[DISCONNECTED]: Closing connection to {client.cleanAddr}")
                else:
                    if msg:
                        print(f"[{client.cleanAddr}]->[SERVER]: {msg}")

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
                client.close_connection()
                print(f"[DISCONNECTED] Server did not receive a response from {client.cleanAddr}. Closing connection.")
                # client.conn.close()
                # client.connected = False
                # self.active_connections.remove(client)

            except ConnectionError as e:
                if e.errno == 10053:
                    client.close_connection()
                    print(f"[DISCONNECTED] Connection to {client.cleanAddr} was aborted")
                    # client.conn.close()
                    # client.connected = False
                    # self.active_connections.remove(client)
        del client
        t.join()

    def send_pong(self, client: Client):
        connect_msg = str(self.HEARTBEAT_SEND_MSG + ' ' + self.HEARTBEAT_FREQUENCY)
        connect_msg_enc = str(connect_msg + '\n').encode(self.FORMAT)
        pong_msg = str(self.HEARTBEAT_SEND_MSG)
        pong_msg_enc = str(pong_msg + '\n').encode(self.FORMAT)

        sleep_time = int(self.HEARTBEAT_FREQUENCY)/1000

        while client in self.active_connections:
            if client.new_connection:
                client.conn.send(connect_msg_enc)
                print(f"[SERVER]->[{client.cleanAddr}]: {connect_msg}")
            else:
                client.conn.send(pong_msg_enc)
                print(f"[SERVER]->[{client.cleanAddr}]: {pong_msg}")
            time.sleep(sleep_time)

    def initial_send(self, msg:str, client: Client):
        time.sleep(1)
        client.new_connection = False
        self.send(msg)

    def send(self, msg: str):
        data_message = msg.encode(self.FORMAT)  # Message sent from the adapter to the server
        # Sends the data to all of the connected clients (agents)
        for client in self.active_connections:
            # TODO: Should probably find a better way of doing this
            if client.new_connection:   # Delays the initial send, otherwise the adapter sends to the agent before it is ready
                t = threading.Thread(target=self.initial_send, args=([msg, client]))    # Creates a thread so the delay in sending to new connections does not hold up other clients in the active connections list
                t.start()
                t.join()
            else:
                client.conn.send(data_message)
                print(f"[SERVER]->[{client.cleanAddr}]: {data_message.decode(self.FORMAT)}")

        ### If the message to the agent requires a header of a specified length
        # msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        # send_length += b' ' * (self.HEADER - len(send_length))
        # self.socket.send(send_length)
        ###
    
    def identify_agent(self, client: Client, ping: str):
        """
        Checks the response message sent back from the client. Determines whether it is an MTC Agent.
        """
        if ping == self.HEARTBEAT_RECIEVE_MSG:
            client.agent = True
            print(f"[{client.cleanAddr}]->[SERVER]: {ping}")
            print(f"[NEW CONNECTION] MTC Agent at {client.ipAddr} connected.")
            self.form_connection(client)
        elif ping:
            client.agent = False
            print(f"[{client.cleanAddr}]->[SERVER]: {ping}")
            print(f"[NEW CONNECTION] MTC Agent at {client.ipAddr} connected.")
            self.form_connection(client)

    def form_connection(self, client: Client):
        """
        Establishes the connection with the client and updates the list of connections.
        """
        # connect_msg = str(self.HEARTBEAT_SEND_MSG + ' ' + self.HEARTBEAT_FREQUENCY).encode(self.FORMAT)
        # client.conn.send(connect_msg)
        # print(f"[SERVER]->{client.cleanAddr}: {connect_msg.decode(self.FORMAT)}")
        client.connected = True
        thread = threading.Thread(target=self.handle_client, args=([client]))
        thread.start()
        self.active_connections.append(client)
        print(f"[ACTIVE CONNECTIONS] {len(self.active_connections)}")

    def start(self):
        """
        Starts the adapter "server" to begin watching for connections and begins a thread for any new connection
        """
        print("[STARTING] Server is starting...")
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        self.socket.listen()
        while True:
            [conn, addr] = self.socket.accept()
            connection = Client(conn, addr, self)
            ping = conn.recv(self.MSGLENGTH).decode(self.FORMAT, errors='ignore') # Figure out a way to handle messages that are received not in utf-8 format
            self.identify_agent(connection, ping)



