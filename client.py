# client.py

from socket import socket

class Client:
    '''
    Class for holding details on the clients (agents) connected to the server.
    Provides the socket and address, as well as information on whether the connection is an MTC Agent, if it has recently connected, and if the connection is active.
    '''
    def __init__(self, conn, addr, server):

        self.HEADER = server.HEADER
        self.FORMAT = server.FORMAT
        self.MSGLENGTH: int = server.MSGLENGTH

        self.hostServer = server

        self.addr = addr
        self.ipAddr = addr[0]
        self.port = addr[1]
        self.cleanAddr = str(addr[0]) + ':' + str(addr[1])

        self.conn: socket = conn

        self.agent: bool = False
        self.connected = False
        self.new_connection = True

    def close_connection(self):
        self.conn.close()
        self.connected = False
        self.hostServer.active_connections.remove(self)


