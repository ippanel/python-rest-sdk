class Base(object):
    """
    base model 
    """

    def from_json(self, data={}):
        for name, value in data.items():
            if name == 'from':
                name = 'sender'
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
        self.error_message = None

        super(Response, self).from_json(data)

        if "meta" in data:
            self.meta = PaginationInfo(data["meta"])


class Message(Base):
    """
    message object template
    """

    def __init__(self, data):
        self.message_id = None
        self.number = None
        self.message = None
        self.state = None
        self.type = None
        self.valid = None
        self.time = None
        self.time_send = None
        self.recipient_count = None
        self.exit_count = None
        self.part = None
        self.cost = None
        self.return_cost = None
        self.summary = None

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
        self.to = None
        self.message = None
        self.sender = None
        self.created_at = None
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
