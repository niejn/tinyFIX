[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# tinyFIX

**What :**

A minimal FIX protocol library for stock Python(2.7) to create tools using FIX protocol and prototype FIX server and client applications.
	
Since it is for stock Python, it will work on most Linux distributions as is.
	
You can just download tinyFix.py and start writing a FIX application by importing single-file library.
Python single-file library : https://github.com/akhin/tiny_fix/blob/master/library_single_file/tinyFix.py

Or you can use its package version : https://github.com/akhin/tiny_fix/blob/master/library_package/

**Why :** 

Created it because it might not always be straightforward to crete test applications using existing FIX engines. FIX engines can do many things behind the scenes that you are not aware.
You will need to configure their XML dictionaries and you will need to learn and use different APIs to customise FIX messages when connecting to different venues. You might even need to 
modify their source code. 

You have full control over your FIX messages generated with tinyFix. You can have connectivity to any venue and do any type of custom logon or other operations. For ex , if you want microseconds precision for tag 52 and tag 60 for Mifid2 ,
you can do it with tinyFix. You don`t need to spend time to find out specific APIs , instead you just need to call addTag/hasTag/getTagValue methods for all types of messages.

**Writing a FIX client in a few minutes :**

	
```python
from tinyFix import FixConstants, FixClient

fixClient = FixClient()

# Optional , if not called seq numbers will start from 1 and 
# You can also directly set seq numbers via fixSession object
fixClient.fixSession.setUseSequenceNumberFile(True)		  
		
# Default timeprecision is MILLISECONDS, you can also set to SECONDS		
fixClient.fixSession.setTimePrecision(FixConstants.TIMESTAMP_PRECISION_MICROSECONDS) 

# Sends logon message , call connectWithCustomLogonMessage for a custom logon message
fixClient.connect("127.0.0.1", serverPortNumber, FixConstants.VERSION_4_2, clientCompId, serverCompId) 

order = fixClient.fixSession.getBaseMessage(FixConstants.FIX_MESSAGE_NEW_ORDER)

order.setTags([
				(FixConstants.TAG_CLIENT_ORDER_ID, 1), (FixConstants.TAG_SYMBOL, "GOOGL"),
				(FixConstants.TAG_ORDER_QUANTITY, 100), (FixConstants.TAG_ORDER_PRICE, 300),
				(FixConstants.TAG_ORDER_SIDE, FixConstants.ORDER_SIDE_BUY),
				(453, 2), (448, 1234), (447, 'P'), (452, 1), (448, 1235), (447, 'D'), (452, 2)
			 ])

fixClient.send(order)

print("Sent : " + order.toString())

executionReport = fixClient.recv()

print("Received : " + executionReport.toString())

# Sends logoff message , you can customise it by passing a FIX message	
fixClient.disconnect() 	   
```
	
**Writing a FIX server in a few minutes :**

```python
from tinyFix import FixConstants, FixClient

execId = 1

fixServer = FixServer()

# Optional , if not called seq numbers will start from 1 and 
# You can also directly set seq numbers via fixSession object
fixServer.fixSession.setUseSequenceNumberFile(True)

# Default timeprecision is MILLISECONDS, you can also set to SECONDS	
fixServer.fixSession.setTimePrecision(FixConstants.TIMESTAMP_PRECISION_MICROSECONDS)

# Responds to logon message , call startWithCustomLogonResponse for a custom logon message
fixServer.start(serverPortNumber, serverCompId, simulatorSubId) 

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

# Details

**Validations :** API does not do any admin level ( sequence numbers , checksums, heartbeat check etc ) or business level ( field types , required fields for messages types , values , difference between FIX versions. ) validations. However all can be added externally easily when using tinyFix.

**Fix version / dictionary :** Having no validations help here as no dictionaries required. You can customise any message type including admin level messages which should allow connectivity with any type of venue to avoid cost of configuration/modification of an existing FIX engine.

**Adding additional FIX header tags:** Existing implementation add only mandatory header tags per FIX message throughout the session. You can add additional tags calling FixSession::addHeaderTagValuePair

**Heartbeats :** Heartbeats are automatic for clients for specified intervals. Note that client implementation currently does not take last sent message time into consideration.

**Setting sequence numbers :** There is an option for restoring sequence numbers from files with format : <sender_comp_id>_<target_comp_id>_sequence.txt
					   Also you can turn it off and set sequence numbers programatically.

**Timestamp precision :** API provides seconds, milliseconds and microseconds. The specified precision will apply to tag 52 and tag 60.

**Repeating groups	:** APIs allow generation and parsing of repeating groups. You basically need to specify an index when using getTagValue to get a repeating group value. When building them , you can use setTag with an index or just use appendTag. Index values are 1-based.

**Timeouts/Async   :** Currently does not support async APIs however FixTcpTransport class methods connect/accept/send/recv methods support timeout values. Timeout for sending and receiving FIX messages can be specified by setting fixSession.fixTransport.netwrokTimeoutInSeconds.

**Thread safety	 :** Only send and recv methods are using same mutex. There is no other syncronisation considerations. You can explicitly call FixSession::lock and FixSession::unlock methods.

**TCP Receiving mechanism :** Receiving mechanism does not do any caching and entirely relies on tag 9 ( body length ) when receiving messages. This mechanism does not have the highest performance as it is not trying to receive all at once from socket buffer and it is also fragile as relies on the other side properly setting tag9. However it will work in most cases.

**Using message queues instead of TCP :** Many internal enterprise FIX applications work with message queues like Tibco or Solace. You can use tinyFix with those by implementing a transport class ( see FixTcpTransport class) and using your implementation by setting fixSession.fixTransport variable.

**Loading FIX messages from files :** You can call FixMessage::loadFromFile method which will return a list of FixMessage objects. It will ignore the lines starting with a hash.

**Limitations :** Current FIXServer is supporting only single client.

**Example applications :** You will find example FIX server, client and concurrent client automation in examples directory : https://github.com/akhin/tiny_fix/blob/master/examples

**Tools :** There is currently one tool , fix_proxy.py in https://github.com/akhin/tiny_fix/blob/master/tools/ , which is basically a TCP proxy and stops when session between two sides end. It is useful to monitor FIX messages between one server and client. It can also be used as a port forwarder for FIX applications.

# Contact

You can mail akin_ocal @ hotmail .com for any questions or enquiries.