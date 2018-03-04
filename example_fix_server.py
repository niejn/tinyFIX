#!/usr/bin/python
from tiny_fix import FixConstants, FixServer, FixTime

def main():
    fixServer = FixServer()
    try:
        execId=1
        simulatorPort = 5555
        simulatorCompId="SERVER"
        simulatorSubId = "01"
        
        print("Venue simulator is starting on " + str(simulatorPort) + " with compid " + simulatorCompId )

        fixServer.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixServer.fixSession.setTimePrecision(FixTime.FIX_MICROSECONDS) # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
        fixServer.start(simulatorPort, simulatorCompId, simulatorSubId) # Responds with logon message, you can customise it by passing a FIX message

        while True:
            fixMessage = fixServer.recv()
            
            if fixMessage is None:
                continue
            messageType = fixMessage.getMessageType()
            
            print("")
            print("Received : ")
            print(fixMessage.toString())
            print("")
            
            if messageType == FixConstants.FIX_MESSAGE_LOG_OFF:
                print("")
                print("Client logged off")
                print("")
                break
            elif messageType == FixConstants.FIX_MESSAGE_HEARTBEAT:
                print("Client sent heartbeat")
                heartBeatResponse = fixServer.fixSession.getHeartbeatMessage()
                fixServer.send(heartBeatResponse)
                continue
            else:
                clientOrderId = fixMessage.getTagValue(FixConstants.FIX_TAG_CLIENT_ORDER_ID)
                execReport = fixServer.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_EXECUTION_REPORT)
                execReport.setTags([
                        (FixConstants.FIX_TAG_CLIENT_ORDER_ID, clientOrderId), (FixConstants.FIX_TAG_EXEC_ID, str(execId)),
                        (FixConstants.FIX_TAG_ORDER_STATUS, FixConstants.FIX_ORDER_STATUS_NEW), (FixConstants.FIX_TAG_EXEC_TYPE, FixConstants.FIX_ORDER_STATUS_NEW)
                     ])
                fixServer.send(execReport)
                
                print("")
                print("Sent : ")
                print(execReport.toString())
                print("")
            
                execId = execId + 1

    except ValueError as err:
        print(err.args)
    finally:
        fixServer.disconnect() # You can also pass a custom logoff message

# Entry point
if __name__ == "__main__":
    main()