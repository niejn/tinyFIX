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

class FixServer:
    def __init__(self):
        self.fixSession = FixSession()
        self.execId = 0

    def initialiseSession(self, port, compId):
        self.fixSession.fixTransport.targetPort = port
        self.fixSession.senderCompid = compId
        self.fixSession.server = True
        
    def start(self, port, compId):
        self.initialiseSession(port, compId)
        return self.fixSession.accept(None)

    def startWithCustomLogonResponse(self, port, customLogonResponse):
        if customLogonResponse.hasTag(FixConstants.TAG_SENDER_COMPID) == false:
            raise Exception("You have to specify sender comp id tag in a custom logon response message")
        compId = customLogonResponse.getTagValue(FixConstants.TAG_SENDER_COMPID)
        self.initialiseSession(port, compId)
        customLogonResponse.removeTag(FixConstants.TAG_SENDER_COMPID)
        return self.fixSession.accept(customLogonResponse)

    def disconnect(self, logOffResponse = None):
        self.fixSession.disconnect(logOffResponse)
        
    def send(self, fixMessage, sendExecutionId=False):
        if sendExecutionId is True:
            fixMessage.setTag(FixConstants.TAG_EXEC_ID, self.execId)
        return self.fixSession.send(fixMessage)
        
    def recv(self):
        message = self.fixSession.recv()
        self.fixSession.saveSequenceNumberToFile()
        return message