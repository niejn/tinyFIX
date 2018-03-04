#!/usr/bin/python
from tiny_fix import FixConstants, FixClient, FixTime

def main():
    fixClient = FixClient()
    try:
        simulatorPort = 5555
        simulatorAddress = "127.0.0.1"
        simulatorCompId="SERVER"
        clientCompId="CLIENT"
        simulatorSubId = clientSubId = "01"
        print("Client is starting on " + str(simulatorPort) + " with compid " + clientCompId )

        fixClient.initialise(FixConstants.FIX_VERSION_4_2, simulatorAddress, simulatorPort, clientCompId, simulatorSubId, simulatorCompId, clientSubId)
        fixClient.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixClient.fixSession.setTimePrecision(FixTime.FIX_MICROSECONDS) # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
        fixClient.connect() # You can also pass a custom logon fix message

        for i in range(3):
            order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)
            order.setTags([
                            (FixConstants.FIX_TAG_CLIENT_ORDER_ID, 1), (FixConstants.FIX_TAG_SYMBOL, "GOOGL"),
                            (FixConstants.FIX_TAG_ORDER_QUANTITY, 100), (FixConstants.FIX_TAG_ORDER_PRICE, 300),
                            (FixConstants.FIX_TAG_ORDER_SIDE, FixConstants.FIX_ORDER_SIDE_BUY),
                            (453, 2), (448, 1234), (447, 'P'), (452, 1), (448, 1235), (447, 'D'), (452, 2) #Repeating groups
                         ])

            fixClient.send(order)

            print("")
            print("Sent : " + order.toString())
            print("")

            executionReport = fixClient.recv()

            print("")
            print("Received : " + executionReport.toString())
            print("")

    except ValueError as err:
        print(err.args)
    finally:
        fixClient.disconnect() # You can also pass a custom logoff message
        
# Entry point
if __name__ == "__main__":
    main()