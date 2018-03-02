function minimalFixInitialise()
{
  $source = @"
  using System;
 
    public class FixConstants
    {
        // GENERAL
        public const char FIX_EQUALS = '=';
        public const char FIX_DELIMITER = ((char)1);
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
 
    public class FixMessage
    {
        private System.Collections.Generic.Dictionary<int, string> m_tagValuePairs = new System.Collections.Generic.Dictionary<int, string>();
        System.Text.StringBuilder m_builder = new System.Text.StringBuilder();
 
        private void appendTagValueToBuilder(int tag, string value, bool delimiter = true)
        {
            m_builder.Append(tag.ToString() + FixConstants.FIX_EQUALS + value);
            if (delimiter)
            {
                m_builder.Append(FixConstants.FIX_DELIMITER);
            }
        }
 
        static public string getCurrentUTCDateTime()
        {
            string datetime = "";
            //datetime = System.DateTime.Now.ToUniversalTime().ToString("yyyyMMdd-HH:mm:ss.fff");
            datetime = System.DateTime.Now.ToString("yyyyMMdd-HH:mm:ss.fff");
            return datetime;
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
 
        public int calculateBodyLength()
        {
            int bodyLength = 0;
 
            foreach (var tagValue in m_tagValuePairs)
            {
                //  We exclude header and checksum
                if (tagValue.Key == FixConstants.FIX_TAG_VERSION)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_BODY_LENGTH)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_BODY_CHECKSUM)
                {
                    continue;
                }
 
                bodyLength += tagValue.Key.ToString().Length + 2 + tagValue.Value.Length; // +2 is because of = and delimiter
            }
 
            return bodyLength;
        }
 
        public void setFixVersion(string fixVersion)
        {
            setTag(FixConstants.FIX_TAG_VERSION, fixVersion);
        }
 
        public bool hasTag(int tag)
        {
            if (m_tagValuePairs.ContainsKey(tag))
            {
                return true;
            }
            return false;
        }
 
        public void setTag(int tag, string value)
        {
            m_tagValuePairs[tag] = value;
        }
 
        public void setTag(int tag, char value)
        {
            m_tagValuePairs[tag] = value.ToString();
        }
 
        public void setTag(int tag, int value)
        {
            m_tagValuePairs[tag] = value.ToString();
        }
 
        public string getTagValue(int tag)
        {
            return m_tagValuePairs[tag];
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
 
        public string toString(bool sendingAsAMessage, bool updateTransactionTime = false)
        {
            m_builder = new System.Text.StringBuilder();
            // FIX VERSION
            appendTagValueToBuilder(FixConstants.FIX_TAG_VERSION, getTagValue(FixConstants.FIX_TAG_VERSION));
 
            // FIX SENDING TIME AND TRANSACTION, have to be before body length calculation ,but not appended for the correct order
            if (sendingAsAMessage)
            {
                var currentUTCDateTime = FixMessage.getCurrentUTCDateTime();
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
 
            // FIX MESSAGE TYPE
            appendTagValueToBuilder(FixConstants.FIX_TAG_MESSAGE_TYPE, getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE));
 
            // FIX SEQUENCE NUMBER
            appendTagValueToBuilder(FixConstants.FIX_TAG_SEQUENCE_NUMBER, getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
 
            // FIX SENDER COMPID
            appendTagValueToBuilder(FixConstants.FIX_TAG_SENDER_COMPID, getTagValue(FixConstants.FIX_TAG_SENDER_COMPID));
 
            // FIX SENDING TIME
            appendTagValueToBuilder(FixConstants.FIX_TAG_SENDING_TIME, getTagValue(FixConstants.FIX_TAG_SENDING_TIME));
 
            // FIX TARGET COMPID
            appendTagValueToBuilder(FixConstants.FIX_TAG_TARGET_COMPID, getTagValue(FixConstants.FIX_TAG_TARGET_COMPID));
 
            foreach (var tagValue in m_tagValuePairs)
            {
                if (tagValue.Key == FixConstants.FIX_TAG_VERSION)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_BODY_LENGTH)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_MESSAGE_TYPE)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_SEQUENCE_NUMBER)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_SENDING_TIME)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_SENDER_COMPID)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_TARGET_COMPID)
                {
                    continue;
                }
 
                if (tagValue.Key == FixConstants.FIX_TAG_BODY_CHECKSUM)
                {
                    continue;
                }
 
                appendTagValueToBuilder(tagValue.Key, tagValue.Value);
            }
 
            // FIX CHECKSUM
            if (sendingAsAMessage)
            {
                var checksum = calculateChecksum(m_builder.ToString());
                appendTagValueToBuilder(FixConstants.FIX_TAG_BODY_CHECKSUM, checksum);           
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
        public string TargetAddress { get; set; }
        public int TargetPort { get; set; }
        public string TargetCompid { get; set; }
        public string SenderCompid { get; set; }
        public int HeartbeatInterval { get; set; }
        public int EncryptionMethod { get; set; }
        public int IncomingSequenceNumber { get; set; }
        public int OutgoingSequenceNumber { get; set; }
        public string FixVersion { get; set; }
 
        public FixSession()
        {
            Connected = false;
            HeartbeatInterval = 30;
            EncryptionMethod = FixConstants.FIX_ENCRYPTION_NONE;
            IncomingSequenceNumber = 1;
            OutgoingSequenceNumber = 1;
            m_socket.NoDelay = true;
        }
 
        public FixMessage getBaseMessage(string messageType)
        {
            FixMessage message = new FixMessage();
            message.setFixVersion(FixVersion);
            message.setTag(FixConstants.FIX_TAG_MESSAGE_TYPE, messageType);
            // Sequence number will be added during sending
            message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, SenderCompid);
            message.setTag(FixConstants.FIX_TAG_SENDING_TIME, "");
            message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, TargetCompid);
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
 
        public bool connect()
        {
            bool result = false;
            try
            {
                m_socket.Connect(TargetAddress, TargetPort);
 
                send(getLogonMessage());
                FixMessage message = recv();
                if (message != null)
                {
                    if (message.hasTag(FixConstants.FIX_TAG_MESSAGE_TYPE))
                    {
                        var value = message.getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE);
                        if (value == FixConstants.FIX_MESSAGE_LOG_ON.ToString())
                        {
                            if (message.hasTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER))
                            {
                                Connected = result = true;
                                IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
                                m_heartbeatTimer.Interval = HeartbeatInterval * 1000;
                                m_heartbeatTimer.Elapsed += new System.Timers.ElapsedEventHandler(heartbeatTimerFunction);
                                m_heartbeatTimer.Start();
                            }
                        }
                    }
                }
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e.Message);
            }
            return result;
        }
 
        public void accept(string clientcompId = "")
        {
            try
            {
                System.Net.IPHostEntry ipHostInfo = System.Net.Dns.GetHostEntry(System.Net.Dns.GetHostName());
                System.Net.IPAddress ipAddress = ipHostInfo.AddressList[0];
                System.Net.IPEndPoint localEndPoint = new System.Net.IPEndPoint(Convert.ToInt32(TargetAddress), TargetPort);
 
                m_serverSocket.Bind(localEndPoint);
                m_serverSocket.Listen(100);
 
                m_socket = m_serverSocket.Accept();
 
                FixMessage message = recv();
 
                if (message != null)
                {
                    if (message.hasTag(FixConstants.FIX_TAG_MESSAGE_TYPE))
                    {
                        var value = message.getTagValue(FixConstants.FIX_TAG_MESSAGE_TYPE);
                        if (value == FixConstants.FIX_MESSAGE_LOG_ON.ToString())
                        {
                            if (message.hasTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER))
                            {
                                Connected = true;
                                IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
                                HeartbeatInterval = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_HEARTBEAT_INTERVAL));
                                
                                if( clientcompId.Length == 0)
                                {
                                    TargetCompid = message.getTagValue(FixConstants.FIX_TAG_SENDER_COMPID);
                                }
                                else
                                {
                                    TargetCompid = clientcompId;
                                }
                                
                                FixVersion = message.getTagValue(FixConstants.FIX_TAG_VERSION);
 
                                if (message.hasTag(FixConstants.FIX_TAG_ENCRYPT_METHOD))
                                {
                                    EncryptionMethod = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_ENCRYPT_METHOD));
                                }
                                
                                send(getLogonMessage());
                            }
                        }
                    }
                }
            }
            catch (System.Exception e)
            {
                System.Console.WriteLine(e.Message);
            }
        }
 
        private void heartbeatTimerFunction(object sender, System.EventArgs e)
        {
            try
            {
                send(getHeartbeatMessage());
            }
            catch { }
        }
 
        public void send(FixMessage message)
        {
            message.setTag(FixConstants.FIX_TAG_VERSION, FixVersion);
            message.setTag(FixConstants.FIX_TAG_SENDER_COMPID, SenderCompid);
            message.setTag(FixConstants.FIX_TAG_TARGET_COMPID, TargetCompid);
            //////////////////////////////////////////////////////////////
            m_mutex.WaitOne();
            message.setTag(FixConstants.FIX_TAG_SEQUENCE_NUMBER, OutgoingSequenceNumber);
            var str = message.toString(true, true);
            byte[] bytes = System.Text.Encoding.ASCII.GetBytes(str);
            m_socket.Send(bytes);
            OutgoingSequenceNumber += 1;
            m_mutex.ReleaseMutex();
            //////////////////////////////////////////////////////////////
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
 
        public FixMessage recv()
        {
            string initialBuffer = recvString(20); // Length of 8=FIX.4.2@9=7000@35= so we always get 35=A
 
            if (initialBuffer == null)
            {
                return null;
            }
 
            if (initialBuffer.Length == 0)
            {
                return null;
            }
 
            int allBytes = System.Convert.ToInt32(initialBuffer.Split((char)1)[1].Split('=')[1]);
            int remainingBytes = allBytes - (20 - initialBuffer.IndexOf("35="));
            remainingBytes += 7; // 7 is because of 10=081@
 
            string restOfBuffer = recvString(remainingBytes);
 
            FixMessage message = new FixMessage();
 
            message.loadFromString(initialBuffer + restOfBuffer);
           
            IncomingSequenceNumber = System.Convert.ToInt32(message.getTagValue(FixConstants.FIX_TAG_SEQUENCE_NUMBER));
 
            return message;
        }
 
        public void disconnect()
        {
            m_heartbeatTimer.Stop();
            send(getLogoffMessage());
            FixMessage logoffResponse = recv();
            m_socket.Close();
            try
            {
                m_serverSocket.Close();
            }
            catch { }
            Connected = false;
            saveSequenceNumberToFile();
        }
 
        public void restoreSequenceNumberFromFile()
        {
            var fileName = getSequenceFileName();
            if (System.IO.File.Exists(fileName))
            {
                int outgoingSequenceNumber = 1;
                int incomingSequenceNumber = 1;
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
 
    public class FixServer
    {
        private FixSession m_session = new FixSession();
        public FixSession FixSession { get { return m_session; } }
 
        public void start(int port, string compId, string clientcompId)
        {
            m_session.TargetPort = port;
            m_session.SenderCompid = compId;
            m_session.restoreSequenceNumberFromFile();
            m_session.accept(clientcompId);
        }
 
        public void disconnect()
        {
            m_session.disconnect();
        }
 
        public void send(FixMessage message)
        {
            m_session.send(message);
        }
 
        public FixMessage recv()
        {
            FixMessage message = m_session.recv();
            FixSession.saveSequenceNumberToFile();
            return message;
        }
    }
 
    public class FixClient
    {
        private int m_orderId = 0;
        private FixSession m_session = new FixSession();
 
        public FixSession FixSession { get { return m_session; } }
 
        public void initialise(string fixVersion, string address, int port, string compId, string targetCompid, int heartbeatInterval = 30, int encryptionMethod = 0)
        {
            m_session.TargetAddress = address;
            m_session.TargetPort = port;
            m_session.SenderCompid = compId;
            m_session.TargetCompid = targetCompid;
            m_session.HeartbeatInterval = heartbeatInterval;
            m_session.EncryptionMethod = encryptionMethod;
            m_session.FixVersion = fixVersion;
            m_session.restoreSequenceNumberFromFile();
        }
 
        public bool connect()
        {
            return m_session.connect();
        }
 
        public void disconnect()
        {
            m_session.disconnect();
        }
 
        public void send(FixMessage message)
        {
            m_orderId++;
            message.setTag(FixConstants.FIX_TAG_CLIENT_ORDER_ID, m_orderId);
            m_session.send(message);
        }
 
        public FixMessage recv()
        {
            return m_session.recv();
        }
    }
 
"@
 
    Add-Type -TypeDefinition $source;
}