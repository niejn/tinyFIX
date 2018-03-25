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
from FixSession import FixSession
import time

class FixClient:
    def __init__(self):
        self.orderId = 0
        self.fixSession = FixSession()

    HEARTBEAT_INTERVAL_DEFAULT = 30
    ENCRYPTION_METHOD_DEFAULT = 0

    def connect(self, address, port, fixVersion, compId, targetCompid, heartbeatInterval=HEARTBEAT_INTERVAL_DEFAULT, encryptionMethod=ENCRYPTION_METHOD_DEFAULT):
        self.fixSession.fixTransport.targetAddress = address
        self.fixSession.fixTransport.targetPort = port
        self.fixSession.fixVersion = fixVersion
        self.fixSession.senderCompid = compId
        self.fixSession.targetCompid = targetCompid
        self.fixSession.heartbeatInterval = heartbeatInterval
        self.fixSession.encryptionMethod = encryptionMethod
        return self.fixSession.connect(None)

    def connectWithCustomLogonMessage(self, adress, port, logOnMessage):
        self.fixSession.targetAddress = address
        self.fixSession.targetPort = port

        mandatoryTags = [FixConstants.TAG_VERSION, FixConstants.TAG_SENDER_COMPID, FixConstants.TAG_TARGET_COMPID]

        if logOnMessage.hasTags(mandatoryTags) == False:
            raise Exception("You have to specify fix version, sender compid and target compid in a custom logon message ")

        self.fixSession.fixVersion = logOnMessage.getTagValue(FixConstants.TAG_VERSION)
        self.fixSession.senderCompid = logOnMessage.getTagValue(FixConstants.TAG_SENDER_COMPID)
        self.fixSession.targetCompid = logOnMessage.getTagValue(FixConstants.TAG_TARGET_COMPID)

        logOnMessage.removeTags(mandatoryTags)

        if logOnMessage.hasTag(FixConstants.TAG_HEARTBEAT_INTERVAL):
            self.fixSession.heartbeatInterval = logOnMessage.getTagValue(FixConstants.TAG_HEARTBEAT_INTERVAL)
        else:
            self.fixSession.heartbeatInterval = FixClient.HEARTBEAT_INTERVAL_DEFAULT

        if logOnMessage.hasTag(FixConstants.TAG_ENCRYPT_METHOD):
            self.fixSession.encryptionMethod = logOnMessage.getTagValue(FixConstants.TAG_ENCRYPT_METHOD)
        else:
            self.fixSession.encryptionMethod = FixClient.HEARTBEAT_INTERVAL_DEFAULT

        return self.fixSession.connect(logOnMessage)

    def disconnect(self, logOffMessage = None):
        self.fixSession.disconnect(logOffMessage)

    def recv(self):
        return self.fixSession.recv()

    def send(self, fixMessage, sendClientOrderId=True, timeoutSeconds=0):
        if sendClientOrderId is True:
            self.orderId += 1
            fixMessage.setTag(FixConstants.TAG_CLIENT_ORDER_ID, self.orderId)
        ret = False
        
        def getTimeInSeconds():
            return int(round(time.time()))
        
        trialStart = getTimeInSeconds()
        while True:
            ret = self.fixSession.send(fixMessage)
            if ret is True:
                break
                
            if timeoutSeconds > 0:
                deltaTime = getTimeInSeconds() - trialStart
                if deltaTime >= timeoutSeconds:
                    break
            else:
                break
            
        return ret