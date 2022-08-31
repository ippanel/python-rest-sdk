import unittest
from ippanel import Client, HTTPError, Response
import json
from unittest import mock


class TestMessage(unittest.TestCase):
    @mock.patch("ippanel.httpclient.requests")
    def test_get_credit(self, http_client):

        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "credit": 30000,
                "gift": null
            }
        }
        '''))

        sms = Client("", http_client)
        credit = sms.get_credit()

        self.assertEqual(credit, 30000)

    @mock.patch("ippanel.httpclient.requests")
    def test_send_response_parse(self, http_client):
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "message_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        message_id = sms.send(
            "9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello", "Show in logs")

        self.assertEqual(message_id, 70671101)

    @mock.patch("ippanel.httpclient.requests")
    def test_send_api_call(self, http_client):

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "message_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"],
                 "Hello", "Show in logs")

        http_client.post.assert_called_once_with("/sms/send/panel/single", {
            "sender": "9810001",
            "recipient": ["98912xxxxxxx", "98913xxxxxxx"],
            "message": "Hello",
            "description": {
                "summary": "Show in logs",
                "count_recipient": "2"
            },
        })

    @mock.patch("ippanel.httpclient.requests")
    def test_message_get(self, http_client):
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "error_message": "",
            "data": [
                {
                    "message_id": 70671101,
                    "number": "+9850002",
                    "message": "Hello from me",
                    "state": "active",
                    "type": "webservice",
                    "valid": "",
                    "time": "2019-12-07T13:34:06Z",
                    "time_sent": "2019-12-07T13:34:06Z",
                    "recipient_count": 1,
                    "exit_count": 0,
                    "part": 1,
                    "cost": 0,
                    "return_cost": 0,
                    "summary": ""
                }
            ]
        }
        '''))

        sms = Client("", http_client)
        message = sms.get_message(70671101)

        self.assertEqual(message.message_id, 70671101)

    @mock.patch("ippanel.httpclient.requests")
    def test_fetch_statuses(self, http_client):
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "deliveries": [
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

    @mock.patch("ippanel.httpclient.requests")
    def test_fetch_inbox_messages(self, http_client):
        http_client.get.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "error_message": "",
            "data": [
                {
                    "to": "+9810001",
                    "message": "Hello",
                    "from": "+98912xxxxxxx",
                    "created_at": "2019-12-17T23:02:10Z",
                    "type": "normal"
                },
                {
                    "to": "+9810001",
                    "message": "Test",
                    "from": "+98913xxxxxxx",
                    "created_at": "2019-12-17T23:01:59Z",
                    "type": "normal"
                }
            ],
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
        self.assertEqual(messages[0].to, "+9810001")
        self.assertEqual(messages[0].message, "Hello")
        self.assertEqual(messages[0].sender, "+98912xxxxxxx")
        self.assertEqual(messages[0].created_at, "2019-12-17T23:02:10Z")
        self.assertEqual(messages[0].type, "normal")

        self.assertEqual(pagination_info.total, 2)

    @mock.patch("ippanel.httpclient.requests")
    def test_create_pattern(self, http_client):

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": 200,
            "error_message": "",
            "data": [
                {
                    "id": "6305dfc31bac95160258e1b5",
                    "code": "6gr7ngjmhi"
                }
            ]
        }
        '''))

        sms = Client("", http_client)
        sms.create_pattern(r"%name% is awesome",
                           "description", {"name": "string"})

        http_client.post.assert_called_once_with("/sms/pattern/normal/store", {
            "pattern": r"%name% is awesome",
            "description": r"description",
            "delimiter": r"%",
            "variable": [{"name": "name", "type": "string"}],
            "is_shared": False,
        })

    @mock.patch("ippanel.httpclient.requests")
    def test_send_pattern(self, http_client: mock.MagicMock):

        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "message_id": 70671101
            }
        }
        '''))

        sms = Client("", http_client)
        message_id = sms.send_pattern(
            "6gr7ngjmhi", "9810001", "+98912xxxxxxx", {"name": "IPPanel"})

        http_client.post.assert_called_once_with("/sms/pattern/normal/send", {
            "code": "6gr7ngjmhi",
            "sender": "9810001",
            "recipient": "+98912xxxxxxx",
            "variable": {"name": "IPPanel"},
        })

        self.assertEqual(message_id, 70671101)

    @mock.patch("ippanel.httpclient.requests")
    def test_parse_exception(self, http_client):
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "message_idd": 70671101
            }
        }
        '''))

        sms = Client("", http_client)

        with self.assertRaises(ValueError):
            sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello", "summary")

    @mock.patch("ippanel.httpclient.requests")
    def test_http_exception(self, http_client):
        http_client.post.return_value = Response(json.loads(r'''
        {
            "status": "OK",
            "code": "OK",
            "error_message": "",
            "data": {
                "message_id": 70671101
            }
        }
        '''))

        http_client.post.side_effect = HTTPError

        sms = Client("", http_client)

        with self.assertRaises(HTTPError):
            sms.send("9810001", ["98912xxxxxxx", "98913xxxxxxx"], "Hello", "summary")
