# IPPanel SMS api SDK

[![Build Status](https://travis-ci.org/ippanel/python-rest-sdk.svg?branch=master)](https://travis-ci.org/ippanel/python-rest-sdk)

## Installation

you can install this package with either pip:

```bash
python -m pip install ippanel
```

or running bellow command after downloading source:

```bash
python setup.py install
```

## Examples

For using sdk, you have to create a client instance that gives you available methods on API

```python
from ippanel import Client

# you api key that generated from panel
api_key = "api-key"

# create client instance
sms = Client(api_key)

...
```

### Credit check

```python
# return float64 type credit amount
credit = sms.get_credit()

```

### Send one to many

For sending sms, obviously you need `originator` number, `recipients` and `message`.

```python
message_id = sms.send(
    "+9810001",          # originator
    ["98912xxxxxxx"],    # recipients
    "ippanel is awesome" # message
    "description"        # is logged
)

```

If send is successful, a unique tracking code returned and you can track your message status with that.

### Get message summery

```python
message_id = "message-tracking-code"

message = sms.get_message(message_id)

print(message.state)       # get message status
print(message.cost)        # get message cost
print(message.return_cost) # get message payback
```

### Get message delivery statuses
Status Code Explanation:
0 for Send
1 for pending
2 for delivered
3 for failed
4 for blaklisted
```python
message_id = "message-tracking-code"

statuses, pagination_info = sms.fetch_statuses(message_id, 0, 10)

# you can loop in messages statuses list
for status in statuses {
    print("Recipient: %s, Status: %s" % (status.recipient, status.status))
}
print("Total: ", pagination_info.total)
```

### Inbox fetch

fetch inbox messages

```python
messages, pagination_info = sms.fetch_inbox(0, 10)

for message in messages {
    print("Received message %s from number %s in line %s" % (message.message, message.sender, message.to))
}
```

### Pattern create

For sending messages with predefined pattern(e.g. verification codes, ...), you hav to create a pattern. a pattern at least have a parameter.

```python
pattern_variables = {
    "name": "string",
    "code": "integer",
}
code = sms.create_pattern(r"%name% is awesome, your code is %code%", "description", pattern_variables, "%", False)

print(code)
```

### Send with pattern

```python
pattern_values = {
    "name": "IPPANEL",
}

message_id = sms.send_pattern(
    "t2cfmnyo0c",    # pattern code
    "+9810001",      # originator
    "98912xxxxxxx",  # recipient
    pattern_values,  # pattern values
)
```

### Error checking

```python
from ippanel import HTTPError, Error, ResponseCode

try:
    message_id = sms.send("9810001", ["98912xxxxx"], "ippanel is awesome")
except Error as e: # ippanel sms error
    if e.code == ResponseCode.ErrUnprocessableEntity.value:
        for field in e.message:
            print(f"Field: {field} , Errors: {e.message[field]}")
    elif e.code == ResponseCode.ErrForbidden.value:
        print(f"Ippanel Error Forbidden => code: {e.code}, message: {e.message}")
    elif e.code == ResponseCode.ErrInternalServer.value:
        print(f"Ippanel Internal Server Error => code: {e.code}, message: {e.message}")
    elif e.code == ResponseCode.ErrNotFound.value:
        print(f"Ippanel Error Not Found => code: {e.code}, message: {e.message}")
except HTTPError as e: # http error like network error, not found, ...
    print(f"Error handled => code: {e}")

```
