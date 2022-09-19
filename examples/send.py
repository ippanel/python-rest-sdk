from ippanel import Client, Error, HTTPError, ResponseCode

client = Client("bETP93HSkawWB4FdCMfoJ7SECKUj2BgiSw0qeZi2CBI=")

try:
    message_id = client.send("+983000505", ["+989153621841"], "Hello from python client!", "summary")
    print(message_id)
except Error as e:
    print("Error handled => code: %s, message: %s" % (e.code, e.message))

    if e.code == ResponseCode.ErrUnprocessableEntity.value:
        for field in e.message:
            print("Field: %s , Errors: %s" % (field, e.message[field]))
except HTTPError as e:
    print("Error handled => code: %s" % (e))
