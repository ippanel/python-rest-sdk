from ippanel.httpclient import HTTPClient
from ippanel.models import Message, Recipient, InboxMessage

# base url for api
BASE_URL = "https://api2.ippanel.com/api/v1/"
# default timeout for http client
DEFAULT_TIMEOUT = 30
# client version
CLIENT_VERSION = "2.0.7"


class Client:
    ''' ippanel client class
    '''

    def __init__(self, apikey, http_client=None):
        self.client = http_client or HTTPClient(
            apikey,
            BASE_URL,
            DEFAULT_TIMEOUT,
            CLIENT_VERSION,
        )
        self.apikey = apikey

    def get_credit(self):
        r"""Get authenticated user credit

        :return: :class:`float <float>` object
        :rtype: float
        """
        res = self.client.get("sms/accounting/credit/show")

        try:
            return res.data["credit"]
        except:
            raise ValueError("returned response not valid")

    def send(self, sender, recipients, message, summary):
        r"""Send a message from sender to many recipients.

        :param sender: sender number, string.
        :param recipients: recipients list, list.
        :param message: message to send, string.
        :param summary: description of the message to be logged, string.
        :return: :class:`int <int>` object
        :rtype: int
        """
        res = self.client.post("sms/send/webservice/single", {
            "sender": sender,
            "recipient": recipients,
            "message": message,
            "description": {
                "summary": summary,
                "count_recipient": f"{len(recipients)}"
            },
        })

        try:
            return res.data["message_id"]
        except:
            raise ValueError("returned response not valid")

    def get_message(self, message_id):
        r"""Get a message brief info

        :param message_id: message id, int.
        :return: :class:`Message <Message>` object
        :rtype: models.Message
        """
        res = self.client.get("sms/message/all", {
            'message_id': message_id,
        })

        try:
            return Message(res.data[0])
        except:
            raise ValueError("returned response not valid")

    def fetch_statuses(self, message_id, page=0, limit=10):
        r"""Fetch message recipients status

        :param message_id: message id, int.
        :param page: page number(start from 0), int.
        :param limit: fetch limit, int.
        :return: :class:`[]Recipient <[]Recipient>` object
        :rtype: []models.Recipient
        """
        res = self.client.get(f"sms/message/show-recipient/message-id/{message_id}", {
            "page": page,
            "per_page": limit,
        })

        try:
            recipients = []
            for recipient in res.data["deliveries"]:
                recipients.append(Recipient(recipient))

            return recipients, res.meta
        except:
            raise ValueError("returned response not valid")

    def fetch_inbox(self, page=0, limit=10):
        r"""Fetch inbox messages

        :param page: page number(start from 0), int.
        :param limit: fetch limit, int.
        :return: :class:`[]InboxMessage <[]InboxMessage>` object
        :rtype: []models.InboxMessage
        """
        res = self.client.get("/inbox", {
            "page": page,
            "per_page": limit,
        })

        try:
            messages = []
            for message in res.data:
                messages.append(InboxMessage(message))

            return messages, res.meta
        except:
            raise ValueError("returned response not valid")

    def create_pattern(self, pattern, description, variables, delimiter="%", is_shared=False):
        r"""Create a pattern

        :param pattern: pattern schema, string.
        :param description: description of pattern, string.
        :param variables: variable list, string.
        :param delimiter: delimiter of variables in pattern, string.
        :param is_shared: determine that pattern shared or not, bool.
        :return: :class:`int <int>` object
        :rtype: int
        """
        params = {
            "pattern": pattern,
            "description": description,
            "delimiter": delimiter,
            "variable": [],
            "is_shared": is_shared,
        }
        for variable_name, type in variables.items():
            params['variable'].append({'name': variable_name, 'type': type})

        res = self.client.post("sms/pattern/normal/store", params)

        try:
            return res.data[0]["code"]
        except:
            raise ValueError("returned response not valid")

    def send_pattern(self, pattern_code, sender, recipient, values={}):
        r"""Send message with pattern

        :param pattern_code: pattern code, string.
        :param sender: sender number, string.
        :param recipient: recipient number, string.
        :param values: pattern values, dict.
        :return: :class:`int <int>` object
        :rtype: int
        """

        res = self.client.post("sms/pattern/normal/send", {
            "code": pattern_code,
            "sender": sender,
            "recipient": recipient,
            "variable": values,
        })

        try:
            return res.data["message_id"]
        except:
            raise ValueError("returned response not valid")
