#!/usr/bin/python
import socket
import sys
import os

CONNECTION_TIMEOUT = 10

def displayHelp():
    print ( "Usage : python ./tcp_proxy.py <from_address> <from_port> <to_address> <to_port>")
    return

class TCPProxy:
    def __init__(self):
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connector.setblocking(True)
        self.connector.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.acceptor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.acceptor.setblocking(True)
        self.acceptor.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.transportSize = 1024

    def __del__(self):
        self.connector.close()
        self.acceptor.close()
        
    def start(self, acceptorAddress, acceptorPort, connectorAddress, connectorPort):
        # Acceptor accepts a connection from the client
        self.acceptor.bind( (acceptorAddress, acceptorPort))
        self.acceptor.listen(100)
        self.acceptor.settimeout(CONNECTION_TIMEOUT)
        clientSocket, clientAdress = self.acceptor.accept()

        # Connector connect to the server
        self.connector.settimeout(CONNECTION_TIMEOUT)
        self.connector.connect((connectorAddress, connectorPort))
        
        # Turn blocking on
        self.connector.setblocking(1)
        clientSocket.setblocking(1)
        
        try:
            while True:
                # Receive from the client
                request = clientSocket.recv(self.transportSize)

                if len(request) > 0 :
                    print("Client -> server : " + request + "\n" )
                    # Transmit it to the server
                    self.connector.send(request)

                # Receive response from server
                response = self.connector.recv(self.transportSize)

                if len(response) > 0:
                    print("Server -> client : " + response + "\n" )
                    # Transmit it to the client
                    clientSocket.send(response)
                    
                # IS IT A FIX LOGOFF
                if "35=5" in response:
                    self.acceptor.close()
                    self.connector.close()
                    clientSocket.close()
                    return
        except Exception as e :
            print(str(e) + "\n")

try:
    if len(sys.argv) < 5:
        displayHelp()
        os._exit(1)
    tcpProxy = TCPProxy()
    print("TCP Proxy is starting. Will timeout in " + str(CONNECTION_TIMEOUT) + " seconds if no connections established" + "\n")
    tcpProxy.start(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
    os._exit(0)
except Exception as e :
    print(str(e))