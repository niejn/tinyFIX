<td><img src="https://img.shields.io/badge/LICENCE-PUBLIC%20DOMAIN-green.svg" alt="Licence badge"></td>

# tinyFIX
tinyFix : a minimal FIX library for stock Python and stock Powershell

A minimal single-file library with no dependencies except stock Python(2.7) and Powershell (v2) to prototype FIX server and client applications.
	
Since it is for stock Python and Powershell, it will work on most Linux distributions and Windows systems.
	
You can just download tinyFix.py or tinyFix.ps1 and start writing a FIX application by importing single-file library.

**Writing a FIX client in one minute :** Code below is Python but please see example_fix_client.ps1 for Powershell version :
	
					import mini_fix
					
					fixClient = FixClient()
					fixClient.initialise("4.2", "127.0.0.1", serverPortNumber, clientCompId, serverCompId)
					fixClient.connect() # Sends logon message
					
					order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)
					order.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, 1)
					order.setTag(FixConstants.FIX_TAG_SYMBOL, "GOOGL")
					order.setTag(FixConstants.FIX_TAG_ORDER_QUANTITY, 100)
					order.setTag(FixConstants.FIX_TAG_ORDER_PRICE, 300)
					order.setTag(FixConstants.FIX_TAG_ORDER_SIDE, FixConstants.FIX_ORDER_SIDE_BUY)
					
					fixClient.send(order)
					print("Sent : " + order.toString())
					
					executionReport = fixClient.recv()
					print("Received : " + executionReport.toString())

					fixClient.disconnect() # Sends logoff message						
	
**Writing a FIX server in one minute :** Code below is Python but please see example_fix_client.ps1 for Powershell version : 

					execId = 1
					fixServer = FixServer()
					fixServer.start(serverPortNumber, serverCompId, clientCompId)
					
					while True:
						fixMessage = fixServer.recv()
						messageType = fixMessage.getMessageType()
            
						if messageType == FixConstants.FIX_MESSAGE_LOG_OFF:
							fixServer.send(fixServer.fixSession.getLogoffMessage())
							break
						elif messageType == FixConstants.FIX_MESSAGE_HEARTBEAT:
							heartBeatResponse = fixServer.fixSession.getHeartbeatMessage()
							fixServer.send(heartBeatResponse)
							continue
						else:
							execReport = fixServer.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_EXECUTION_REPORT)
							execReport.setTag( FixConstants.FIX_TAG_EXEC_ID, str(execId) )
							execReport.setTag( FixConstants.FIX_TAG_ORDER_STATUS, FixConstants.FIX_ORDER_STATUS_NEW)
							execReport.setTag( FixConstants.FIX_TAG_EXEC_TYPE, FixConstants.FIX_ORDER_STATUS_NEW)
							fixServer.send(execReport)
                 
						execId = execId + 1

					fixServer.disconnect()