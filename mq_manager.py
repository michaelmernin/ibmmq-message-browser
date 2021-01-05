import pymqi
from pymqi import *
from error_handler import ErrorHandler


class QueueManager:
    """ Handles connection to queue manager """
    conn_details = None

    def __init__(self):
        self.connection = self.start_manager_connection()

    def start_manager_connection(self):
        queue_manager = self.conn_details.get('queue_manager')
        channel = self.conn_details.get('channel')
        host = self.conn_details.get('host')
        port = self.conn_details.get('port')
        conn_info = '%s(%s)' % (host, port)
        return pymqi.connect(queue_manager, channel, conn_info)

    def close_manager_connection(self):
        self.connection.disconnect()
