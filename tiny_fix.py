#!/usr/bin/python
import socket
import os.path
import threading
from threading import Thread, Lock
import time
from datetime import datetime

class FixConstants:
    # GENERAL
    FIX_EQUALS = '='
    FIX_DELIMITER = chr(1)
    # TAGS
    FIX_AVERAGE_PRICE = 6
    FIX_TAG_VERSION = 8
    FIX_TAG_BODY_LENGTH = 9
    FIX_TAG_BODY_CHECKSUM = 10
    FIX_TAG_CLIENT_ORDER_ID = 11
    FIX_TAG_CUMULATIVE_QUANTITY = 14
    FIX_TAG_EXEC_ID = 17
    FIX_TAG_EXEC_INST = 18
    FIX_TAG_EXEC_TRANSTYPE = 20
    FIX_TAG_HAND_INST = 21
    FIX_TAG_LAST_PRICE = 31
    FIX_TAG_LAST_QUANTITY = 32
    FIX_TAG_SEQUENCE_NUMBER = 34
    FIX_TAG_MESSAGE_TYPE = 35
    FIX_TAG_ORDER_ID = 37
    FIX_TAG_ORDER_QUANTITY = 38
    FIX_TAG_ORDER_STATUS = 39
    FIX_TAG_ORDER_TYPE = 40
    FIX_TAG_ORIG_CLIENT_ORDER_ID = 41
    FIX_TAG_ORDER_PRICE = 44
    FIX_TAG_SECURITY_ID = 48
    FIX_TAG_SENDER_COMPID = 49
    FIX_TAG_SENDER_SUBID = 50
    FIX_TAG_SENDING_TIME = 52
    FIX_TAG_ORDER_SIDE = 54
    FIX_TAG_SYMBOL = 55
    FIX_TAG_TARGET_COMPID = 56
    FIX_TAG_TARGET_SUBID = 57
    FIX_TAG_FREE_TEXT = 58
    FIX_TAG_TIME_IN_FORCE = 59
    FIX_TAG_TRANSACTION_TIME = 60
    FIX_TAG_ENCRYPT_METHOD = 98
    FIX_TAG_HEARTBEAT_INTERVAL = 108
    FIX_TAG_TEST_REQ_ID = 112
    FIX_TAG_EXEC_TYPE = 150
    FIX_TAG_LEAVES_QTY = 151
    FIX_TAG_USERNAME = 553
    FIX_TAG_PASSWORD = 554
    FIX_TAG_USER_REQUEST_ID = 923
    FIX_TAG_USER_PASSWORD = 924
    # MESSAGE TYPES
    FIX_MESSAGE_HEARTBEAT = "0"
    FIX_MESSAGE_TEST_REQUEST = "1"
    FIX_MESSAGE_ADMIN_REJECT = "3"
    FIX_MESSAGE_USER_LOGON = "BE"
    FIX_MESSAGE_USER_RESPONSE = "BF"
    FIX_MESSAGE_LOG_ON = "A"
    FIX_MESSAGE_LOG_OFF = "5"
    FIX_MESSAGE_EXECUTION_REPORT = "8"
    FIX_MESSAGE_NEW_ORDER = "D"
    FIX_MESSAGE_AMEND_ORDER = "G"
    FIX_MESSAGE_CANCEL_ORDER = "F"
    FIX_MESSAGE_BUSINES_REJECT = "j"
    # ORDER STATUS
    FIX_ORDER_STATUS_NEW = '0'
    FIX_ORDER_STATUS_PARTIALLY_FILLED = '1'
    FIX_ORDER_STATUS_FILLED = '2'
    FIX_ORDER_STATUS_DONE_FOR_DAY = '3'
    FIX_ORDER_STATUS_CANCELED = '4'
    FIX_ORDER_STATUS_REPLACED = '5'
    FIX_ORDER_STATUS_PENDING_CANCEL = '6'
    FIX_ORDER_STATUS_STOPPED = '7'
    FIX_ORDER_STATUS_REJECTED = '8'
    # ORDER TYPE
    FIX_ORDER_TYPE_MARKET= '1'
    FIX_ORDER_TYPE_LIMIT = '2'
    # SIDE
    FIX_ORDER_SIDE_BUY = '1'
    FIX_ORDER_SIDE_SELL = '2'
    # TIME IN FORCE
    FIX_ORDER_TIF_DAY = '0'
    # ENCRYPTION METHODS
    FIX_ENCRYPTION_NONE = '0'

class FixMessage:
    def __init__(self):
        self.tagValuePairs = dict()
        self.messageAsString = ""

    def appendToMessageAsString(self, tag, value, appendDelimiter=True):
        self.messageAsString += str(tag) + FixConstants.FIX_EQUALS + value
        if appendDelimiter is True:
            self.messageAsString += FixConstants.FIX_DELIMITER

    @staticmethod
    def getCurrentUTCDateTime():
        retVal = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        return retVal

    def setFixVersion(self, fixVersion):
        self.setTag(FixConstants.FIX_TAG_VERSION, fixVersion)

    def hasTag(self, tag):
        if tag in self.tagValuePairs:
            return True
        return False

    def getTagValue(self, tag):
        return self.tagValuePairs[tag]

    def setTag(self, tag, value):
        self.tagValuePairs[tag] = str(value)

    def getMessageType(self):
        return self.tagValuePairs[FixConstants.FIX_TAG_MESSAGE_TYPE]

    def isAdminMessage(self):
        messageType = self.getMessageType()
        if messageType is FixConstants.FIX_MESSAGE_LOG_ON:
            return True
        if messageType is FixConstants.FIX_MESSAGE_LOG_OFF:
            return True
        if messageType is FixConstants.FIX_MESSAGE_HEARTBEAT:
            return True
        return False

    def loadFromString(self, input=""):
        tagValuePairs = input.split(FixConstants.FIX_DELIMITER)
        for tagValuePair in tagValuePairs:
            if len(tagValuePair) < 3:
                continue
            tokens = tagValuePair.split(FixConstants.FIX_EQUALS)
            tag = tokens[0]
            value = tokens[1]
            self.setTag(int(tag), value)

    @staticmethod
    def loadFromFile(fileName):
        fixMessages = []
        with open(fileName, "r") as fileContent:
            for line in fileContent:
                if line.startswith('#') is False:
                    fixMessage = FixMessage()
                    fixMessage.loadFromString(line)
                    fixMessages.append(fixMessage)
        return fixMessages

    @staticmethod
    def calculateChecksum(message):
        checksum = ""
        sum = 0
        for c in message:
            sum += ord(c)
        sum = sum % 256
        checksum = str(sum)
        checksum.zfill(3)
        return checksum

    def calculateBodyLength(self):
        bodyLength = 0
        for tag in self.tagValuePairs:
            if tag is FixConstants.FIX_TAG_VERSION:
                continue
            if tag is FixConstants.FIX_TAG_BODY_LENGTH:
                continue
            if tag is FixConstants.FIX_TAG_BODY_CHECKSUM:
                continue
            bodyLength += len(str(tag)) + len( self.tagValuePairs[tag] ) + 2 # +2 is because of = and delimiter
        return bodyLength

    def toString(self, sendingAsMessage, updateTransactionTime = False):
        self.messageAsString = ""
        # FIX VERSION
        self.appendToMessageAsString(FixConstants.FIX_TAG_VERSION, self.getTagValue(FixConstants.FIX_TAG_VERSION))

        # FIX SENDING TIME AND TRANSACTION, have to be before body length calculation ,but not appended for the correct order
        if sendingAsMessage is True:
            currentUTCDateTime = FixMessage.getCurrentUTCDateTime()
            self.setTag(FixConstants.FIX_TAG_SENDING_TIME, currentUTCDateTime)

            if updateTransactionTime is True:
                if self.isAdminMessage() is False:
                    self.setTag(FixConstants.FIX_TAG_TRANSACTION_TIME, currentUTCDateTime)

        # FIX BODY LENGTH
        if sendingAsMessage is True:
            bodyLength = str(self.calculateBodyLength())
            self.appendToMessageAsString(FixConstants.FIX_TAG_BODY_LENGTH, bodyLength)

        # FIX MESSAGE TYPE
        self.appendToMessageAsString(FixConstants.FIX_TAG_MESSAGE_TYPE, self.getMessageType())

        # FIX SEQUENCE NUMBER
        self.appendToMessageAsString(FixConstants.FIX_TAG_SEQUENCE_NUMBER, self.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER))

        # FIX SENDER COMPID
        self.appendToMessageAsString(FixConstants.FIX_TAG_SENDER_COMPID, self.getTagValue(FixConstants.FIX_TAG_SENDER_COMPID))

        # FIX SENDING TIME
        self.appendToMessageAsString(FixConstants.FIX_TAG_SENDING_TIME, self.getTagValue(FixConstants.FIX_TAG_SENDING_TIME))

        # FIX TARGET COMPID
        self.appendToMessageAsString(FixConstants.FIX_TAG_TARGET_COMPID, self.getTagValue(FixConstants.FIX_TAG_TARGET_COMPID))

        for tag in self.tagValuePairs:
            if tag is FixConstants.FIX_TAG_VERSION:
                continue
            if tag is FixConstants.FIX_TAG_BODY_LENGTH:
                continue
            if tag is FixConstants.FIX_TAG_MESSAGE_TYPE:
                continue
            if tag is FixConstants.FIX_TAG_SEQUENCE_NUMBER:
                continue
            if tag is FixConstants.FIX_TAG_SENDING_TIME:
                continue
            if tag is FixConstants.FIX_TAG_SENDER_COMPID:
                continue
            if tag is FixConstants.FIX_TAG_TARGET_COMPID:
                continue
            if tag is FixConstants.FIX_TAG_BODY_CHECKSUM:
                continue
            self.appendToMessageAsString(tag, self.getTagValue(tag))

        # FIX CHECKSUM
        if sendingAsMessage is True:
            checksumValue = FixMessage.calculateChecksum(self.messageAsString)
            self.appendToMessageAsString(FixConstants.FIX_TAG_BODY_CHECKSUM, checksumValue)

        return self.messageAsString

class FixSession:
    def __init__(self):
        self.connected = False
        self.targetAddress = ""
        self.targetPort = 0
        self.heartbeatInterval = 30
        self.encryptionMethod = FixConstants.FIX_ENCRYPTION_NONE
        self.incomingSequenceNumber = 1
        self.outgoingSequenceNumber = 1
        self.fixVersion = ""
        self.senderCompid = ""
        self.targetCompid = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(True)
        self.serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.heartbeatTimer = None
        self.mutex = Lock()

    def getBaseMessage(self, messageType):
        message = FixMessage()
        message.setFixVersion(self.fixVersion)
        message.setTag(FixConstants.FIX_TAG_MESSAGE_TYPE, messageType)
        # Sequence number will be added during send call
        message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, self.senderCompid)
        message.setTag(FixConstants.FIX_TAG_SENDING_TIME, "")
        message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, self.targetCompid)
        return  message

    def getLogonMessage(self):
        message = self.getBaseMessage(FixConstants.FIX_MESSAGE_LOG_ON)
        message.setTag(FixConstants.FIX_TAG_ENCRYPT_METHOD, self.encryptionMethod)
        message.setTag(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL, self.heartbeatInterval)
        return message

    def getLogoffMessage(self):
        message = self.getBaseMessage(FixConstants.FIX_MESSAGE_LOG_OFF)
        message.setTag(FixConstants.FIX_TAG_ENCRYPT_METHOD, self.encryptionMethod)
        message.setTag(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL, self.heartbeatInterval)
        return message

    def getHeartbeatMessage(self):
        message = self.getBaseMessage(FixConstants.FIX_MESSAGE_HEARTBEAT)
        return message

    def getSequenceFileName(self):
        ret = self.senderCompid + "_" + self.targetCompid + "_sequence.txt"
        return ret

    def saveSequenceNumberToFile(self):
        fileName = self.getSequenceFileName()
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName, "w") as textFile:
            textFile.write(str(self.outgoingSequenceNumber) + "," + str(self.incomingSequenceNumber))

    def restoreSequenceNumber(self):
        incomingNumber = 1
        outgoingNumber = 1
        fileName = self.getSequenceFileName()

        if os.path.exists(fileName):
            with open(fileName, "r") as fileContent:
                line = fileContent.readline()
                outgoingNumberString = line.split(',')[0]
                incomingNumberString = line.split(',')[1]

                if incomingNumberString.isdigit() is True:
                    incomingNumber = int(incomingNumberString)

                if outgoingNumberString.isdigit() is True:
                    outgoingNumber = int(outgoingNumberString)

        self.incomingSequenceNumber = incomingNumber
        self.outgoingSequenceNumber = outgoingNumber

    def connect(self):
        try:
            self.socket.connect((self.targetAddress, self.targetPort))
            self.send(self.getLogonMessage())
            message = self.recv()

            if message is not None:
                if message.hasTag(FixConstants.FIX_TAG_MESSAGE_TYPE):
                    messageType = message.getMessageType()
                    if messageType is FixConstants.FIX_MESSAGE_LOG_ON:
                        if message.hasTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER):
                            self.connected = True
                            self.incomingSequenceNumber = int( message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER) )
                            self.heartbeatTimer = threading.Timer(self.heartbeatInterval, self.heartbeatFunction)
                            self.heartbeatTimer.start()
        except Exception as e:
            print("Socket connection failed %s:%d. Exception is %s" % (self.targetAddress, self.targetPort, e))

        return  self.connected
        
    def accept(self, clientCompId=""):
        try:
            self.serverSocket.bind( (self.targetAddress, self.targetPort))
            self.serverSocket.listen(100)
            self.socket, address = self.serverSocket.accept()
            message = self.recv()

            if message is not None:
                if message.hasTag(FixConstants.FIX_TAG_MESSAGE_TYPE):
                    messageType = message.getMessageType()
                    if messageType is FixConstants.FIX_MESSAGE_LOG_ON:
                        if message.hasTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER):
                            self.connected = True
                            self.incomingSequenceNumber = int( message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER) )
                            self.heartbeatInterval = int( message.getTagValue(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL) )
                            if len(clientCompId) == 0:
                                self.targetCompid = message.getTagValue(FixConstants.FIX_TAG_SENDER_COMPID)
                            else:
                                self.targetCompid = clientCompId
                            self.fixVersion = message.getTagValue(FixConstants.FIX_TAG_VERSION)
                            if message.hasTag(FixConstants.FIX_TAG_ENCRYPT_METHOD):
                                self.encryptionMethod = int( message.getTagValue(FixConstants.FIX_TAG_ENCRYPT_METHOD) )
                            self.send(self.getLogonMessage())
                            
        except Exception as e:
            print("Socket listening failed %s:%d. Exception is %s" % (self.targetAddress, self.targetPort, e))

    def heartbeatFunction(self):
        self.send(self.getHeartbeatMessage())

    def disconnect(self):
        if self.heartbeatTimer:
            self.heartbeatTimer.cancel()
        try:
            self.send(self.getLogoffMessage())
            logoffResponse = self.recv()
            print("Disconnected : " + logoffResponse.toString(False))
            self.serverSocket.close()
        except:
            pass
        self.socket.close()
        self.connected = False
        self.saveSequenceNumberToFile()

    def send(self, message):
        message.setTag(FixConstants.FIX_TAG_VERSION, self.fixVersion)
        message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, self.senderCompid)
        message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, self.targetCompid)
        self.mutex.acquire()
        message.setTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER, self.outgoingSequenceNumber)
        self.socket.send( message.toString(True, True))
        self.outgoingSequenceNumber += 1
        self.mutex.release()
        return

    def recvString(self, size):
        data = ""
        try:
            data = self.socket.recv(size)
        except socket.error:
            data = None
            print "Socket error"
        return data

    def recv(self):
        initialBuffer = self.recvString(20) # Length of 8=FIX.4.2@9=7000@35= so we always get 35=A

        if initialBuffer is None:
            return None

        if len(initialBuffer) is 0:
            return None

        # Find all bytes from tag body length
        allBytes = int ( initialBuffer.split(FixConstants.FIX_DELIMITER)[1].split(FixConstants.FIX_EQUALS)[1] )
        # Calculate remaining bytes
        remainingBytes = allBytes - 20 + initialBuffer.find("35=")
        remainingBytes += 7 #7 is because of 10=081@
        restOfBuffer = self.recvString(remainingBytes)

        message = FixMessage()
        message.loadFromString( initialBuffer + restOfBuffer )

        self.incomingSequenceNumber = int(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER))

        return  message

class FixClient:
    def __init__(self):
        self.orderId = 0
        self.fixSession = FixSession()

    def initialise(self, fixVersion, address, port, compId, targetCompid, heartbeatInterval=30, encryptionMethod=0):
        self.fixSession.fixVersion = fixVersion
        self.fixSession.targetAddress = address
        self.fixSession.targetPort = port
        self.fixSession.senderCompid = compId
        self.fixSession.targetCompid = targetCompid
        self.fixSession.heartbeatInterval = heartbeatInterval
        self.fixSession.encryptionMethod = encryptionMethod
        self.fixSession.restoreSequenceNumber()

    def connect(self):
        self.fixSession.connect()

    def disconnect(self):
        self.fixSession.disconnect()

    def recv(self):
        return self.fixSession.recv()

    def send(self, fixMessage):
        self.orderId += 1
        fixMessage.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, self.orderId)
        self.fixSession.send(fixMessage)
        
class FixServer:
    def __init__(self):
        self.fixSession = FixSession()
        
    def start(self, port, compId, clientcompId):
        self.fixSession.targetPort = port
        self.fixSession.senderCompid = compId
        self.fixSession.restoreSequenceNumber()
        self.fixSession.accept(clientcompId)

    def disconnect(self):
        self.fixSession.disconnect()
        
    def send(self, fixMessage):
        self.fixSession.send(fixMessage)
        
    def recv(self):
        message = self.fixSession.recv()
        self.fixSession.saveSequenceNumberToFile()
        return message