function tinyFixInitialise()
{
  $source = @"
  using System;
 
    public class FixConstants
    {
        // GENERAL
        public const char FIX_EQUALS = '=';
        public const char FIX_DELIMITER = ((char)1);
        // VERSIONS
        public const string FIX_VERSION_4_0 = "FIX.4.0";
        public const string FIX_VERSION_4_1 = "FIX.4.1";
        public const string FIX_VERSION_4_2 = "FIX.4.2";
        public const string FIX_VERSION_4_3 = "FIX.4.3";
        public const string FIX_VERSION_4_4 = "FIX.4.4";
        public const string FIX_VERSION_5_0 = "FIX.5.0";
        // TAGS
        public const int FIX_AVERAGE_PRICE = 6;
        public const int FIX_TAG_VERSION = 8;
        public const int FIX_TAG_BODY_LENGTH = 9;
        public const int FIX_TAG_BODY_CHECKSUM = 10;
        public const int FIX_TAG_CLIENT_ORDER_ID = 11;
        public const int FIX_TAG_CUMULATIVE_QUANTITY = 14;
        public const int FIX_TAG_EXEC_ID = 17;
        public const int FIX_TAG_EXEC_INST = 18;
        public const int FIX_TAG_EXEC_TRANSTYPE = 20;
        public const int FIX_TAG_HAND_INST = 21;
        public const int FIX_TAG_LAST_PRICE = 31;
        public const int FIX_TAG_LAST_QUANTITY = 32;
        public const int FIX_TAG_SEQUENCE_NUMBER = 34;
        public const int FIX_TAG_MESSAGE_TYPE = 35;
        public const int FIX_TAG_ORDER_ID = 37;
        public const int FIX_TAG_ORDER_QUANTITY = 38;
        public const int FIX_TAG_ORDER_STATUS = 39;
        public const int FIX_TAG_ORDER_TYPE = 40;
        public const int FIX_TAG_ORIG_CLIENT_ORDER_ID = 41;
        public const int FIX_TAG_ORDER_PRICE = 44;
        public const int FIX_TAG_SECURITY_ID = 48;
        public const int FIX_TAG_SENDER_COMPID = 49;
        public const int FIX_TAG_SENDER_SUBID = 50;
        public const int FIX_TAG_SENDING_TIME = 52;
        public const int FIX_TAG_ORDER_SIDE = 54;
        public const int FIX_TAG_SYMBOL = 55;
        public const int FIX_TAG_TARGET_COMPID = 56;
        public const int FIX_TAG_TARGET_SUBID = 57;
        public const int FIX_TAG_TIME_IN_FORCE = 59;
        public const int FIX_TAG_TRANSACTION_TIME = 60;
        public const int FIX_TAG_ENCRYPT_METHOD = 98;
        public const int FIX_TAG_HEARTBEAT_INTERVAL = 108;
        public const int FIX_TAG_TEST_REQ_ID = 112;
        public const int FIX_TAG_EXEC_TYPE = 150;
        public const int FIX_TAG_LEAVES_QTY = 151;
        public const int FIX_TAG_USERNAME = 553;
        public const int FIX_TAG_PASSWORD = 554;
        public const int FIX_TAG_USER_REQUEST_ID = 923;
        public const int FIX_TAG_USER_PASSWORD = 924;
        // MESSAGE TYPES
        public const string FIX_MESSAGE_HEARTBEAT = "0";
        public const string FIX_MESSAGE_TEST_REQUEST = "1";
        public const string FIX_MESSAGE_LOG_ON = "A";
        public const string FIX_MESSAGE_LOG_OFF = "5";
        public const string FIX_MESSAGE_ADMIN_REJECT = "3";
        public const string FIX_MESSAGE_USER_LOGON = "BE";
        public const string FIX_MESSAGE_USER_RESPONSE = "BF";
        public const string FIX_MESSAGE_EXECUTION_REPORT = "8";
        public const string FIX_MESSAGE_NEW_ORDER = "D";
        public const string FIX_MESSAGE_AMEND_ORDER = "G";
        public const string FIX_MESSAGE_CANCEL_ORDER = "F";
        public const string FIX_MESSAGE_BUSINESS_REJECT = "j";
        // ORDER STATUS
        public const int FIX_ORDER_STATUS_NEW = 0;
        public const int FIX_ORDER_STATUS_PARTIALLY_FILLED = 1;
        public const int FIX_ORDER_STATUS_FILLED = 2;
        public const int FIX_ORDER_STATUS_DONE_FOR_DAY = 3;
        public const int FIX_ORDER_STATUS_CANCELED = 4;
        public const int FIX_ORDER_STATUS_REPLACED = 5;
        public const int FIX_ORDER_STATUS_PENDING_CANCEL = 6;
        public const int FIX_ORDER_STATUS_STOPPED = 7;
        public const int FIX_ORDER_STATUS_REJECTED = 8;
        // ORDER TYPE
        public const int FIX_ORDER_TYPE_MARKET = 1;
        public const int FIX_ORDER_TYPE_LIMIT = 2;
        // SIDE
        public const int FIX_ORDER_SIDE_BUY = 1;
        public const int FIX_ORDER_SIDE_SELL = 2;
        // TIME IN FORCE
        public const int FIX_ORDER_TIF_DAY = 0;
        // ENCRYPTION METHODS
        public const int FIX_ENCRYPTION_NONE = 0;
    }
    
    // Not using enum to be consistent with Python interface
    public class FixTime
    {
        public const int FIX_SECONDS = 1;
        public const int FIX_MILLISECONDS = 2;
        public const int FIX_MICROSECONDS = 3;
        
        static public string getCurrentUTCDateTimeSeconds()
        {
            string datetime = "";
            datetime = System.DateTime.Now.ToString("yyyyMMdd-HH:mm:ss");
            return datetime;
        }
        
        static public string getCurrentUTCDateTimeMilliseconds()
        {
            string datetime = "";
            datetime = System.DateTime.Now.ToString("yyyyMMdd-HH:mm:ss.fff");
            return datetime;
        }
        
        static public string getCurrentUTCDateTimeMicroseconds()
        {
            string datetime = "";
            datetime = System.DateTime.Now.ToString("yyyyMMdd-HH:mm:ss.ffffff");
            return datetime;
        }
    }
    
    // Not using .Net FW tuples in order to support most C# / .Net FW versions
    public class FixTagValuePair
    {
        public int Tag {get; set;}
        public string Value {get; set;}
    }
 
    public class FixMessage
    {
        private System.Collections.Generic.List<FixTagValuePair> m_tagValuePairs = new System.Collections.Generic.List<FixTagValuePair>();
        private int m_timePrecision = FixTime.FIX_MILLISECONDS;
        
        System.Text.StringBuilder m_builder = new System.Text.StringBuilder();
 
        private void appendTagValueToBuilder(int tag, string value = "")
        {
            if( value.Length == 0)
            {
                value = getTagValue(tag);
            }
            m_builder.Append(tag.ToString() + FixConstants.FIX_EQUALS + value);
            m_builder.Append(FixConstants.FIX_DELIMITER);
        }
        
        public void setTimePrecision(int precision)
        {
            m_timePrecision = precision;
        }
        
        public string getCurrentUTCDateTime()
        {
            if( m_timePrecision == FixTime.FIX_MICROSECONDS)
            {
                return FixTime.getCurrentUTCDateTimeMicroseconds();
            }
            
            if( m_timePrecision == FixTime.FIX_MILLISECONDS)
            {
                return FixTime.getCurrentUTCDateTimeMilliseconds();
            }
            
            return FixTime.getCurrentUTCDateTimeSeconds();
        }
 
        public static string calculateChecksum(string message)
        {
            string checksum = "";
            int sum = 0;
 
            foreach (char c in message)
            {
                sum += (int)c;
            }
 
            sum = sum % 256;
            checksum = string.Format("{0}", sum);
            checksum = checksum.PadLeft(3, '0');
            return checksum;
        }
 
        public string getMessageType()
        {
            return getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE);
        }
 
        public bool isAdminMessage()
        {
            var type = getMessageType();
            if (type == FixConstants.FIX_MESSAGE_HEARTBEAT)
            {
                return true;
            }
            if (type == FixConstants.FIX_MESSAGE_LOG_ON)
            {
                return true;
            }
            if (type == FixConstants.FIX_MESSAGE_LOG_OFF)
            {
                return true;
            }
            return false;
        }
        
        static public bool isBodyTag(int tag)
        {
            if( tag == FixConstants.FIX_TAG_VERSION )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_BODY_LENGTH )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_MESSAGE_TYPE )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_SEQUENCE_NUMBER )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_SENDING_TIME )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_SENDER_COMPID )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_SENDER_SUBID )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_TARGET_COMPID )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_TARGET_SUBID )
            {
                return false;
            }
            if( tag == FixConstants.FIX_TAG_BODY_CHECKSUM )
            {
                return false;
            }
            return true;
        }
 
        public int calculateBodyLength()
        {
            int bodyLength = 0;
 
            foreach (var tagValue in m_tagValuePairs)
            {
                //  We exclude header and checksum
                if (tagValue.Tag == FixConstants.FIX_TAG_VERSION)
                {
                    continue;
                }
 
                if (tagValue.Tag == FixConstants.FIX_TAG_BODY_LENGTH)
                {
                    continue;
                }
 
                if (tagValue.Tag == FixConstants.FIX_TAG_BODY_CHECKSUM)
                {
                    continue;
                }
 
                bodyLength += tagValue.Tag.ToString().Length + 2 + tagValue.Value.Length; // +2 is because of = and delimiter
            }
 
            return bodyLength;
        }
 
        public void setFixVersion(string fixVersion)
        {
            setTag(FixConstants.FIX_TAG_VERSION, fixVersion);
        }
 
        public bool hasTag(int tag)
        {
            foreach (var tagValue in m_tagValuePairs)
            {
                if(tagValue.Tag == tag)
                {
                    return true;
                }
            }
            return false;
        }
 
        public void setTag(int tag, string value)
        {
            var pair = new FixTagValuePair();
            pair.Tag = tag;
            pair.Value = value;
            m_tagValuePairs.Add(pair);
        }
 
        public void setTag(int tag, char value)
        {
            setTag(tag, value.ToString());
        }
 
        public void setTag(int tag, int value)
        {
            setTag(tag, value.ToString());
        }
        
        public void setTag(int tag, double value)
        {
            setTag(tag, value.ToString());
        }
 
        public string getTagValue(int tag, int index=1)
        {
            var count = 0;
            foreach (var tagValue in m_tagValuePairs)
            {
                if(tag == tagValue.Tag)
                {
                    count++;
                    if(index == count)
                    {
                        return tagValue.Value;
                    }
                }
            }
            return null;
        }
 
        public void loadFromString(string input)
        {
            var tagValuePairs = input.Split(FixConstants.FIX_DELIMITER);
 
            foreach (var tagValuePair in tagValuePairs)
            {
                if (tagValuePair.Length == 0)
                {
                    continue;
                }
                var tokens = tagValuePair.Split(FixConstants.FIX_EQUALS);
                int tag = System.Convert.ToInt32(tokens[0]);
                string value = tokens[1];
                setTag(tag, value);
            }
        }
 
        static public System.Collections.Generic.List<FixMessage> loadFromFile(string fileName)
        {
            System.Collections.Generic.List<FixMessage> ret = new System.Collections.Generic.List<FixMessage>();
            if (System.IO.File.Exists(fileName))
            {
                using (System.IO.StreamReader file = new System.IO.StreamReader(fileName))
                {
                    string line;
 
                    while ((line = file.ReadLine()) != null)
                    {
                        FixMessage currentMessage = new FixMessage();
                        currentMessage.loadFromString(line);
                        ret.Add(currentMessage);
                    }
                }
            }
            return ret;
        }
 
        public string toString(bool sendingAsAMessage = false, bool updateTransactionTime = false)
        {
            m_builder = new System.Text.StringBuilder();
            // FIX VERSION
            appendTagValueToBuilder(FixConstants.FIX_TAG_VERSION);
 
            // FIX SENDING TIME AND TRANSACTION, have to be before body length calculation ,but not appended for the correct order
            if (sendingAsAMessage)
            {
                var currentUTCDateTime = getCurrentUTCDateTime();
                setTag(FixConstants.FIX_TAG_SENDING_TIME, currentUTCDateTime);
               
                if (updateTransactionTime && isAdminMessage() == false)
                {
                    setTag(FixConstants.FIX_TAG_TRANSACTION_TIME, currentUTCDateTime);
                }
            }
 
            // FIX BODY LENGTH
            if (sendingAsAMessage)
            {
                var bodyLength = calculateBodyLength().ToString();
                appendTagValueToBuilder(FixConstants.FIX_TAG_BODY_LENGTH, bodyLength);
            }
            else
            {
                if( hasTag(FixConstants.FIX_TAG_BODY_LENGTH))
                {
                    appendTagValueToBuilder(FixConstants.FIX_TAG_BODY_LENGTH);
                }
            }
 
            // FIX MESSAGE TYPE
            appendTagValueToBuilder(FixConstants.FIX_TAG_MESSAGE_TYPE);
 
            // FIX SEQUENCE NUMBER
            appendTagValueToBuilder(FixConstants.FIX_TAG_SEQUENCE_NUMBER);
 
            // FIX SENDER COMPID
            appendTagValueToBuilder(FixConstants.FIX_TAG_SENDER_COMPID);
            
            // FIX SENDER SUBID
            if( hasTag(FixConstants.FIX_TAG_SENDER_SUBID) )
            {
                appendTagValueToBuilder(FixConstants.FIX_TAG_SENDER_SUBID);
            }           
 
            // FIX SENDING TIME
            appendTagValueToBuilder(FixConstants.FIX_TAG_SENDING_TIME);
 
            // FIX TARGET COMPID
            appendTagValueToBuilder(FixConstants.FIX_TAG_TARGET_COMPID);
            
            // FIX TARGET SUBID
            if( hasTag(FixConstants.FIX_TAG_TARGET_SUBID) )
            {
                appendTagValueToBuilder(FixConstants.FIX_TAG_TARGET_SUBID);
            }       
 
            foreach (var tagValue in m_tagValuePairs)
            {
                if( isBodyTag( tagValue.Tag ) == false )
                {
                    continue;
                }
                appendTagValueToBuilder(tagValue.Tag);
            }
 
            // FIX CHECKSUM
            if (sendingAsAMessage)
            {
                var checksum = calculateChecksum(m_builder.ToString());
                appendTagValueToBuilder(FixConstants.FIX_TAG_BODY_CHECKSUM, checksum);           
            }
            else
            {
                if( hasTag(FixConstants.FIX_TAG_BODY_CHECKSUM))
                {
                    appendTagValueToBuilder(FixConstants.FIX_TAG_BODY_CHECKSUM);
                }
            }
            return m_builder.ToString();
        }
    }
 
    public class FixSession
    {
        private System.Net.Sockets.Socket m_socket = new System.Net.Sockets.Socket(System.Net.Sockets.AddressFamily.InterNetwork, System.Net.Sockets.SocketType.Stream, System.Net.Sockets.ProtocolType.Tcp);
        private System.Net.Sockets.Socket m_serverSocket = new System.Net.Sockets.Socket(System.Net.Sockets.AddressFamily.InterNetwork, System.Net.Sockets.SocketType.Stream, System.Net.Sockets.ProtocolType.Tcp);
        private System.Timers.Timer m_heartbeatTimer = new System.Timers.Timer();
        private System.Threading.Mutex m_mutex = new System.Threading.Mutex();
 
        public bool Connected { get; set; }
        public int TimePrecision {get; set;}
        public int NetworkTimeoutInSeconds{get; set;}
        public bool RestoreSequenceNumbersFromFile {get; set;}
        public string TargetAddress { get; set; }
        public int TargetPort { get; set; }
        public string TargetCompid { get; set; }
        public string TargetSubid { get; set; }
        public string SenderCompid { get; set; }
        public string SenderSubid { get; set; }
        public int HeartbeatInterval { get; set; }
        public int EncryptionMethod { get; set; }
        public int IncomingSequenceNumber { get; set; }
        public int OutgoingSequenceNumber { get; set; }
        public string FixVersion { get; set; }
 
        public FixSession()
        {
            Connected = false;
            TimePrecision = FixTime.FIX_MILLISECONDS;
            HeartbeatInterval = 30;
            EncryptionMethod = FixConstants.FIX_ENCRYPTION_NONE;
            NetworkTimeoutInSeconds = 0;
            IncomingSequenceNumber = 1;
            OutgoingSequenceNumber = 1;
            m_socket.NoDelay = true;
            enableSocketBlocking();
        }
 
        public FixMessage getBaseMessage(string messageType)
        {
            FixMessage message = new FixMessage();
            message.setFixVersion(FixVersion);
            message.setTimePrecision(TimePrecision);
            message.setTag(FixConstants.FIX_TAG_MESSAGE_TYPE, messageType);
            // Sequence number will be added during sending
            message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, SenderCompid);
            
            if( SenderSubid != null )
            {
                if(SenderSubid.Length > 0)
                {
                    message.setTag(FixConstants.FIX_TAG_SENDER_SUBID, SenderSubid);
                }
            }
            message.setTag(FixConstants.FIX_TAG_SENDING_TIME, "");
            message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, TargetCompid);
            
            if( TargetSubid != null )
            {
                if(TargetSubid.Length > 0)
                {
                    message.setTag(FixConstants.FIX_TAG_TARGET_SUBID, TargetSubid);
                }
            }
            return message;
        }
 
        public FixMessage getLogonMessage()
        {
            FixMessage message = getBaseMessage(FixConstants.FIX_MESSAGE_LOG_ON);
            message.setTag(FixConstants.FIX_TAG_ENCRYPT_METHOD, EncryptionMethod);
            message.setTag(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL, HeartbeatInterval);
            return message;
        }
 
        public FixMessage getLogoffMessage()
        {
            FixMessage message = getBaseMessage(FixConstants.FIX_MESSAGE_LOG_OFF);
            return message;
        }
 
        private FixMessage getHeartbeatMessage()
        {
            FixMessage message = getBaseMessage(FixConstants.FIX_MESSAGE_HEARTBEAT);
            return message;
        }
 
        private string getSequenceFileName()
        {
            string ret = SenderCompid + "_" + TargetCompid + "_sequence.txt";
            return ret;
        }
 
        public bool connect(FixMessage logonMessage)
        {
            FixMessage message = null;
            // Not supporting timeouts in accept and connect methods
            var originalNetworkTimeoutInSeconds = NetworkTimeoutInSeconds;
            NetworkTimeoutInSeconds = 0;
            
            while(true)
            {   
                try
                {
                    m_socket.Connect(TargetAddress, TargetPort);

                    if( RestoreSequenceNumbersFromFile )
                    {
                        restoreSequenceNumberFromFile();
                    }
     
                    if(logonMessage == null)
                    {
                        logonMessage = getLogonMessage();
                    }

                    send(logonMessage);

                    message = recv();

                    if( message.getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE) != FixConstants.FIX_MESSAGE_LOG_ON )
                    {
                        throw new Exception("Incoming message was not a logon response");
                    }

                    if( RestoreSequenceNumbersFromFile == false)
                    {
                        IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
                    }

                    m_heartbeatTimer.Interval = HeartbeatInterval * 1000;
                    m_heartbeatTimer.Elapsed += new System.Timers.ElapsedEventHandler(heartbeatTimerFunction);
                    m_heartbeatTimer.Start();
                    Connected = true;

                    break;
                }
                catch(System.Net.Sockets.SocketException e)
                {
                    if(e.ErrorCode == 10061) // WSAECONNREFUSED
                    {
                        continue;
                    }
                }
                catch (System.Exception e)
                {
                    string exceptionMessage = "Error during a connection attempt : " ;
                    exceptionMessage += e.Message;
                    
                    if( message != null )
                    {
                        exceptionMessage += System.Environment.NewLine;
                        exceptionMessage += message.toString();
                    }

                    System.Console.WriteLine(exceptionMessage);
                    break;
                }
            }
            
            NetworkTimeoutInSeconds = originalNetworkTimeoutInSeconds;
            return Connected;
        }
 
        public bool accept(FixMessage logOnResponse)
        {
            FixMessage message = null;
            // Not supporting timeouts in accept and connect methods
            var originalNetworkTimeoutInSeconds = NetworkTimeoutInSeconds;
            NetworkTimeoutInSeconds = 0;
            try
            {
                System.Net.IPHostEntry ipHostInfo = System.Net.Dns.GetHostEntry(System.Net.Dns.GetHostName());
                System.Net.IPAddress ipAddress = ipHostInfo.AddressList[0];
                System.Net.IPEndPoint localEndPoint = new System.Net.IPEndPoint(Convert.ToInt32(TargetAddress), TargetPort);
 
                m_serverSocket.Bind(localEndPoint);
                m_serverSocket.Listen(100);
                m_socket = m_serverSocket.Accept();
 
                message = recv();
                    
                if( message.getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE) != FixConstants.FIX_MESSAGE_LOG_ON )
                {
                    throw new Exception("Incoming message was not a logon message");
                }
                
                if( RestoreSequenceNumbersFromFile == false )
                {
                    IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
                }
                else
                {
                    restoreSequenceNumberFromFile();
                }
                
                HeartbeatInterval = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL));
                TargetCompid = message.getTagValue(FixConstants.FIX_TAG_SENDER_COMPID);
                
                if( message.hasTag(FixConstants.FIX_TAG_SENDER_SUBID) )
                {
                    SenderSubid = message.getTagValue(FixConstants.FIX_TAG_SENDER_SUBID);
                }

                FixVersion = message.getTagValue(FixConstants.FIX_TAG_VERSION);
                if (message.hasTag(FixConstants.FIX_TAG_ENCRYPT_METHOD))
                {
                    EncryptionMethod = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_ENCRYPT_METHOD));
                    
                }
                if(logOnResponse == null)
                {
                    logOnResponse = getLogonMessage();
                }
                send(logOnResponse);
                Connected = true;
            }
            catch (System.Exception e)
            {
                string exceptionMessage = "Error during a connection attempt : " ;
                exceptionMessage += e.Message;
                
                if( message != null )
                {
                    exceptionMessage += System.Environment.NewLine;
                    exceptionMessage += message.toString();
                }

                System.Console.WriteLine(exceptionMessage);
            }
            NetworkTimeoutInSeconds = originalNetworkTimeoutInSeconds;
            return Connected;
        }
 
        private void heartbeatTimerFunction(object sender, System.EventArgs e)
        {
            try
            {
                send(getHeartbeatMessage());
            }
            catch { }
        }
 
        public bool send(FixMessage message)
        {
            message.setTag(FixConstants.FIX_TAG_VERSION, FixVersion);
            message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, SenderCompid);
            message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, TargetCompid);
            int sentBytes = 0;
            
            m_mutex.WaitOne();
            
            if(NetworkTimeoutInSeconds > 0)
            {
                m_socket.Blocking = false;
                m_socket.SendTimeout = NetworkTimeoutInSeconds * 1000;
            }
            
            message.setTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER, OutgoingSequenceNumber);
            var str = message.toString(true, true);
            byte[] bytes = System.Text.Encoding.ASCII.GetBytes(str);
            
            try
            {
                sentBytes = m_socket.Send(bytes);
                if(sentBytes > 0)
                {
                    OutgoingSequenceNumber += 1;
                }
            }
            catch
            {
                sentBytes = 0;
            }
            
            enableSocketBlocking();
            m_mutex.ReleaseMutex();
            return sentBytes > 0;
        }
 
        private string recvString(int length)
        {
            try
            {
                System.Text.Decoder decoder = System.Text.Encoding.UTF8.GetDecoder();
                byte[] buffer = new byte[length];
                Int32 bytes = m_socket.Receive(buffer);
                char[] chars = new char[bytes];
                int charLen = decoder.GetChars(buffer, 0, bytes, chars, 0);
                System.String received = new System.String(chars);
                return received;
            }
            catch
            {
                return null;
            }
        }
        
        private void enableSocketBlocking()
        {
            m_socket.Blocking = true;
            m_socket.ReceiveTimeout = 0;
            m_socket.SendTimeout = 0;
        }
 
        public FixMessage recv()
        {
            FixMessage message = null;
            m_mutex.WaitOne();
            
            if(NetworkTimeoutInSeconds > 0)
            {
                m_socket.Blocking = false;
                m_socket.ReceiveTimeout = NetworkTimeoutInSeconds * 1000;
            }
            
            try
            {
                string initialBuffer = recvString(20); // Length of 8=FIX.4.2@9=7000@35= so we always get 35=A
     
                if (initialBuffer == null)
                {
                    throw new Exception("Receive failed");
                }
     
                if (initialBuffer.Length == 0)
                {
                    throw new Exception("Receive failed");
                }
     
                int allBytes = System.Convert.ToInt32(initialBuffer.Split((char)1)[1].Split('=')[1]);
                int remainingBytes = allBytes - (20 - initialBuffer.IndexOf("35="));
                remainingBytes += 7; // 7 is because of 10=081@
     
                string restOfBuffer = recvString(remainingBytes);
                
                if( restOfBuffer == null)
                {
                    throw new Exception("Receive failed");
                }
                
                if( remainingBytes > 0 && restOfBuffer.Length == 0)
                {
                    throw new Exception("Receive failed");
                }
     
                message = new FixMessage();
     
                message.loadFromString(initialBuffer + restOfBuffer);
               
                IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
            }
            catch
            {
            }
            enableSocketBlocking();
            m_mutex.ReleaseMutex();
            return message;
        }
 
        public void disconnect(FixMessage logoffMessage)
        {
            if(Connected)
            {
                m_heartbeatTimer.Stop();
                try
                {   
                    if(logoffMessage == null)
                    {
                        logoffMessage = getLogoffMessage();
                    }
                    send(logoffMessage);
                    FixMessage logoffResponse = recv();
                    m_socket.Close();
                    m_serverSocket.Close();
                }
                catch { }
                saveSequenceNumberToFile();
                Connected = false;
            }
        }
 
        public void restoreSequenceNumberFromFile()
        {
            var fileName = getSequenceFileName();
            if (System.IO.File.Exists(fileName))
            {
                int outgoingSequenceNumber = 1;
                int incomingSequenceNumber = 1;
                try
                {
                    string text = System.IO.File.ReadAllText(fileName);
     
                    if (System.Int32.TryParse(text.Split(',')[0], out outgoingSequenceNumber))
                    {
                        OutgoingSequenceNumber = outgoingSequenceNumber;
                    }
     
                    if (System.Int32.TryParse(text.Split(',')[1], out incomingSequenceNumber))
                    {
                        IncomingSequenceNumber = incomingSequenceNumber;
                    }
                }
                catch
                {
                    Console.WriteLine("Warning : Error during opening sequence number file , sequence numbers set to 1");
                }
            }
        }
 
        public void saveSequenceNumberToFile()
        {
            var fileName = getSequenceFileName();
            if (System.IO.File.Exists(fileName))
            {
                System.IO.File.Delete(fileName);
            }
            System.IO.File.WriteAllText(fileName, OutgoingSequenceNumber.ToString() + "," + IncomingSequenceNumber.ToString());
        }
    }
 
    public class FixClient
    {
        private int m_orderId = 0;
        private FixSession m_session = new FixSession();
 
        public FixSession FixSession { get { return m_session; } }
 
        public void initialise(string fixVersion, string address, int port, string compId, string subId, string targetCompid, string targetSubid, int heartbeatInterval = 30, int encryptionMethod = 0)
        {
            m_session.TargetAddress = address;
            m_session.TargetPort = port;
            m_session.SenderCompid = compId;
            m_session.SenderSubid = subId;
            m_session.TargetCompid = targetCompid;
            m_session.TargetSubid = targetSubid;
            m_session.HeartbeatInterval = heartbeatInterval;
            m_session.EncryptionMethod = encryptionMethod;
            m_session.FixVersion = fixVersion;
        }
 
        public bool connect(FixMessage logonMessage = null)
        {
            return m_session.connect(logonMessage);
        }
 
        public void disconnect(FixMessage logoffMessage = null)
        {
            m_session.disconnect(logoffMessage);
        }
 
        public bool send(FixMessage message)
        {
            m_orderId++;
            message.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, m_orderId);
            return m_session.send(message);
        }
 
        public FixMessage recv()
        {
            return m_session.recv();
        }
    }
    
    public class FixServer
    {
        private FixSession m_session = new FixSession();
        public FixSession FixSession { get { return m_session; } }
 
        public bool start(int port, string compId, string subId, FixMessage logOnResponse = null)
        { 
            m_session.TargetPort = port;
            m_session.SenderCompid = compId;
            m_session.SenderSubid = subId;
            return m_session.accept(logOnResponse);
        }
 
        public void disconnect(FixMessage logoffResponse = null)
        {
            m_session.disconnect(logoffResponse);
        }
 
        public bool send(FixMessage message)
        {
            return m_session.send(message);
        }
 
        public FixMessage recv()
        {
            FixMessage message = m_session.recv();
            FixSession.saveSequenceNumberToFile();
            return message;
        }
    }
"@
 
    Add-Type -TypeDefinition $source;
}