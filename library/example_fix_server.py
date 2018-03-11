#!/usr/bin/python
from tinyFix import FixConstants, FixServer

def main():
    fixServer = FixServer()
    try:
        simulatorPort = 5555
        simulatorCompId="SERVER"
        
        print("Venue simulator is starting on " + str(simulatorPort) + " with compid " + simulatorCompId )

        fixServer.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixServer.fixSession.setTimePrecision(FixConstants.TIMESTAMP_PRECISION_MICROSECONDS) # Default value is MILLISECONDS, you can also set to SECONDS
        fixServer.start(simulatorPort, simulatorCompId)  # Responds to logon message , 
                                                         # You can respond with a customised logon message  
                                                         # by calling startWithCustomLogonResponse

        while True:
            fixMessage = fixServer.recv()
            
            if fixMessage is None:
                continue
            messageType = fixMessage.getMessageType()
            
            print("")
            print("Received : ")
            print(fixMessage)
            print("")
            
            if messageType == FixConstants.MESSAGE_LOG_OFF:
                print("")
                print("Client logged off")
                print("")
                break
            elif messageType == FixConstants.MESSAGE_HEARTBEAT:
                print("Client sent heartbeat")
                heartBeatResponse = fixServer.fixSession.getHeartbeatMessage()
                fixServer.send(heartBeatResponse)
                continue
            else:
                clientOrderId = fixMessage.getTagValue(FixConstants.TAG_CLIENT_ORDER_ID)
                execReport = fixServer.fixSession.getBaseMessage(FixConstants.MESSAGE_EXECUTION_REPORT)
                execReport.setTags([
                        (FixConstants.TAG_CLIENT_ORDER_ID, clientOrderId), 
                        (FixConstants.TAG_ORDER_STATUS, FixConstants.ORDER_STATUS_NEW), 
                        (FixConstants.TAG_EXEC_TYPE, FixConstants.ORDER_STATUS_NEW)
                     ])
                fixServer.send(execReport, True) # True is for sending executionId
                
                print("")
                print("Sent : ")
                print(execReport)
                print("")

    except ValueError as err:
        print(err.args)
    finally:
        fixServer.disconnect() # You can also pass a custom logoff message

# Entry point
if __name__ == "__main__":
    main()