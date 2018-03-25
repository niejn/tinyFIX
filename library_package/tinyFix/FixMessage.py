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

class FixMessage:
    def __init__(self, tagValueTupleArray=None):
        if tagValueTupleArray:
            self.setTags(tagValueTupleArray)
        self.__tagValuePairs = [] # Array of tuples

    def hasTag(self, tag):
        for tagValuePair in self.__tagValuePairs:
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                return True
        return False

    # Index and count use for supporting repeating groups
    def getTagValue(self, tag, index=1):
        count = 0
        for tagValuePair in self.__tagValuePairs:
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                count = count + 1
                if count == index:
                    return currentValue
        return None

    def setTag(self, tag, value, index=1, addTagIfNotExists=True):
        if self.hasTag(tag) == False:
            if addTagIfNotExists == True:
                self.appendTag(tag, value)
                return
        count = 0
        listIndex = -1
        for tagValuePair in self.__tagValuePairs:
            listIndex = listIndex + 1
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                count = count + 1
                if count == index:
                    self.__tagValuePairs[listIndex] = tuple((tag, str(value)))
                    return

    def appendTag(self, tag, value):
        self.__tagValuePairs.append( tuple((tag, str(value))) )

    def removeTag(self, tag, index = 1):
        if self.hasTag(tag) == False:
            return
        count = 0
        listIndex = -1
        for tagValuePair in self.__tagValuePairs:
            listIndex = listIndex + 1
            currentTag, currentValue = tagValuePair
            if tag == currentTag:
                count = count + 1
                if count == index:
                    del self.__tagValuePairs[listIndex]
                    return
        
    def setTags(self , tagValueTupleArray):
        for tagValuePair in tagValueTupleArray:
            tag, value = tagValuePair
            self.setTag(tag, value)

    def hasTags(self, tagArray):
        for tag in tagArray:
            if self.hasTag(tag) == False:
                return False
        return True

    def removeTags(self, tagArray):
        for tag in tagArray:
            self.removeTag(tag)

    def getMessageType(self):
        return self.getTagValue(FixConstants.TAG_MESSAGE_TYPE)

    def loadFromString(self, input=""):
        tagValuePairs = input.split(FixConstants.DELIMITER)
        for tagValuePair in tagValuePairs:
            if len(tagValuePair) < 3:
                continue
            tokens = tagValuePair.split(FixConstants.EQUALS)
            tag = tokens[0]
            value = tokens[1]
            self.appendTag(int(tag), value)

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
        for tagValue in self.__tagValuePairs:
            tag , value = tagValue
            if tag is FixConstants.TAG_VERSION:
                continue
            if tag is FixConstants.TAG_BODY_LENGTH:
                continue
            if tag is FixConstants.TAG_BODY_CHECKSUM:
                continue
            bodyLength += len(str(tag)) + len( str(value) ) + 2 # +2 is because of = and delimiter
        return bodyLength

    def toString(self, sendingAsMessage = False):
        # If it was Python3 could use a non local variable instead making string a mutable array
        messageAsString = [""]
        
        def appendToMessageAsString(tag, value = ""):
            if len(value) == 0:
                value = self.getTagValue(tag)
            messageAsString[0] += str(tag) + FixConstants.EQUALS + value
            messageAsString[0] += FixConstants.DELIMITER

        # CALCULATE BODY LENGTH
        if sendingAsMessage is True:
            bodyLength = str(self.calculateBodyLength())
            self.setTag(FixConstants.TAG_BODY_LENGTH, bodyLength)
            
        # ADD HEADER TAGS
        for headerTag in FixConstants.HEADER_TAGS:
            if self.hasTag(headerTag):
                appendToMessageAsString(headerTag)

        # ADD BODY TAGS
        for tagValue in self.__tagValuePairs:
            tag, value = tagValue
            if FixConstants.isHeaderTag(tag) is True:
                continue
            if FixConstants.isTrailerTag(tag) is True:
                continue
            appendToMessageAsString(tag)

        # ADD TRAILER TAGS EXCLUDING CHECKSUM
        for trailerTag in FixConstants.TRAILER_TAGS:
            if self.hasTag(trailerTag):
                if trailerTag != FixConstants.TAG_BODY_CHECKSUM:
                    appendToMessageAsString(trailerTag)

        # ADD CHECKSUM
        if sendingAsMessage is True:
            checksumValue = FixMessage.calculateChecksum(messageAsString[0])
            appendToMessageAsString(FixConstants.TAG_BODY_CHECKSUM, checksumValue)
        else:
            if self.hasTag(FixConstants.TAG_BODY_CHECKSUM):
                appendToMessageAsString(FixConstants.TAG_BODY_CHECKSUM)

        return messageAsString[0]

    def __str__(self):
        ret = self.toString(False)
        return ret