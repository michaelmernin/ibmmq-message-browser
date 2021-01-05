import datetime
import json
import pytz
from datetime import *

from error_handler import ErrorHandler
from mq_client import MQReader
from mq_manager import QueueManager


class RequestHandler:
    @classmethod
    def process_request(cls, request):
        params = cls.parse_request(request)
        cls.validate_params(params)
        return cls.search(params)

    @classmethod
    def parse_request(cls, request):
        params = {}
        # Merges form(UI calls), args(Postman form-data) params
        arguments = {**request.form.to_dict(), **request.args.to_dict()}

        # Extract queue_list[] from splash.html if present
        queue_list = request.form.getlist("queue_list[]")
        if len(queue_list) > 0:
            arguments['queue_list'] = queue_list
            arguments.pop("queue_list[]")

        # Support for JAVA JSON body requests
        if request.json:
            arguments = {**arguments, **request.json}

        # Support for POSTMAN raw JSON body requests
        if len(arguments) == 0:
            arguments = json.loads(request.data.decode())

        if len(arguments) == 0:
            raise ErrorHandler("Error parsing params")

        # Extract params from request
        search_string = arguments.get('searchParam', None)
        if not search_string:
            raise ErrorHandler("Required param 'searchParam' not found .... If you are receiving this error in postman "
                               "and have included the searchParam, "
                               "please uncheck option in Headers Content-type - "
                               "application/x-www-form-urlencoded and try again")

        params['search_string'] = search_string.strip().lower()
        params['queue_suffix'] = arguments.get('queueSuffix', 'DEFAULT.QUEUE.SUFFIX').strip()
        params['delimiter'] = arguments.get('includeDelimiter', 'false').strip().lower()
        not_before = arguments.get('notBefore', 'false').strip().lower()
        if not_before != 'false' and not_before != '':
            not_before = cls.convert_not_before(not_before)

        params['not_before'] = not_before
        params['base_queues'] = arguments.get('BASE.QUEUE.PREFIX', 'false').strip().lower()

        params['queue_list'] = arguments.get('queue_list', [])

        return params

    @classmethod
    def convert_not_before(cls, not_before):
        try:
            # convert notBefore param into 'aware' datetime object
            return pytz.UTC.localize(datetime.fromisoformat(not_before))
        except Exception as e:
            raise ErrorHandler(
                "Error parsing DateTime 'notBefore' -> " + not_before + " .  Value must be of format "
                                                                        "DateTimeFormatter.ofPattern('yyyy-MM-dd HH:mm:ss') " + str(
                    e))

    @classmethod
    def validate_params(cls, params):
        if len(params['queue_list']) == 0:
            raise ErrorHandler("No valid queues selected for search, ensure queue names are in ALL CAPS")

    @classmethod
    def search(cls, params):
        response = {}
        # Start connection to queue manager
        try:
            queue_manager = QueueManager()
        except Exception as e:
            raise ErrorHandler(
                "Unable to connect to QueueManager, please try again. Error code: " + str(e))

        # Iterate through the search queue list and browse all messages,
        # returning all messages that match the search param
        for name in params.get('queue_list'):
            queue_suffix = params.get('queue_suffix')
            try:
                browser = MQReader(queue_manager, name, params.get('base_queues'), queue_suffix)
                found_msgs = browser.search_for_msgs(params.get('search_string'), params.get('delimiter'),
                                                     params.get('not_before'))
                browser.close_browser_connection()
            except Exception as e:
                response["QUEUE___" + name + '.' + queue_suffix] = "queue was unresponsive " + str(e)
                continue
            response["QUEUE___" + name + '.' + queue_suffix] = found_msgs

        # Close connection to queue manager
        try:
            queue_manager.close_manager_connection()
        except Exception as e:
            response['ERROR'] = "ISSUE CLOSING QUEUE MANAGER error code: " + str(e)

        return response


class QueueNames:
    names = None
