from ippanel import Client, Error, HTTPError, ResponseCode

client = Client("YOUR-API-KEY")

try:
    bulk_id = client.send("+9810001", ["+98912xxxxxxx"], "Hello from python client!")
    print(bulk_id)
except Error as e:
    print("Error handled => code: %s, message: %s" % (e.code, e.message))

    if e.code == ResponseCode.ErrUnprocessableEntity.value:
        for field in e.message:
            print("Field: %s , Errors: %s" % (field, e.message[field]))
except HTTPError as e:
    print("Error handled => code: %s" % (e))
