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
    # VERSIONS
    FIX_VERSION_4_0 = "FIX.4.0"
    FIX_VERSION_4_1 = "FIX.4.1"
    FIX_VERSION_4_2 = "FIX.4.2"
    FIX_VERSION_4_3 = "FIX.4.3"
    FIX_VERSION_4_4 = "FIX.4.4"
    FIX_VERSION_5_0 = "FIX.5.0"
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
    
# Can not use enums as supporting Python2.7 , they are added in 3.4
class FixTime:
    FIX_SECONDS=1
    FIX_MILLISECONDS=2
    FIX_MICROSECONDS=3
    
    @staticmethod
    def getCurrentUTCDateTimeSeconds():
        retVal = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S")
        return retVal

    @staticmethod
    def getCurrentUTCDateTimeMilliSeconds():
        retVal = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3]
        return retVal
        
    @staticmethod
    def getCurrentUTCDateTimeMicroSeconds():
        retVal = datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")
        return retVal

class FixMessage:
    def __init__(self):
        self.tagValuePairs = [] # Array of tuples
        self.timePrecision = FixTime.FIX_MILLISECONDS
        
    def getCurrentUTCDateTime(self):
        if self.timePrecision == FixTime.FIX_MICROSECONDS:
            return FixTime.getCurrentUTCDateTimeMicroSeconds()
        if self.timePrecision == FixTime.FIX_MILLISECONDS:
            return FixTime.getCurrentUTCDateTimeMilliSeconds()
        return FixTime.getCurrentUTCDateTimeSeconds()

    def setFixVersion(self, fixVersion):
        self.setTag(FixConstants.FIX_TAG_VERSION, fixVersion)
        
    def setTimePrecision(self, precision):
        self.timePrecision = precision

    def hasTag(self, tag):
        for tagValuePair in self.tagValuePairs:
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                return True
        return False

    # Index and count use for supporting repeating groups
    def getTagValue(self, tag, index=1):
        count = 0
        for tagValuePair in self.tagValuePairs:
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                count = count + 1
                if count == index:
                    return currentValue
        return None

    def setTag(self, tag, value):
        self.tagValuePairs.append( tuple((tag, str(value))) )
        
    def setTags(self , tagValueTuple):
        for tagValuePair in tagValueTuple:
            tag, value = tagValuePair
            self.setTag(tag, value)

    def getMessageType(self):
        return self.getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE)

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
        for tagValue in self.tagValuePairs:
            tag , value = tagValue
            if tag is FixConstants.FIX_TAG_VERSION:
                continue
            if tag is FixConstants.FIX_TAG_BODY_LENGTH:
                continue
            if tag is FixConstants.FIX_TAG_BODY_CHECKSUM:
                continue
            bodyLength += len(str(tag)) + len( str(value) ) + 2 # +2 is because of = and delimiter
        return bodyLength
        
    @staticmethod
    def isBodyTag(tag):
        if tag is FixConstants.FIX_TAG_VERSION:
            return False
        if tag is FixConstants.FIX_TAG_BODY_LENGTH:
            return False
        if tag is FixConstants.FIX_TAG_MESSAGE_TYPE:
            return False
        if tag is FixConstants.FIX_TAG_SEQUENCE_NUMBER:
            return False
        if tag is FixConstants.FIX_TAG_SENDING_TIME:
            return False
        if tag is FixConstants.FIX_TAG_SENDER_COMPID:
            return False
        if tag is FixConstants.FIX_TAG_SENDER_SUBID:
            return False
        if tag is FixConstants.FIX_TAG_TARGET_COMPID:
            return False
        if tag is FixConstants.FIX_TAG_TARGET_SUBID:
            return False
        if tag is FixConstants.FIX_TAG_BODY_CHECKSUM:
            return False
        return True

    def toString(self, sendingAsMessage = False, updateTransactionTime = False):
        # If it was Python3 could use a non local variable instead making string a mutable array
        messageAsString = [""]
        
        def appendToMessageAsString(tag, value = ""):
            if len(value) == 0:
                value = self.getTagValue(tag)
            messageAsString[0] += str(tag) + FixConstants.FIX_EQUALS + value
            messageAsString[0] += FixConstants.FIX_DELIMITER
        
        # FIX VERSION
        appendToMessageAsString(FixConstants.FIX_TAG_VERSION)

        # FIX SENDING TIME AND TRANSACTION, have to be before body length calculation ,but not appended for the correct order
        if sendingAsMessage is True:
            currentUTCDateTime = self.getCurrentUTCDateTime()
            self.setTag(FixConstants.FIX_TAG_SENDING_TIME, currentUTCDateTime)
            if updateTransactionTime is True:

                if self.isAdminMessage() is False:
                    self.setTag(FixConstants.FIX_TAG_TRANSACTION_TIME, currentUTCDateTime)

        # FIX BODY LENGTH
        if sendingAsMessage is True:
            bodyLength = str(self.calculateBodyLength())
            appendToMessageAsString(FixConstants.FIX_TAG_BODY_LENGTH, bodyLength)
        else:
            if self.hasTag(FixConstants.FIX_TAG_BODY_LENGTH):
                appendToMessageAsString(FixConstants.FIX_TAG_BODY_LENGTH)

        # FIX MESSAGE TYPE
        appendToMessageAsString(FixConstants.FIX_TAG_MESSAGE_TYPE)

        # FIX SEQUENCE NUMBER
        appendToMessageAsString(FixConstants.FIX_TAG_SEQUENCE_NUMBER)

        # FIX SENDER COMPID
        appendToMessageAsString(FixConstants.FIX_TAG_SENDER_COMPID)

        # FIX SENDER SUBID
        if self.hasTag(FixConstants.FIX_TAG_SENDER_SUBID):
            appendToMessageAsString(FixConstants.FIX_TAG_SENDER_SUBID)

        # FIX SENDING TIME
        appendToMessageAsString(FixConstants.FIX_TAG_SENDING_TIME)

        # FIX TARGET COMPID
        appendToMessageAsString(FixConstants.FIX_TAG_TARGET_COMPID)
        
        # FIX TARGET SUBID
        if self.hasTag(FixConstants.FIX_TAG_TARGET_SUBID):
            appendToMessageAsString(FixConstants.FIX_TAG_TARGET_SUBID)

        for tagValue in self.tagValuePairs:
            tag, value = tagValue
            if FixMessage.isBodyTag(tag) is False:
                continue
            appendToMessageAsString(tag)

        # FIX CHECKSUM
        if sendingAsMessage is True:
            checksumValue = FixMessage.calculateChecksum(messageAsString[0])
            appendToMessageAsString(FixConstants.FIX_TAG_BODY_CHECKSUM, checksumValue)
        else:
            if self.hasTag(FixConstants.FIX_TAG_BODY_CHECKSUM):
                appendToMessageAsString(FixConstants.FIX_TAG_BODY_CHECKSUM)

        return messageAsString[0]

class FixSession:
    def __init__(self):
        self.connected = False
        self.restoreSequenceNumberFromFile = False
        self.targetAddress = ""
        self.targetPort = 0
        self.heartbeatInterval = 30
        self.encryptionMethod = FixConstants.FIX_ENCRYPTION_NONE
        self.incomingSequenceNumber = 1
        self.outgoingSequenceNumber = 1
        self.fixVersion = ""
        self.senderCompid = ""
        self.senderSubid = ""
        self.targetCompid = ""
        self.targetSubid = ""
        self.timePrecision = FixTime.FIX_MILLISECONDS
        self.networkTimeoutInSeconds = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(True)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(True)
        self.serverSocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.heartbeatTimer = None
        self.mutex = Lock()
        
    def setUseSequenceNumberFile(self, value):
        self.restoreSequenceNumberFromFile = value
        
    def setNetworkTimeoutInSeconds(self, timeout):
        self.networkTimeoutInSeconds = timeout
        
    def setTimePrecision(self, precision):
        self.timePrecision = precision

    def getBaseMessage(self, messageType):
        message = FixMessage()
        message.setFixVersion(self.fixVersion)
        message.setTimePrecision(self.timePrecision)
        message.setTag(FixConstants.FIX_TAG_MESSAGE_TYPE, messageType)
        # Sequence number will be added during send call
        message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, self.senderCompid)
        if len(self.senderSubid) > 0:
            message.setTag(FixConstants.FIX_TAG_SENDER_SUBID, self.senderSubid)
        message.setTag(FixConstants.FIX_TAG_SENDING_TIME, "")
        message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, self.targetCompid)
        if len(self.targetSubid) > 0:
            message.setTag(FixConstants.FIX_TAG_TARGET_SUBID, self.targetSubid)
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
        ret = (self.senderCompid) + "_" + (self.targetCompid) + "_sequence.txt"
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
        try:
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
        except:
            print("Warning : Error during opening sequence number file , sequence numbers set to 1")

        self.incomingSequenceNumber = incomingNumber
        self.outgoingSequenceNumber = outgoingNumber

    def connect(self, logonMessage):
        message = None
        # Not supporting timeouts in accept and connect methods
        originalTimeoutInSeconds = self.networkTimeoutInSeconds
        self.networkTimeoutInSeconds = 0
        try:
            self.socket.connect((self.targetAddress, self.targetPort))

            if self.restoreSequenceNumberFromFile is True:
                self.restoreSequenceNumber()

            if logonMessage is None:
                logonMessage = self.getLogonMessage()
            
            self.send(logonMessage)
            message = self.recv()

            if message.getMessageType() != FixConstants.FIX_MESSAGE_LOG_ON:
                raise Exception("Incoming message was not a logon response")            
            
            if self.restoreSequenceNumberFromFile is False:
                self.incomingSequenceNumber = int( message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER) )
                
            self.heartbeatTimer = threading.Timer(self.heartbeatInterval, self.heartbeatFunction)
            self.heartbeatTimer.start()
            
            self.connected = True
        except Exception as e:
            exceptionMessage = "Error during a connection attempt : "
            exceptionMessage += str(e)
            if message != None:
                exceptionMessage += "\n"
                exceptionMessage += message.toString()
            print(exceptionMessage)
        self.networkTimeoutInSeconds = originalTimeoutInSeconds
        return  self.connected
        
    def accept(self, logOnResponse):
        message = None
        # Not supporting timeouts in accept and connect methods
        originalTimeoutInSeconds = self.networkTimeoutInSeconds
        self.networkTimeoutInSeconds = 0
            
        try:
            self.serverSocket.bind( (self.targetAddress, self.targetPort))
            self.serverSocket.listen(100)
            self.socket, address = self.serverSocket.accept()
            
            message = self.recv()

            if message.getMessageType() != FixConstants.FIX_MESSAGE_LOG_ON:
                raise Exception("Incoming message was not a logon message")                
                
            if self.restoreSequenceNumberFromFile is False:
                self.incomingSequenceNumber = int( message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER) )
            else:
                self.restoreSequenceNumber()
                
            self.heartbeatInterval = int( message.getTagValue(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL) )
            self.targetCompid = message.getTagValue(FixConstants.FIX_TAG_SENDER_COMPID)
            
            if message.hasTag(FixConstants.FIX_TAG_SENDER_SUBID):
                self.targetSubId = message.getTagValue(FixConstants.FIX_TAG_SENDER_SUBID)
            
            self.fixVersion = message.getTagValue(FixConstants.FIX_TAG_VERSION)
            
            if message.hasTag(FixConstants.FIX_TAG_ENCRYPT_METHOD):
                self.encryptionMethod = int( message.getTagValue(FixConstants.FIX_TAG_ENCRYPT_METHOD) )
            
            if logOnResponse is None:
                logOnResponse = self.getLogonMessage()
            
            self.send(logOnResponse)
            
            self.connected = True                            
        except Exception as e:
            exceptionMessage = "Error during a connection attempt : "
            exceptionMessage += str(e)
            if message != None:
                exceptionMessage += "\n"
                exceptionMessage += message.toString()
            print(exceptionMessage)
        self.networkTimeoutInSeconds = originalTimeoutInSeconds
        return  self.connected

    def heartbeatFunction(self):
        self.send(self.getHeartbeatMessage())

    def disconnect(self, logoffMessage = None):
        if self.connected:
            if self.heartbeatTimer:
                self.heartbeatTimer.cancel()
            try:
                if logoffMessage is None:
                    logoffMessage = self.getLogoffMessage()
                self.send(logoffMessage)
                logoffResponse = self.recv()
                print("Disconnected : " + logoffResponse.toString())
                self.serverSocket.close()
                self.socket.close()
            except:
                pass
            self.connected = False
            self.saveSequenceNumberToFile()
            
    def enableSocketBlocking(self):
        self.socket.settimeout(None) # Put socket back into blocking mode
        
    def arrangeSocketTimeOut(self):
        if self.networkTimeoutInSeconds > 0:
            self.socket.settimeout(self.networkTimeoutInSeconds)

    def send(self, message):
        message.setTag(FixConstants.FIX_TAG_VERSION, self.fixVersion)
        message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, self.senderCompid)
        message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, self.targetCompid)
        
        self.mutex.acquire()
        
        self.arrangeSocketTimeOut()
        message.setTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER, self.outgoingSequenceNumber)
        sentBytes = 0
        
        try:
            sentBytes = self.socket.send( message.toString(True, True))
            if sentBytes > 0:
                self.outgoingSequenceNumber += 1
        except socket.timeout:
            sentBytes = 0
        
        self.enableSocketBlocking() # Put socket back into blocking mode
        
        self.mutex.release()
        
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
        self.mutex.acquire()
        self.arrangeSocketTimeOut()
        message = None
        try:
            initialBuffer = self.recvString(20) # Length of 8=FIX.4.2@9=7000@35= so we always get 35=A

            if initialBuffer is None:
                raise Exception("Receive failed")

            if len(initialBuffer) is 0:
                raise Exception("Receive failed")

            # Find all bytes from tag body length
            allBytes = int ( initialBuffer.split(FixConstants.FIX_DELIMITER)[1].split(FixConstants.FIX_EQUALS)[1] )
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

            self.incomingSequenceNumber = int(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER))
        except Exception as e:
            pass
        
        self.enableSocketBlocking() # Put socket back into blocking mode # Put socket back into blocking mode
        self.mutex.release()
        return  message

class FixClient:
    def __init__(self):
        self.orderId = 0
        self.fixSession = FixSession()

    def initialise(self, fixVersion, address, port, compId, subId, targetCompid, targetSubId, heartbeatInterval=30, encryptionMethod=0):
        self.fixSession.fixVersion = fixVersion
        self.fixSession.targetAddress = address
        self.fixSession.targetPort = port
        self.fixSession.senderCompid = compId
        self.fixSession.senderSubid = subId
        self.fixSession.targetCompid = targetCompid
        self.fixSession.targetSubId = targetSubId
        self.fixSession.heartbeatInterval = heartbeatInterval
        self.fixSession.encryptionMethod = encryptionMethod

    def connect(self, logOnMessage = None):
        return self.fixSession.connect(logOnMessage)

    def disconnect(self, logOffMessage = None):
        self.fixSession.disconnect(logOffMessage)

    def recv(self):
        return self.fixSession.recv()

    def send(self, fixMessage):
        self.orderId += 1
        fixMessage.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, self.orderId)
        return self.fixSession.send(fixMessage)
        
class FixServer:
    def __init__(self):
        self.fixSession = FixSession()
        
    def start(self, port, compId, subId, logOnResponse = None):
        self.fixSession.targetPort = port
        self.fixSession.senderCompid = compId
        self.fixSession.senderSubid = subId
        return self.fixSession.accept(logOnResponse)

    def disconnect(self, logOffResponse = None):
        self.fixSession.disconnect(logOffResponse)
        
    def send(self, fixMessage):
        return self.fixSession.send(fixMessage)
        
    def recv(self):
        message = self.fixSession.recv()
        self.fixSession.saveSequenceNumberToFile()
        return message