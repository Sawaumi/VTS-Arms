import asyncio

import time
import websockets

import pyfabrik_local
from pyfabrik_local import Fabrik3D
from setup import *
import math
import sys

from vectormath import Vector3

from typing import Tuple
from typing import List
from typing import Union

HANDS_POS_TAG = {"lx": "HandLeftPositionX",
                 "ly": "HandLeftPositionY",
                 "lz": "HandLeftPositionZ",
                 "rx": "HandRightPositionX",
                 "ry": "HandRightPositionY",
                 "rz": "HandRightPositionZ"}

INITIAL_LEFT_ARM_POSITION = [Vector3(1.7, 0, 0),  # Start point
                             Vector3(4.2, 0, 0), Vector3(4.5, 0, 0), Vector3(3.4, 0, 0)]
INITIAL_RIGHT_ARM_POSITION = [Vector3(-1.7, 0, 0),  # Fixed Start point
                              Vector3(-4.2, 0, 0), Vector3(-4.5, 0, 0), Vector3(-3.4, 0, 0)]
TOLERANCE = 0.01


class Handler:
    def __init__(self) -> None:
        self.req_pos = {"HandLeftPositionX": 0,
                        "HandLeftPositionY": 0,
                        "HandLeftPositionZ": 0,
                        "HandRightPositionX": 0,
                        "HandRightPositionY": 0,
                        "HandRightPositionZ": 0,
                        "FacePositionX": 0,
                        "FacePositionY": 0,
                        "FacePositionZ": 0}

        self.left_arm_params = {"WRIST": 0,
                                "ELBOW": 0,
                                "SHOULDER": 0}

        self.right_arm_params = {"WRIST": 0,
                                 "ELBOW": 0,
                                 "SHOULDER": 0}

        self.fab_left_arm = Fabrik3D(INITIAL_LEFT_ARM_POSITION, TOLERANCE)
        self.fab_right_arm = Fabrik3D(INITIAL_RIGHT_ARM_POSITION, TOLERANCE)

        self.ws = None

    async def async_connect(self, url):
        try:
            self.ws = await websockets.connect(url)
            pass
        except Exception as e:
            print("Couldn't connect to VtubeStudio")
            print(e)
            input("press enter to quit program")
            quit()
        await setup(self.ws)

    async def send_payload(self, payload):
        await self.ws.send(json.dumps(payload))

    async def req_param(self, param):
        payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": api_version,
            "requestID": param,
            "messageType": "ParameterValueRequest",
            "data": {
                "name": param
            }
        }
        await self.ws.send(json.dumps(payload))

    async def listen(self, callback=None):
        i = 0
        while True:
            json_data = await self.ws.recv()
            reply = json.loads(json_data)
            try:
                self.req_pos[reply["requestID"]] = reply["data"]["value"]
            except KeyError:
                callback(reply, i)
                return
            # print("Reply %s" % i + " at %s" % time.time(), self.req_pos)
            i += 1

    async def solve_IK(self):
        self.fab_left_arm.move_to(
            Vector3(self.req_pos["HandLeftPositionX"],
                    self.req_pos["HandLeftPositionY"],
                    self.req_pos["HandLeftPositionZ"]))
        self.fab_right_arm.move_to(
            Vector3(self.req_pos["HandRightPositionX"],
                    self.req_pos["HandRightPositionY"],
                    self.req_pos["HandRightPositionZ"]))
        print("Left %s" % self.fab_left_arm.angles_deg,
              "Right %s" % self.fab_right_arm.angles_deg)
