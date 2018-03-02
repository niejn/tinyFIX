#!/usr/bin/python
from tiny_fix import FixConstants
from tiny_fix import FixClient

def main():
    try:
        simulatorPort = 5555
        simulatorCompId="SERVER"
        clientCompId="CLIENT"
        print("Client is starting on " + str(simulatorPort) + " with compid " + clientCompId )

        fixClient = FixClient()
        fixClient.initialise("FIX.4.2", "127.0.0.1", simulatorPort, clientCompId, simulatorCompId)
        fixClient.connect()

        order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)
        order.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, 1)
        order.setTag(FixConstants.FIX_TAG_SYMBOL, "GOOGL")
        order.setTag(FixConstants.FIX_TAG_ORDER_QUANTITY, 100)
        order.setTag(FixConstants.FIX_TAG_ORDER_PRICE, 300)
        order.setTag(FixConstants.FIX_TAG_ORDER_SIDE, FixConstants.FIX_ORDER_SIDE_BUY)

        fixClient.send(order)

        print("")
        print("Sent : " + order.toString(False))
        print("")

        executionReport = fixClient.recv()

        print("")
        print("Received : " + executionReport.toString(False))
        print("")

        fixClient.disconnect()

    except ValueError as err:
        print(err.args)

# Entry point
if __name__ == "__main__":
    main()