#!/usr/bin/python
from tiny_fix import FixConstants
from tiny_fix import FixServer

def main():
    try:
        execId=1
        simulatorPort = 5555
        simulatorCompId="SERVER"
        clientCompId="CLIENT"
        
        print("Venue simulator is starting on " + str(simulatorPort) + " with compid " + simulatorCompId )

        fixServer = FixServer()
        fixServer.start(simulatorPort, simulatorCompId, clientCompId)
        
        while True:
            fixMessage = fixServer.recv()
            
            if fixMessage is None:
                continue
            
            messageType = fixMessage.getMessageType()
            
            print("")
            print("Received : ")
            print(fixMessage.toString(False))
            print("")
            
            if messageType == FixConstants.FIX_MESSAGE_LOG_OFF:
                fixServer.send(fixServer.fixSession.getLogoffMessage())
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
                execReport.setTag( FixConstants.FIX_TAG_CLIENT_ORDER_ID, clientOrderId)
                execReport.setTag( FixConstants.FIX_TAG_EXEC_ID, str(execId) )
                execReport.setTag( FixConstants.FIX_TAG_ORDER_STATUS, FixConstants.FIX_ORDER_STATUS_NEW)
                execReport.setTag( FixConstants.FIX_TAG_EXEC_TYPE, FixConstants.FIX_ORDER_STATUS_NEW)
                fixServer.send(execReport)
                
                print("")
                print("Sent : ")
                print(execReport.toString(False))
                print("")
            
                execId = execId + 1

        fixServer.disconnect()

    except ValueError as err:
        print(err.args)
    finally:
        if fixServer.fixSession.connected:
            fixServer.disconnect()

# Entry point
if __name__ == "__main__":
    main()