#!/usr/bin/python
from tinyFix import FixConstants, FixClient

def main():
    fixClient = FixClient()
    try:
        simulatorPort = 5555
        simulatorAddress = "127.0.0.1"
        simulatorCompId="SERVER"
        clientCompId="CLIENT"
        print("Client is starting on " + str(simulatorPort) + " with compid " + clientCompId )

        fixClient.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixClient.fixSession.setTimePrecision(FixConstants.TIMESTAMP_PRECISION_MICROSECONDS) # Default value is MILLISECONDS, you can also set to SECONDS
        fixClient.connect(simulatorAddress, simulatorPort, FixConstants.VERSION_4_2, clientCompId, simulatorCompId) # Sends logon message , 
                                                                                                                    # You can send a customised logon message   
                                                                                                                    # by calling connectWithCustomLogonMessage

        for i in range(3):
            order = fixClient.fixSession.getBaseMessage(FixConstants.MESSAGE_NEW_ORDER)
            order.setTags([
                            (FixConstants.TAG_CLIENT_ORDER_ID, 1), (FixConstants.TAG_SYMBOL, "GOOGL"),
                            (FixConstants.TAG_ORDER_QUANTITY, 100), (FixConstants.TAG_ORDER_PRICE, 300),
                            (FixConstants.TAG_ORDER_SIDE, FixConstants.ORDER_SIDE_BUY), (FixConstants.TAG_TRANSACTION_TIME, fixClient.fixSession.getCurrentUTCDateTime()),
                            (453, 2), (448, 1234), (447, 'P'), (452, 1), (448, 1235), (447, 'D'), (452, 2) #Repeating groups
                         ])

            fixClient.send(order)

            print("")
            print("Sent : ")
            print(order)
            print("")

            executionReport = fixClient.recv()

            print("")
            print("Received : ") 
            print(executionReport)
            print("")

    except ValueError as err:
        print(err.args)
    finally:
        fixClient.disconnect() # You can also pass a custom logoff message
        
# Entry point
if __name__ == "__main__":
    main()