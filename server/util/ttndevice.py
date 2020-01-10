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
  "disableFCntCheck": True,
  "uses32BitFCnt": True,
}

def genNewDevice(username, id):
    device = devicetemplate.copy()
    devicetemplate["description"] = "{}poldevice{}".format(username.lower, id)
    devicetemplate["appEui"] = TTN_APPEUI
    devicetemplate["devEui"] = binascii.b2a_hex(os.urandom(8)).upper()
    devicetemplate["appkey"] = binascii.b2a_hex(os.urandom(16)).upper()
    return device
