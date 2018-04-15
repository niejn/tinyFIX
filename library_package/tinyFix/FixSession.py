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
from FixTcpTransport import FixTcpTransport
from threading import Lock
import threading
import os.path
from datetime import datetime

class FixSession:
    def __init__(self):
        self.connected = False
        self.server = False
        self.restoreSequenceNumberFromFile = False
        self.incomingSequenceNumber = 1
        self.incomingSequenceNumber = 1
        self.heartbeatInterval = 30                                 #Required for logon message
        self.encryptionMethod = FixConstants.ENCRYPTION_NONE    #Required for logon message
        self.fixVersion = ""                                        #Required for every message
        self.senderCompid = ""                                      #Required for every message
        self.targetCompid = ""                                      #Required for every message
        self.additionalHeaderTagValuePairs = [] # Array of tuples, will be applied to each message for ex senderSubId & targetSubId
        self.timePrecision = FixConstants.TIMESTAMP_PRECISION_MILLISECONDS
        self.fixTransport = FixTcpTransport()
        self.heartbeatTimer = None
        self.mutex = Lock()

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
        
    def getCurrentUTCDateTime(self):
        if self.timePrecision == FixConstants.TIMESTAMP_PRECISION_MICROSECONDS:
            return FixSession.getCurrentUTCDateTimeMicroSeconds()
        if self.timePrecision == FixConstants.TIMESTAMP_PRECISION_MILLISECONDS:
            return FixSession.getCurrentUTCDateTimeMilliSeconds()
        return FixSession.getCurrentUTCDateTimeSeconds()
        
    def setUseSequenceNumberFile(self, value):
        self.restoreSequenceNumberFromFile = value

    def addHeaderTagValuePair(self, tag, value):
        self.additionalHeaderTagValuePairs.append((tag, value))

    def addHeaderTagValuePairs(self, tagValueTupleArray):
        for tagValue in tagValueTupleArray:
            self.additionalHeaderTagValuePairs.append(tagValue)
        
    def setTimePrecision(self, precision):
        self.timePrecision = precision

    def getBaseMessage(self, messageType):
        message = FixMessage()
        message.setTag(FixConstants.TAG_MESSAGE_TYPE, messageType)
        return  message

    def getLogonMessage(self):
        message = self.getBaseMessage(FixConstants.MESSAGE_LOG_ON)
        message.setTag(FixConstants.TAG_ENCRYPT_METHOD, self.encryptionMethod)
        message.setTag(FixConstants.TAG_HEARTBEAT_INTERVAL, self.heartbeatInterval)
        return message

    def getLogoffMessage(self):
        message = self.getBaseMessage(FixConstants.MESSAGE_LOG_OFF)
        return message

    def getHeartbeatMessage(self):
        message = self.getBaseMessage(FixConstants.MESSAGE_HEARTBEAT)
        return message

    def getSequenceFileName(self):
        ret = (self.senderCompid) + "_" + (self.targetCompid) + "_sequence.txt"
        return ret

    def saveSequenceNumberToFile(self):
        fileName = self.getSequenceFileName()
        if os.path.exists(fileName):
            os.remove(fileName)
        with open(fileName, "w") as textFile:
            textFile.write(str(self.incomingSequenceNumber) + "," + str(self.incomingSequenceNumber))

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
        self.incomingSequenceNumber = outgoingNumber

    def connect(self, logonMessage):
        message = None

        try:
            if self.fixTransport.connect() == False:
                return False

            if self.restoreSequenceNumberFromFile is True:
                self.restoreSequenceNumber()

            if logonMessage is None:
                logonMessage = self.getLogonMessage()
            
            self.send(logonMessage)
            message = self.recv()

            if message.getMessageType() != FixConstants.MESSAGE_LOG_ON:
                raise Exception("Incoming message was not a logon response")            
            
            if self.restoreSequenceNumberFromFile is False:
                self.incomingSequenceNumber = int( message.getTagValue(FixConstants.TAG_SEQUENCE_NUMBER) )
                
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

        return  self.connected
        
    def accept(self, logOnResponse):
        message = None
            
        try:
            if self.fixTransport.accept() == False:
                return False
            
            message = self.recv()

            if message.getMessageType() != FixConstants.MESSAGE_LOG_ON:
                raise Exception("Incoming message was not a logon message")                
                
            if self.restoreSequenceNumberFromFile is False:
                self.incomingSequenceNumber = int( message.getTagValue(FixConstants.TAG_SEQUENCE_NUMBER) )
            else:
                self.restoreSequenceNumber()
                
            self.heartbeatInterval = int( message.getTagValue(FixConstants.TAG_HEARTBEAT_INTERVAL) )
            self.targetCompid = message.getTagValue(FixConstants.TAG_SENDER_COMPID)
            
            self.fixVersion = message.getTagValue(FixConstants.TAG_VERSION)
            
            if message.hasTag(FixConstants.TAG_ENCRYPT_METHOD):
                self.encryptionMethod = int( message.getTagValue(FixConstants.TAG_ENCRYPT_METHOD) )

            for bidirectionalTagPair in FixConstants.BIDIRECTIONAL_HEADER_TAGS:
                tag = bidirectionalTagPair[0]
                if tag == FixConstants.TAG_SENDER_COMPID:
                    continue
                correspondingTag = bidirectionalTagPair[1]
                if message.hasTag(tag):
                    value = message.getTagValue(tag)
                    self.addHeaderTagValuePair(correspondingTag, value)
            
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
                if self.server == False:
                    logoffResponse = self.recv()
            except:
                pass
            finally:
                self.fixTransport.close()
            self.connected = False
            self.saveSequenceNumberToFile()

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()

    def send(self, message):
        message.setTag(FixConstants.TAG_VERSION, self.fixVersion)
        message.setTag(FixConstants.TAG_SENDER_COMPID, self.senderCompid)
        message.setTag(FixConstants.TAG_TARGET_COMPID, self.targetCompid)
        message.setTag(FixConstants.TAG_SENDING_TIME, self.getCurrentUTCDateTime())

        #Apply additional session header tag value pairs
        for tagValuePair in self.additionalHeaderTagValuePairs:
            currentTag, currentValue = tagValuePair
            message.setTag(currentTag, currentValue)

        self.lock()
        
        message.setTag(FixConstants.TAG_SEQUENCE_NUMBER, self.incomingSequenceNumber)

        success = self.fixTransport.send( message )

        if success == True:
            self.incomingSequenceNumber += 1
        
        self.unlock()
        
        return success

    def recv(self):
        self.lock()

        message = None
        message = self.fixTransport.recv()

        if message != None:
            self.incomingSequenceNumber = int(message.getTagValue(FixConstants.TAG_SEQUENCE_NUMBER))
        
        self.unlock()
        
        return  message