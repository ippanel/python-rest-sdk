try:
    import simplejson as json
except ImportError:
    import json


class Base(object):
    """
    base model 
    """

    def from_json(self, data={}):
        for name, value in list(data.items()):
            if hasattr(self, name) and not callable(getattr(self, name)):
                setattr(self, name, value)

    def __repr__(self):
        return str(self.__dict__)


class PaginationInfo(Base):
    """
    response pagination info template
    """

    def __init__(self, data):
        self.total = None
        self.limit = None
        self.page = None
        self.pages = None
        self.prev = None
        self.next = None

        super(PaginationInfo, self).from_json(data)


class Response(Base):
    """
    api response template
    """

    def __init__(self, data):
        self.status = None
        self.code = None
        self.data = None
        self.meta = None

        super(Response, self).from_json(data)

        if "meta" in data:
            self.meta = PaginationInfo(data["meta"])


class Message(Base):
    """
    message object template
    """

    def __init__(self, data):
        self.bulk_id = None
        self.number = None
        self.message = None
        self.status = None
        self.type = None
        self.confirm_state = None
        self.created_at = None
        self.sentAt = None
        self.recipients_count = None
        self.valid_recipients_count = None
        self.page = None
        self.cost = None
        self.payback_cost = None
        self.description = None

        super(Message, self).from_json(data)


class Recipient(Base):
    """
    message recipient object template
    """

    def __init__(self, data):
        self.recipient = None
        self.status = None

        super(Recipient, self).from_json(data)


class InboxMessage(Base):
    """
    inbox message template
    """

    def __init__(self, data):
        self.number = None
        self.message = None
        self.sender = None
        self.time = None
        self.type = None

        super(InboxMessage, self).from_json(data)


class Pattern(Base):
    """
    pattern template
    """

    def __init__(self, data):
        self.code = None
        self.status = None
        self.message = None
        self.is_shared = None

        super(Pattern, self).from_json(data)
