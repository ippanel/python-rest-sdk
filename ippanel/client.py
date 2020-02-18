from ippanel.httpclient import HTTPClient
from ippanel.models import Message, Recipient, InboxMessage, Pattern

# base url for api
BASE_URL = "http://rest.ippanel.com"
# default timeout for http client
DEFAULT_TIMEOUT = 30
# client version
CLIENT_VERSION = "1.0.1"


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
        res = self.client.get("/v1/credit")

        try:
            return res.data["credit"]
        except:
            raise ValueError("returned response not valid")

    def send(self, originator, recipients, message):
        r"""Send a message from originator to many recipients.

        :param originator: originator number, string.
        :param recipients: recipients list, list.
        :param message: message to send, string.
        :return: :class:`int <int>` object
        :rtype: int
        """
        res = self.client.post("/v1/messages", {
            "originator": originator,
            "recipients": recipients,
            "message": message,
        })

        try:
            return res.data["bulk_id"]
        except:
            raise ValueError("returned response not valid")

    def get_message(self, bulk_id):
        r"""Get a message brief info

        :param bulk_id: bulk id, int.
        :return: :class:`Message <Message>` object
        :rtype: models.Message
        """
        res = self.client.get("/v1/messages/" + str(bulk_id))

        try:
            return Message(res.data["message"])
        except:
            raise ValueError("returned response not valid")

    def fetch_statuses(self, bulk_id, page=0, limit=10):
        r"""Fetch message recipients status

        :param bulk_id: bulk id, int.
        :param page: page number(start from 0), int.
        :param limit: fetch limit, int.
        :return: :class:`[]Recipient <[]Recipient>` object
        :rtype: []models.Recipient
        """
        res = self.client.get("/v1/messages/%s/recipients" % str(bulk_id), {
            "page": page,
            "limit": limit,
        })

        try:
            recipients = []
            for recipient in res.data["recipients"]:
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
        res = self.client.get("/v1/messages/inbox", {
            "page": page,
            "limit": limit,
        })

        try:
            messages = []
            for message in res.data["messages"]:
                messages.append(InboxMessage(message))

            return messages, res.meta
        except:
            raise ValueError("returned response not valid")

    def create_pattern(self, pattern, is_shared=False):
        r"""Create a pattern

        :param pattern: pattern schema, string.
        :param is_shared: determine that pattern shared or not, bool.
        :return: :class:`Pattern <Pattern>` object
        :rtype: []models.Pattern
        """
        res = self.client.post("/v1/messages/patterns", {
            "pattern": pattern,
            "is_shared": is_shared,
        })

        try:
            return Pattern(res.data["pattern"])
        except:
            raise ValueError("returned response not valid")

    def send_pattern(self, pattern_code, originator, recipient, values={}):
        r"""Send message with pattern

        :param pattern_code: pattern code, string.
        :param originator: originator number, string.
        :param recipient: recipient number, string.
        :param values: pattern values, dict.
        :return: :class:`int <int>` object
        :rtype: int
        """

        res = self.client.post("/v1/messages/patterns/send", {
            "pattern_code": pattern_code,
            "originator": originator,
            "recipient": recipient,
            "values": values,
        })

        try:
            return res.data["bulk_id"]
        except:
            raise ValueError("returned response not valid")
