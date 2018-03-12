#!/usr/bin/python
'''
Copyright (c) 2018 Akin Ocal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

class FixConstants:
    # GENERAL
    EQUALS = '='
    DELIMITER = chr(1)
    # VERSIONS
    VERSION_4_0 = "FIX.4.0"
    VERSION_4_1 = "FIX.4.1"
    VERSION_4_2 = "FIX.4.2"
    VERSION_4_3 = "FIX.4.3"
    VERSION_4_4 = "FIX.4.4"
    VERSION_5_0 = "FIX.5.0"
    # TIMESTAMP PRECISION
    TIMESTAMP_PRECISION_SECONDS=1
    TIMESTAMP_PRECISION_MILLISECONDS=2
    TIMESTAMP_PRECISION_MICROSECONDS=3
    # HEADER TAGS
    TAG_VERSION = 8                 #REQUIRED
    TAG_BODY_LENGTH = 9             #REQUIRED
    TAG_MESSAGE_TYPE = 35           #REQUIRED
    TAG_SENDER_COMPID = 49          #REQUIRED
    TAG_TARGET_COMPID = 56          #REQUIRED
    TAG_ON_BEHALF_OF_COMPID = 115
    TAG_DELIVER_TO_COMPID = 128
    TAG_SECURE_DATA_LEN = 90
    TAG_SECURE_DATA = 91
    TAG_SEQUENCE_NUMBER = 34        #REQUIRED
    TAG_SENDER_SUBID = 50
    TAG_SENDER_LOCATION_ID = 142
    TAG_TARGET_SUBID = 57
    TAG_TARGET_LOCATION_ID = 143
    TAG_ON_BEHALF_OF_SUBID = 116
    TAG_ON_BEHALF_OF_LOCATIONID = 144
    TAG_DELIVER_TO_SUBID = 129
    TAG_DELIVER_TO_LOCATIONID = 145
    TAG_POSS_DUPP_FLAG=43
    TAG_POSS_RESEND=97
    TAG_SENDING_TIME = 52           #REQUIRED
    TAG_ORIG_SENDING_TIME = 122
    TAG_XML_DATA_LEN = 212
    TAG_XML_DATA = 213
    TAG_MESSAGE_ENCODING = 347
    TAG_LAST_MSQ_SEQ_NUM_PROCESSED = 369
    TAG_NO_HOPS = 627
    TAG_HOP_COMP_ID = 628
    TAG_HOP_SENDING_TIME = 629
    TAG_HOP_REF_ID = 630
    # HEADER TAGS ORDER , NEED TO BUILD FIX HEADER TAGS IN THIS ORDER
    HEADER_TAGS = [ 
                        TAG_VERSION, 
                        TAG_BODY_LENGTH,
                        TAG_MESSAGE_TYPE, 
                        TAG_SENDER_COMPID,
                        TAG_TARGET_COMPID,
                        TAG_ON_BEHALF_OF_COMPID,
                        TAG_DELIVER_TO_COMPID,
                        TAG_SECURE_DATA_LEN,
                        TAG_SECURE_DATA,
                        TAG_SEQUENCE_NUMBER,
                        TAG_SENDER_SUBID,
                        TAG_SENDER_LOCATION_ID,
                        TAG_TARGET_SUBID,
                        TAG_TARGET_LOCATION_ID,
                        TAG_ON_BEHALF_OF_SUBID,
                        TAG_ON_BEHALF_OF_LOCATIONID,
                        TAG_DELIVER_TO_SUBID,
                        TAG_DELIVER_TO_LOCATIONID,
                        TAG_POSS_DUPP_FLAG,
                        TAG_POSS_RESEND,
                        TAG_SENDING_TIME,
                        TAG_ORIG_SENDING_TIME,
                        TAG_XML_DATA_LEN,
                        TAG_XML_DATA,
                        TAG_MESSAGE_ENCODING,
                        TAG_LAST_MSQ_SEQ_NUM_PROCESSED,
                        TAG_NO_HOPS,
                        TAG_HOP_COMP_ID,
                        TAG_HOP_SENDING_TIME,
                        TAG_HOP_REF_ID
                      ]
    # FIX BIDIRECTIONAL HEADER TAGS, NEED TO KNOW CORRESPONDING HEADER TAGS FOR FIX SESSIONS
    BIDIRECTIONAL_HEADER_TAGS = [ 
                                      [TAG_SENDER_COMPID, TAG_TARGET_COMPID],
                                      [TAG_SENDER_SUBID, TAG_TARGET_SUBID],
                                      [TAG_SENDER_LOCATION_ID, TAG_TARGET_LOCATION_ID]
                                    ]
    # TRAILER TAGS
    TAG_SIGNAGURE_LENGTH = 93
    TAG_SIGNATURE = 89
    TAG_BODY_CHECKSUM = 10          #REQUIRED
    TRAILER_TAGS = [ 
                        TAG_SIGNAGURE_LENGTH,
                        TAG_SIGNATURE,
                        TAG_BODY_CHECKSUM
                      ]
    # BODY TAGS
    TAG_AVERAGE_PRICE = 6
    TAG_CLIENT_ORDER_ID = 11
    TAG_CUMULATIVE_QUANTITY = 14
    TAG_EXEC_ID = 17
    TAG_EXEC_INST = 18
    TAG_EXEC_TRANSTYPE = 20
    TAG_HAND_INST = 21
    TAG_LAST_PRICE = 31
    TAG_LAST_QUANTITY = 32
    TAG_ORDER_ID = 37
    TAG_ORDER_QUANTITY = 38
    TAG_ORDER_STATUS = 39
    TAG_ORDER_TYPE = 40
    TAG_ORIG_CLIENT_ORDER_ID = 41
    TAG_ORDER_PRICE = 44
    TAG_SECURITY_ID = 48
    TAG_ORDER_SIDE = 54
    TAG_SYMBOL = 55
    TAG_FREE_TEXT = 58
    TAG_TIME_IN_FORCE = 59
    TAG_TRANSACTION_TIME = 60
    TAG_ENCRYPT_METHOD = 98
    TAG_HEARTBEAT_INTERVAL = 108
    TAG_TEST_REQ_ID = 112
    TAG_EXEC_TYPE = 150
    TAG_LEAVES_QTY = 151
    TAG_USERNAME = 553
    TAG_PASSWORD = 554
    TAG_USER_REQUEST_ID = 923
    TAG_USER_PASSWORD = 924
    # MESSAGE TYPES
    MESSAGE_HEARTBEAT = "0"
    MESSAGE_TEST_REQUEST = "1"
    MESSAGE_ADMIN_REJECT = "3"
    MESSAGE_USER_LOGON = "BE"
    MESSAGE_USER_RESPONSE = "BF"
    MESSAGE_LOG_ON = "A"
    MESSAGE_LOG_OFF = "5"
    MESSAGE_EXECUTION_REPORT = "8"
    MESSAGE_ORDER_CANCEL_REJECT = "9"
    MESSAGE_NEW_ORDER = "D"
    MESSAGE_AMEND_ORDER = "G"
    MESSAGE_CANCEL_ORDER = "F"
    MESSAGE_BUSINES_REJECT = "j"
    # ORDER STATUS
    ORDER_STATUS_NEW = '0'
    ORDER_STATUS_PARTIALLY_FILLED = '1'
    ORDER_STATUS_FILLED = '2'
    ORDER_STATUS_DONE_FOR_DAY = '3'
    ORDER_STATUS_CANCELED = '4'
    ORDER_STATUS_REPLACED = '5'
    ORDER_STATUS_PENDING_CANCEL = '6'
    ORDER_STATUS_STOPPED = '7'
    ORDER_STATUS_REJECTED = '8'
    # ORDER TYPE
    ORDER_TYPE_MARKET= '1'
    ORDER_TYPE_LIMIT = '2'
    # SIDE
    ORDER_SIDE_BUY = '1'
    ORDER_SIDE_SELL = '2'
    # TIME IN FORCE
    ORDER_TIF_DAY = '0'
    # ENCRYPTION METHODS
    ENCRYPTION_NONE = '0'

    @staticmethod
    def isHeaderTag(tag):
        for headerTag in FixConstants.HEADER_TAGS:
            if headerTag == tag:
                return True
        return False

    @staticmethod
    def isTrailerTag(tag):
        for trailerTag in FixConstants.TRAILER_TAGS:
            if trailerTag == tag:
                return True
        return False