import os
import binascii
from ..secrets import TTN_APPEUI

devicetemplate = {
  "description": "Description",
  "appEui": "0011223344556677",
  "devEui": "9988776655443322",
  "appKey": "",
  "fCntUp": 0,
  "fCntDown": 0,
  "latitude": 0,
  "longitude": 0,
  "altitude": 0,
  "disableFCntCheck": False,
  "uses32BitFCnt": True,
}

# Generates a new device object to be sent to the things network to register
def genNewDevice(username, id):
    device = devicetemplate.copy()
    device["description"] = "{}poldevice{}".format(username.lower(), id)
    device["appEui"] = TTN_APPEUI
    device["devEui"] = binascii.b2a_hex(os.urandom(8)).upper()
    device["appKey"] = binascii.b2a_hex(os.urandom(16)).upper()
    return device