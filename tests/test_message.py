import unittest
from ippanel import Client, Error, HTTPError, Response
from requests.exceptions import Timeout

try:
    import simplejson as json
except ImportError:
    import json

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class TestMessage(unittest.TestCase):
    def test_send_response_parse(self):
        http_client = Mock()
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "bulk_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        bulk_id = sms.send(
            "9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello")

        self.assertEqual(bulk_id, 70671101)

    def test_send_api_call(self):
        http_client = Mock()

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "bulk_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello")

        http_client.post.assert_called_once_with("/v1/messages", {
            "originator": "9810001",
            "recipients": ["98912xxxxxxx", "98913xxxxxxx"],
            "message": "Hello",
        })

    def test_message_get(self):
        http_client = Mock()
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "message": "Ok",
            "data": {
                "message": {
                "bulk_id": 70671101,
                "number": "+9850002",
                "message": "Hello from me",
                "status": "active",
                "type": "webservice",
                "confirm_state": "",
                "created_at": "2019-12-07T13:34:06Z",
                "sent_at": "2019-12-07T13:34:06Z",
                "recipients_count": 1,
                "valid_recipients_count": 0,
                "page": 1,
                "cost": 0,
                "payback_cost": 0,
                "description": ""
                }
            }
        }
        '''))

        sms = Client("", http_client)
        message = sms.get_message(70671101)

        self.assertEqual(message.bulk_id, 70671101)

    def test_fetch_statuses(self):
        http_client = Mock()
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "recipients": [
                    {
                        "recipient": "+98912xxxxxxx",
                        "status": "delivered"
                    }
                ]
            },
            "meta": {
                "total": 1,
                "pages": 1,
                "limit": 1,
                "page": 0,
                "prev": null,
                "next": null
            }
        }
        '''))

        sms = Client("", http_client)
        statuses, pagination_info = sms.fetch_statuses(52738671, 0, 10)

        self.assertEqual(len(statuses), 1)
        self.assertEqual(statuses[0].recipient, "+98912xxxxxxx")
        self.assertEqual(statuses[0].status, "delivered")

        self.assertEqual(pagination_info.total, 1)

    def test_fetch_inbox_messages(self):
        http_client = Mock()
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "message": "Ok",
            "data": {
                "messages": [
                    {
                        "number": "+9810001",
                        "message": "Hello",
                        "sender": "+98912xxxxxxx",
                        "time": "2019-12-17T23:02:10Z",
                        "type": "normal"
                    },
                    {
                        "number": "+9810001",
                        "message": "Test",
                        "sender": "+98913xxxxxxx",
                        "time": "2019-12-17T23:01:59Z",
                        "type": "normal"
                    }
                ]
            },
            "meta": {
                "total": 2,
                "pages": 1,
                "limit": 2,
                "page": 0,
                "prev": null,
                "next": null
            }
        }
        '''))

        sms = Client("", http_client)
        messages, pagination_info = sms.fetch_inbox(0, 2)

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].number, "+9810001")
        self.assertEqual(messages[0].message, "Hello")
        self.assertEqual(messages[0].sender, "+98912xxxxxxx")
        self.assertEqual(messages[0].time, "2019-12-17T23:02:10Z")
        self.assertEqual(messages[0].type, "normal")

        self.assertEqual(pagination_info.total, 2)

    def test_create_pattern(self):
        http_client = Mock()

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "message": "Ok",
            "data": {
                "pattern": {
                    "code": "6gr7ngjmhi",
                    "status": "pending",
                    "message": "%name% is awesome",
                    "is_shared": false
                }
            }
        }
        '''))

        sms = Client("", http_client)
        sms.create_pattern(r"%name% is awesome", False)

        http_client.post.assert_called_once_with("/v1/messages/patterns", {
            "pattern": r"%name% is awesome",
            "is_shared": False,
        })

    def test_send_pattern(self):
        http_client = Mock()

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "bulk_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        bulk_id = sms.send_pattern("6gr7ngjmhi","9810001", "+98912xxxxxxx", {"name": "IPPanel"})

        http_client.post.assert_called_once_with("/v1/messages/patterns/send", {
            "pattern_code": "6gr7ngjmhi",
            "originator": "9810001",
            "recipient": "+98912xxxxxxx",
            "values": {"name": "IPPanel"},
        })

        self.assertEqual(bulk_id, 70671101)

    def test_parse_exception(self):
        http_client = Mock()
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "bulk_idd": 70671101
            }
        }
        '''))

        sms = Client("", http_client)

        with self.assertRaises(ValueError):
            sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello")
    
    def test_http_exception(self):
        http_client = Mock()
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "message": "Ok",
            "data": {
                "bulk_id": 70671101
            }
        }
        '''))

        http_client.post.side_effect = HTTPError

        sms = Client("", http_client)

        with self.assertRaises(HTTPError):
            sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello")
