#!/usr/bin/python
'''
Copyright (c) 2018 Akin Ocal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from FixConstants import FixConstants
from FixMessage import FixMessage
import socket

class FixTcpTransport:
    def __init__(self):
        self.networkTimeoutInSeconds = 0
        self.targetAddress = ""
        self.targetPort = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(True)
        self.serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    def setNetworkTimeoutInSeconds(self, timeout):
        self.networkTimeoutInSeconds = timeout

    def connect(self):
        connected = False
        message = None
        self.arrangeSocketTimeOut()
        try:
            while True:
                try:
                    self.socket.connect((self.targetAddress, self.targetPort))
                    connected = True
                    break
                except socket.error, v:
                    errorCode = v[0]
                    if errorCode == 10061: # Remote actively refused it
                        continue
                    raise Exception(v)
        except Exception as e:
            exceptionMessage = "Error during a connection attempt : "
            exceptionMessage += str(e)
            if message != None:
                exceptionMessage += "\n"
                exceptionMessage += message.toString()
            print(exceptionMessage)
        self.enableSocketBlocking()
        return  connected
        
    def accept(self):
        connected = False
        message = None
        
        if self.networkTimeoutInSeconds > 0:
            self.serverSocket.settimeout(self.networkTimeoutInSeconds)
            
        try:
            self.serverSocket.bind( (self.targetAddress, self.targetPort))
            self.serverSocket.listen(100)
            self.socket, address = self.serverSocket.accept()
            connected = True                            
        except Exception as e:
            exceptionMessage = "Error during a connection attempt : "
            exceptionMessage += str(e)
            if message != None:
                exceptionMessage += "\n"
                exceptionMessage += message.toString()
            print(exceptionMessage)
        self.enableSocketBlocking()
        return  connected

    def close(self):
        self.serverSocket.close()
        self.socket.close()
            
    def enableSocketBlocking(self):
        self.socket.settimeout(None) # Put socket back into blocking mode
        
    def arrangeSocketTimeOut(self):
        if self.networkTimeoutInSeconds > 0:
            self.socket.settimeout(self.networkTimeoutInSeconds)

    def send(self, message):
        self.arrangeSocketTimeOut()
        sentBytes = 0
        
        try:
            sentBytes = self.socket.send( message.toString(True) )
        except socket.timeout:
            sentBytes = 0
        
        self.enableSocketBlocking()
        
        return sentBytes > 0

    def recvString(self, size):
        data = ""
        
        try:
            data = self.socket.recv(size)
        except socket.error:
            data = None
            print "Socket error"
        return data

    def recv(self):
        self.arrangeSocketTimeOut()
        message = None
        try:
            initialBuffer = self.recvString(20) # Length of 8=FIX.4.2@9=7000@35= so we always get 35=A

            if initialBuffer is None:
                raise Exception("Receive failed")

            if len(initialBuffer) is 0:
                raise Exception("Receive failed")

            # Find all bytes from tag body length
            allBytes = int ( initialBuffer.split(FixConstants.DELIMITER)[1].split(FixConstants.EQUALS)[1] )
            # Calculate remaining bytes
            remainingBytes = allBytes - 20 + initialBuffer.find("35=")
            remainingBytes += 7 #7 is because of 10=081@
            restOfBuffer = self.recvString(remainingBytes)
            
            if restOfBuffer is None:
                raise Exception("Receive failed")

            if len(restOfBuffer) is 0 and remainingBytes > 0:
                raise Exception("Receive failed")
            
            message = FixMessage()
            message.loadFromString( initialBuffer + restOfBuffer )

        except Exception as e:
            print( "Error during recv : " + str(e))
        
        self.enableSocketBlocking() # Put socket back into blocking mode # Put socket back into blocking mode
        return  message