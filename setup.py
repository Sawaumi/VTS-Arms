import os
import json

import asyncio
import websockets

import func
from func import *
from util import *

try:
    import winreg
except Exception as e_import_winreg:
    print(e_import_winreg)

"""
Huge thanks to emlo40's frame work: https://github.com/mlo40/VsPyYt
"""

MOTIONS = ["motions/removeHair.exp3.json",
           "motions/tintTexture.exp3.json",
           "motions/textureSwap.exp3.json"]


async def setup(ws):
    if os.path.exists('token.json'):
        print('Loading authtoken From File...')
        with open('token.json', "r") as json_file:
            data = json.load(json_file)
            auth_token = (data['authenticationkey'])
            confirm = await authorize(ws, auth_token)
            if auth_token == "" or not confirm["data"]["authenticated"]:
                print('Error Token Invalid')
                print('Fetching New Tokens...')
                auth_token = await get_auth_token(ws)
                print(auth_token)
                print('Saving authtoken for Future Use...')
                data["authenticationkey"] = auth_token
                json_file.close()
                json_file = open('token.json', "w")
                json_file.write(json.dumps(data))
                json_file.close()
                print("Saving finished")
            else:
                json_file.close()
    else:
        print('Fetching New Tokens...')
        auth_token = await get_auth_token(ws)
        print(auth_token)
        print('Saving authtoken for Future Use...')
        with open('token.json', "w") as json_file:
            json_file_con = {
                "chatspeed": 0.1,
                "authenticationkey": auth_token,
                "authenticationkeytwitch": ""
            }
            json_file.write(json.dumps(json_file_con))
            json_file.close()
        await authorize(ws, auth_token)

    with open('token.json') as json_file:
        data = json.load(json_file)
        json_file.close()
    print("Successfully Loaded")
