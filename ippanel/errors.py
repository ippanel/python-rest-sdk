import enum


class ResponseCode(enum.Enum):
    # ErrCredential error when executing repository query
    ErrCredential = "10001"
    # ErrMessageBodyIsEmpty message body is empty
    ErrMessageBodyIsEmpty = "10002"
    # ErrUserLimitted user is limited
    ErrUserLimited = "10003"
    # ErrNumberNotAssignedToYou line not assigned to you
    ErrNumberNotAssignedToYou = "10004"
    # ErrRecipientsEmpty recipients is empty
    ErrRecipientsEmpty = "10005"
    # ErrCreditNotEnough credit not enough
    ErrCreditNotEnough = "10006"
    # ErrNumberNotProfitForBulkSend line not profit for bulk send
    ErrNumberNotProfitForBulkSend = "10007"
    # ErrNumberDeactiveTemp line deactivated temporally
    ErrNumberDeactiveTemp = "10008"
    # ErrMaximumRecipientExceeded maximum recipients number exceeded
    ErrMaximumRecipientExceeded = "10009"
    # ErrGatewayOffline operator is offline
    ErrGatewayOffline = "10010"
    # ErrNoPricing pricing not defined for user
    ErrNoPricing = "10011"
    # ErrTicketIsInvalid ticket is invalid
    ErrTicketIsInvalid = "10012"
    # ErrAccessDenied access denied
    ErrAccessDenied = "10013"
    # ErrPatternIsInvalid pattern is invalid
    ErrPatternIsInvalid = "10014"
    # ErrPatternParamettersInvalid pattern parameters is invalid
    ErrPatternParamettersInvalid = "10015"
    # ErrPatternIsInactive pattern is inactive
    ErrPatternIsInactive = "10016"
    # ErrPatternRecipientInvalid pattern recipient invalid
    ErrPatternRecipientInvalid = "10017"
    # ErrItsTimeToSleep send time is 8-23
    ErrItsTimeToSleep = "10019"
    # ErrDocumentsNotApproved one/all of users documents not approved
    ErrDocumentsNotApproved = "10021"
    # ErrInternal internal error
    ErrInternal = "10022"
    # ErrNumberNotFound provided number not found
    ErrNumberNotFound = "10023"
    # ErrGatewayDisabled gateway disabled
    ErrGatewayDisabled = "10024"
    # ErrUnprocessableEntity inputs have some problems
    ErrUnprocessableEntity = "422"
    # ErrUnauthorized unauthorized
    ErrUnauthorized = "1401"
    # ErrKeyNotValid api key is not valid
    ErrKeyNotValid = "1402"
    # ErrKeyRevoked api key revoked
    ErrKeyRevoked = "1403"


class Error(Exception):
    """
    Error template
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

        super(Error, self).__init__(str(message))


class HTTPError(Exception):
    pass

def parse_errors(response):
    if "error" in response.data:
        return Error(response.code, response.data["error"])
    return
