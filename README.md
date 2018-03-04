<td><img src="https://img.shields.io/badge/LICENCE-PUBLIC%20DOMAIN-green.svg" alt="Licence badge"></td>

# tinyFIX

A minimal single-file library with no dependencies except stock Python(2.7) and Powershell (v2) to prototype FIX server and client applications.
    
Since it is for stock Python and Powershell, it will work on most Linux distributions and Windows systems.
    
You can just download tinyFix.py or tinyFix.ps1 and start writing a FIX application by importing single-file library.

**Writing a FIX client in a few minutes :** Code below is Python but please see example_fix_client.ps1 for Powershell version :
    
        from tiny_fix import FixConstants, FixClient, FixTime
        
        fixClient = FixClient()
        fixClient.initialise(FixConstants.FIX_VERSION_4_2, "127.0.0.1", serverPortNumber, clientCompId, clientSubId, serverCompId, serverSubId)
        fixClient.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixClient.fixSession.setTimePrecision(FixTime.FIX_MICROSECONDS) # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
        fixClient.connect() # Sends logon message , you can customise it by passing a FIX Message
        
        order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)
        order.setTags([
                        (FixConstants.FIX_TAG_CLIENT_ORDER_ID, 1), (FixConstants.FIX_TAG_SYMBOL, "GOOGL"),
                        (FixConstants.FIX_TAG_ORDER_QUANTITY, 100), (FixConstants.FIX_TAG_ORDER_PRICE, 300),
                        (FixConstants.FIX_TAG_ORDER_SIDE, FixConstants.FIX_ORDER_SIDE_BUY),
                        (453, 2), (448, 1234), (447, 'P'), (452, 1), (448, 1235), (447, 'D'), (452, 2) #Repeating groups
                     ])
        
        fixClient.send(order)
        print("Sent : " + order.toString())
        
        executionReport = fixClient.recv()
        print("Received : " + executionReport.toString())

        fixClient.disconnect() # Sends logoff message , you can customise it by passing a FIX message           
    
**Writing a FIX server in a few minutes :** Code below is Python but please see example_fix_client.ps1 for Powershell version : 

        from tiny_fix import FixConstants, FixClient, FixTime

        execId = 1
        fixServer = FixServer()
        fixServer.fixSession.setUseSequenceNumberFile(True)       # Optional , if not called seq numbers will start from 1 and 
                                                                  # You can also directly set seq numbers via fixSession object
        fixServer.fixSession.setTimePrecision(FixTime.FIX_MICROSECONDS) # Default value is FIX_MILLISECONDS, you can also set to FIX_SECONDS
        fixServer.start(serverPortNumber, serverCompId, simulatorSubId) # Responds with logon message, you can customise it by passing a FIX message
        
        while True:
            fixMessage = fixServer.recv()
            messageType = fixMessage.getMessageType()

            if messageType == FixConstants.FIX_MESSAGE_LOG_OFF:
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

        fixServer.disconnect() # Sends logoff message , you can customise it by passing a FIX message
		
**Features :**

		Validations					API does not do any validations but they can be added externally easily.
		
		Fix version / dictionary	Having no validations help here as no dictionaries required.
									You can customise any message type including admin level messages which should allow
									connectivity with any type of venue.
		
		Heartbeats					Heartbeats are automatic for clients for specified intervals. Note that 
									client implementation currently does not take last sent message time into consideration.
		
		Sequence number management	There is an option for restoring sequence numbers from files with format :
									<sender_comp_id>_<target_comp_id>_sequence.txt
									Also you can turn it off and set sequence numbers programatically.
									
		Timestamp precision			API provides seconds, milliseconds and microseconds. The specified precision will apply to tag60 and tag52.
		
		Repeating groups			APIs allow generation and parsing of repeating groups. You basically need to specify an index when using getTagValue method.
		
		Timeouts/Async				Currently does not support async APIs however send and recv methods support timeout values.
									Timeout for sending and receiving FIX messages can be specified via FixSession::setNetworkTimeout call.
									
		Thread safety				Only send and recv methods are using same mutex. There is no other syncronisation considerations.