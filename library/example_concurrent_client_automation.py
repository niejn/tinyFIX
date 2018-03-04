#!/usr/bin/python
from tiny_fix import FixConstants, FixClient, FixTime, FixMessage
import os
from sys import platform as _platform
#As Cpython ( default python engine) uses GIL ( https://wiki.python.org/moin/GlobalInterpreterLock )
#using process instead to benefit from multicore : http://stackoverflow.com/questions/1182315/python-multicore-processing
from multiprocessing import Process, Queue
import time

class Utility:
    CONSOLE_RED = '\033[91m'
    CONSOLE_BLUE = '\033[94m'
    CONSOLE_YELLOW = '\033[93m'
    CONSOLE_END = '\033[0m'

    @staticmethod
    def getCurrentTimeInMilliseconds():
        return int(round(time.time() * 1000))

    @staticmethod
    def pressAnyKey():
        if _platform == "linux" or _platform == "linux2":
            os.system('read -s -n 1 -p "Press any key to continue..."')
        elif _platform == "win32":
            os.system('pause')

    @staticmethod
    def changeWorkingDirectoryToScriptLocation():
        absolutePath = os.path.abspath(__file__)
        dirName = os.path.dirname(absolutePath)
        os.chdir(dirName)

    @staticmethod
    def askQuestion(questionText, defaultAnswer = ""):
        actualQuestionText = questionText
        if len(defaultAnswer) == 0:
            actualQuestionText += " ( Press enter for " + defaultAnswer + " ) "
        actualQuestionText += " : "
        answer = raw_input(actualQuestionText)
        if not answer:
            answer = defaultAnswer
        return answer

    @staticmethod
    def yesNoQuestion(questionText):
        actualQuestionText = questionText + " ( Y/y or N/n ) : "
        retVal = False
        while True:
            answer = raw_input(actualQuestionText)
            answer = answer.lower()
            if not answer:
                continue

            if answer == "y" or answer == "yes":
                retVal = True
                break

            if answer == "n" or answer == "no":
                break

        return  retVal


    @staticmethod
    def writeColorMessage(message, colorCode):
        if _platform == "linux" or _platform == "linux2":
            print(colorCode + message + Utility.CONSOLE_END)
        elif _platform == "win32":
            os.system("echo " + message)

    @staticmethod
    def writeMessage(message):
        Utility.writeColorMessage(message, Utility.CONSOLE_BLUE)

    @staticmethod
    def writeErrorMessage(message):
        Utility.writeColorMessage(message, Utility.CONSOLE_RED)

    @staticmethod
    def writeInfoMessage(message):
        Utility.writeColorMessage(message, Utility.CONSOLE_YELLOW)

class StopWatch:
    def __init__(self):
        self.startTime = 0
        self.endTime = 0

    def start(self):
        self.startTime = Utility.getCurrentTimeInMilliseconds()

    def stop(self):
        self.endTime = Utility.getCurrentTimeInMilliseconds()

    def elapsedTimeInMilliseconds(self):
        return self.endTime - self.startTime

class FixAutomationClient(FixClient):
    def __init__(self):
        FixClient.__init__(self)
        self.ordersToSend = []
        self.executionReports = []

    def setOrders(self, orders):
        self.ordersToSend = orders

    def getOrders(self):
        return self.ordersToSend

    def getExecutionReports(self):
        return self.executionReports

    def addExecutionReport(self, fixMessage):
        self.executionReports.append(fixMessage)

def fixClientAutomationClientThread(resultsQueue, ordersFile, fixVersion, address, port, baseCompId, clientIndex, targetCompid):
    senderCompId = baseCompId + str(clientIndex)

    fixClient = FixAutomationClient()
    fixClient.initialise(fixVersion, address, port, senderCompId, "", targetCompid, "")

    orders = FixMessage.loadFromFile(ordersFile)
    ordersCount = len(orders)

    fixClient.connect()
    connected = fixClient.fixSession.connected

    if connected is True:
        print( senderCompId + " connected" )

        processedCount = 0

        for order  in orders:
            fixClient.send(order)

        print(senderCompId + " fired all orders")

        # Collect execution reports
        while True:
            message = fixClient.recv()

            if message is None:
                continue

            if message.getMessageType() is FixConstants.FIX_MESSAGE_HEARTBEAT:
                continue

            resultsQueue.put( str(clientIndex) +  "," +  message.toString(False) )

            if message.hasTag(FixConstants.FIX_TAG_ORDER_STATUS):
                orderStatus = message.getTagValue(FixConstants.FIX_TAG_ORDER_STATUS)
                if orderStatus is FixConstants.FIX_ORDER_STATUS_FILLED:
                    processedCount += 1
                    print( senderCompId + " received a fill :" + str(processedCount) + " of " + str(ordersCount) )
                if orderStatus is FixConstants.FIX_ORDER_STATUS_CANCELED:
                    processedCount += 1
                    ordersCount -= 1
                    print( senderCompId + " received a cancel :" + str(processedCount) + " of " + str(ordersCount) )

            if processedCount == ordersCount:
                break

        fixClient.disconnect()
        print(senderCompId + " disconnected")

class FixClientAutomation:
    def __init__(self):
        self.resultsQueue = Queue()
        self.fixClientThreads = []
        self.fixVersion = ""
        self.numberOfClients = 0
        self.ordersFile = ""
        self.address = ""
        self.port = 0
        self.compIdBase = ""
        self.targetCompId = ""

    def __del__(self):
        self.shutdown()

    def initialise(self, numberOfClients, ordersFile, fixVersion, address, port, compdIdBase, targetCompid):
        self.numberOfClients = numberOfClients
        self.ordersFile = ordersFile
        self.fixVersion = fixVersion
        self.address = address
        self.port = port
        self.compIdBase = compdIdBase
        self.targetCompId = targetCompid

    def shutdown(self):
        for thread in self.fixClientThreads:
            if thread.is_alive():
                thread.join()

    def start(self):
        for i in range(0, self.numberOfClients):
            fixClientThread = Process(target=fixClientAutomationClientThread,
                                      args=[self.resultsQueue, self.ordersFile, self.fixVersion, self.address, self.port, self.compIdBase, i+1, self.targetCompId ])
            self.fixClientThreads.append(fixClientThread)
            self.fixClientThreads[len(self.fixClientThreads) - 1].start()

    def join(self):
        for thread in self.fixClientThreads:
            thread.join()

    def report(self, reportFileName):
        report = ""

        numberOfClients = len(self.fixClientThreads)
        clientExecReports = []

        for i in range(0, numberOfClients):
            list = []
            clientExecReports.append(list)

        while not self.resultsQueue.empty():
            result = self.resultsQueue.get()
            clientIndex = int(result.split(',')[0])-1
            actualResult = result.split(',')[1]
            clientExecReports[clientIndex-1].append(actualResult)

        for i in range(0, numberOfClients):
            # Sender comp id
            currentClientFirstExecReport = FixMessage()
            currentClientFirstExecReport.loadFromString( clientExecReports[i][0] )
            report += currentClientFirstExecReport.getTagValue(FixConstants.FIX_TAG_TARGET_COMPID)

            report += "\n"
            report += "\n"

            for execReport in clientExecReports[i]:
                report += execReport
                report += "\n"

            report += "\n"
            report += "\n"

        if os.path.exists(reportFileName):
            os.remove(reportFileName)

        with open(reportFileName, "w") as textFile:
            textFile.write(report)

def main():
    try:
        Utility.changeWorkingDirectoryToScriptLocation()

        fixClientAutomation = FixClientAutomation()
        numberOfClients = 1
        ordersFile = "test_fix_messages.txt"
        fixVersion = FixConstants.FIX_VERSION_4_2
        server = "127.0.0.1"
        serverPort = 5001
        clientCompIdBase = "TEST_CLIENT"
        serverCompId = "SERVER"

        reportFile = "report.txt"

        # GATHER ARGUMENTS
        while True :
            Utility.writeInfoMessage("Current automation parameters are : ")
            print("")
            Utility.writeInfoMessage("1 Number of concurrent clients : " + str(numberOfClients))
            Utility.writeInfoMessage("2 Test case fix file : " + ordersFile)
            Utility.writeInfoMessage("3 Fix version : " + fixVersion)
            Utility.writeInfoMessage("4 Server address : " + server)
            Utility.writeInfoMessage("5 Server port : " + str(serverPort))
            Utility.writeInfoMessage("6 Server comp id : " + serverCompId)
            Utility.writeInfoMessage("7 Client comp id base value : " + clientCompIdBase)

            print("")
            answer = Utility.yesNoQuestion("Do you want to change any parameters ? ")
            print("")

            if answer is False:
                break

            if answer is True:
                try:
                    parameterIndexToChange = int( Utility.askQuestion("Enter a number between 1 and 7 :") )
                except:
                    continue
                if parameterIndexToChange >= 1 and parameterIndexToChange <= 7:
                    parameterNewValue = Utility.askQuestion("Enter value for the parameter you selected")

                    try:
                        if parameterIndexToChange == 1:
                            numberOfClients = int(parameterNewValue)
                        elif parameterIndexToChange == 2:
                            ordersFile = parameterNewValue
                        elif parameterIndexToChange == 3:
                            fixVersion = parameterNewValue
                        elif parameterIndexToChange == 4:
                            server = parameterNewValue
                        elif parameterIndexToChange == 5:
                            serverPort = int(parameterNewValue)
                        elif parameterNewValue == 6:
                            serverCompId = parameterNewValue
                        elif parameterNewValue == 7:
                            clientCompIdBase = parameterNewValue
                    except:
                        continue

        # RUN AUTOMATION
        print("")
        Utility.writeInfoMessage("Client automation starting")
        print("")

        stopwatch = StopWatch()
        stopwatch.start()

        fixClientAutomation.initialise(numberOfClients, ordersFile, fixVersion, server, serverPort, clientCompIdBase, serverCompId)
        fixClientAutomation.start()
        fixClientAutomation.join()

        stopwatch.stop()

        # DISPLAY RESULTS
        print("")
        Utility.writeInfoMessage("Client automation took " + str(stopwatch.elapsedTimeInMilliseconds()) + " milliseconds" )
        print("")

        fixClientAutomation.report(reportFile)

        if _platform == "linux" or _platform == "linux2":
            Utility.writeInfoMessage(reportFile + " created")
        elif _platform == "win32":
            os.system("notepad " + reportFile )

    except ValueError as err:
        Utility.writeErrorMessage(err.args)

# Entry point
if __name__ == "__main__":
    main()