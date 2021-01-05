import json

import pymqi
from dateutil.parser import parse
from pymqi import *


class MQReader:
    """ Handles connection to queue and browses all available messages """

    def __init__(self, qmgr, name, base_queues='false', queue_suffix='DEFAULT.QUEUE.SUFFIX'):
        # If true, searches base queues
        queue_name = bytes('BASE.QUEUE.PREFIX' + '.' + name + 'BASE.QUEUE.SUFFIX',
                           'utf-8') if base_queues == 'true' else bytes(
            qmgr.conn_details.get('queue_prefix') + '.' + name + '.' + queue_suffix, 'utf-8')

        gqdesc = od(ObjectName=queue_name)

        self.browse_q = Queue(qmgr.connection, gqdesc, CMQC.MQOO_BROWSE)
        # self.inquire_q = Queue(self.qmgr, gqdesc)

    # def inquire_queue_depth(self):
    #     qDepth = self.inquire_q.inquire(CMQC.MQIA_CURRENT_Q_DEPTH)
    #     return qDepth

    def close_browser_connection(self):
        # self.inquire_q.close()
        self.browse_q.close()

    def search_for_msgs(self, search, include_delimiter, not_before='false'):
        messages = []
        getOpts = gmo(Options=CMQC.MQGMO_BROWSE_NEXT)
        getOpts.WaitInterval = CMQC.MQWI_UNLIMITED
        msgDesc = md()
        count = 0
        while True:
            try:
                message = self.browse_q.get(None, msgDesc, getOpts).decode("utf-8")
                count = count + 1
            except MQMIError as e:
                if 'MQRC_NO_MSG_AVAILABLE' not in str(e):
                    print(str(e))
                print("messages counted " + str(count))
                break
            # check for 'searchParam' within the JSON string, if true continue processing message
            if search in message.lower():
                try:
                    msg = json.loads(message)
                    # compare notBefore param and timestamp of message,
                    # only messages with timestamps after the notBefore date are included in the result
                    if not_before != 'false':
                        msg_time = msg.get('time', None)
                        if msg_time is None or not_before > parse(msg_time):
                            msgDesc['MsgId'] = bytes('', 'utf-8')
                            msgDesc['CorrelId'] = bytes('', 'utf-8')
                            continue
                    messages.insert(0, msg)
                    if include_delimiter == 'true':
                        messages.insert(1, "##############################################################")
                        messages.insert(2, "####################  MESSAGE SEPARATOR  #####################")
                        messages.insert(3, "##############################################################")
                except:
                    messages.insert(0, message)
                    if include_delimiter == 'true':
                        messages.insert(1, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        messages.insert(2, "XXXXXXXXXXXXXXX   IMPROPER MESSAGE FOUND   XXXXXXXXXXXXXXXXXXX")
                        messages.insert(3, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                        msgDesc['MsgId'] = bytes('', 'utf-8')
                        msgDesc['CorrelId'] = bytes('', 'utf-8')
                    continue
            # reset message cursor in order to browse next message
            msgDesc['MsgId'] = bytes('', 'utf-8')
            msgDesc['CorrelId'] = bytes('', 'utf-8')

        return messages
