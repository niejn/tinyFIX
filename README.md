<td><img src="https://img.shields.io/badge/LICENCE-PUBLIC%20DOMAIN-green.svg" alt="Licence badge"></td>

# tinyFIX

A minimal single-file library with no dependencies except stock Python(2.7) to prototype FIX server and client applications.
	
Since it is for stock Python, it will work on most Linux distributions.
	
You can just download tinyFix.py and start writing a FIX application by importing single-file library.

Python single-file library : https://github.com/akhin/tiny_fix/blob/master/library/tinyFix.py

**Writing a FIX client in a few minutes :**

	
```python
from tinyFix import FixConstants, FixClient

fixClient = FixClient()

fixClient.fixSession.setUseSequenceNumberFile(True)		  # Optional , if not called seq numbers will start from 1 and 
														  # You can also directly set seq numbers via fixSession object
fixClient.fixSession.setTimePrecision(FixConstants.TIMESTAMP_PRECISION_MICROSECONDS) # Default value is MILLISECONDS, you can also set to SECONDS

fixClient.connect("127.0.0.1", serverPortNumber, FixConstants.VERSION_4_2, clientCompId, serverCompId) # Sends logon message , call connectWithCustomLogonMessage for a custom logon message

order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)

order.setTags([
				(FixConstants.TAG_CLIENT_ORDER_ID, 1), (FixConstants.TAG_SYMBOL, "GOOGL"),
				(FixConstants.TAG_ORDER_QUANTITY, 100), (FixConstants.TAG_ORDER_PRICE, 300),
				(FixConstants.TAG_ORDER_SIDE, FixConstants.ORDER_SIDE_BUY),
				(453, 2), (448, 1234), (447, 'P'), (452, 1), (448, 1235), (447, 'D'), (452, 2) #Repeating groups
			 ])

fixClient.send(order)

print("Sent : " + order.toString())

executionReport = fixClient.recv()

print("Received : " + executionReport.toString())

fixClient.disconnect() # Sends logoff message , you can customise it by passing a FIX message		   
```
	
**Writing a FIX server in a few minutes :**

```python
from tinyFix import FixConstants, FixClient

execId = 1

fixServer = FixServer()

fixServer.fixSession.setUseSequenceNumberFile(True)		  # Optional , if not called seq numbers will start from 1 and 
														  # You can also directly set seq numbers via fixSession object

fixServer.fixSession.setTimePrecision(FixTime.TIMESTAMP_PRECISION_MICROSECONDS) # Default value is MILLISECONDS, you can also set to SECONDS

fixServer.start(serverPortNumber, serverCompId, simulatorSubId) # Responds to logon message , call startWithCustomLogonResponse for a custom logon message

while True:

	fixMessage = fixServer.recv()
	messageType = fixMessage.getMessageType()

	if messageType == FixConstants.MESSAGE_LOG_OFF:
		break
	elif messageType == FixConstants.MESSAGE_HEARTBEAT:
		heartBeatResponse = fixServer.fixSession.getHeartbeatMessage()
		fixServer.send(heartBeatResponse)
		continue
	else:
		execReport = fixServer.fixSession.getBaseMessage(FixConstants.MESSAGE_EXECUTION_REPORT)
		execReport.setTag( FixConstants.TAG_EXEC_ID, str(execId) )
		execReport.setTag( FixConstants.TAG_ORDER_STATUS, FixConstants.ORDER_STATUS_NEW)
		execReport.setTag( FixConstants.TAG_EXEC_TYPE, FixConstants.ORDER_STATUS_NEW)
		fixServer.send(execReport)

	execId = execId + 1

fixServer.disconnect() # Sends logoff message , you can customise it by passing a FIX message
```
		
**Validations :** API does not do any admin level ( sequence numbers , checksums, heartbeat check etc ) or business level ( field types , required fields for messages types , values , difference between FIX versions. ) validations. However all can be added externally easily when using tinyFix.


**Fix version / dictionary :** Having no validations help here as no dictionaries required. You can customise any message type including admin level messages which should allow connectivity with any type of venue to avoid cost of configuration/modification of an existing FIX engine.

**Adding additional FIX header tags:** Existing implementation add only mandatory header tags per FIX message throughout the session. You can add additional tags calling FixSession::addHeaderTagValuePair

**Heartbeats :** Heartbeats are automatic for clients for specified intervals. Note that client implementation currently does not take last sent message time into consideration.

**Setting sequence numbers :** There is an option for restoring sequence numbers from files with format : <sender_comp_id>_<target_comp_id>_sequence.txt
					   Also you can turn it off and set sequence numbers programatically.

**Timestamp precision :** API provides seconds, milliseconds and microseconds. The specified precision will apply to tag 52 and tag 60.

**Repeating groups	:** APIs allow generation and parsing of repeating groups. You basically need to specify an index when using getTagValue method.

**Timeouts/Async   :** Currently does not support async APIs however send and recv methods support timeout values. Timeout for sending and receiving FIX messages can be specified via FixSession::setNetworkTimeout call.

**Thread safety	 :** Only send and recv methods are using same mutex. There is no other syncronisation considerations. You can explicitly call FixSession::lock and FixSession::unlock methods.

**Limitations :** Current FIXServer is supporting only single client.

**Example applications :** You will find example FIX server and clients in library directory : https://github.com/akhin/tiny_fix/blob/master/library

**Tools :** There is currently one tool , fix_proxy.py in https://github.com/akhin/tiny_fix/blob/master/tools/ , which is basically a TCP proxy and stops when session between two sides end. It is useful to monitor FIX messages between one server and client. It can also be used as a port forwarder for FIX applications.