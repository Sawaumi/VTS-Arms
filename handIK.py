import asyncio
import time

import setup
from handler import Handler
from setup import *
import websockets
from func import *

FRAME_TIME = 0.06  # .06 -> 15fps, .03->30fps, .016->60fps

truck = ""

POS_TAGS = ["HandLeftPositionX",
            "HandLeftPositionY",
            "HandLeftPositionZ",
            "HandLeftPositionX",
            "HandRightPositionX",
            "HandRightPositionY",
            "HandRightPositionZ",
            "FacePositionX",
            "FacePositionY",
            "FacePositionZ"]


def get_param_value(param):
    switch: param


def get_hand_right_pos_x(reply):
    return


async def req_param_feed(handler_: Handler, param):
    while True:
        try:
            await asyncio.wait_for(handler_.req_param(param), timeout=FRAME_TIME)
            await asyncio.sleep(FRAME_TIME)
        except asyncio.TimeoutError:
            print("request %s time out" % param)
            return


async def solve_IK_feed(handler_: Handler):
    while True:
        try:
            await asyncio.wait_for(handler_.solve_IK(), timeout=FRAME_TIME)
            await asyncio.sleep(FRAME_TIME)
        except asyncio.TimeoutError:
            print("IK time out")
            return


async def callback_(p, c):
    # await asyncio.sleep(1)
    print(c, "callback awake")


async def main():
    remote_url = 'ws://127.0.0.1:8001'

    handler = Handler()
    await handler.async_connect(remote_url)

    print("Connection stable")
    loop = asyncio.get_event_loop()
    # await asyncio.gather(req_param_feed(handler, "HandLeftPositionX"),
    #                      req_param_feed(handler, "HandLeftPositionY"),
    #                      req_param_feed(handler, "HandLeftPositionZ"),
    #                      req_param_feed(handler, "HandRightPositionX"),
    #                      req_param_feed(handler, "HandRightPositionY"),
    #                      req_param_feed(handler, "HandRightPositionZ"),
    #                      req_param_feed(handler, "FacePositionX"),
    #                      req_param_feed(handler, "FacePositionY"),
    #                      req_param_feed(handler, "FacePositionZ"),
    #                      handler.listen(callback_))

    tasks = [req_param_feed(handler, POS_TAG) for POS_TAG in POS_TAGS]
    gather_requests = asyncio.gather(*tasks)
    gather_listener = asyncio.gather(handler.listen())
    gather_solve_IK = asyncio.gather(solve_IK_feed(handler))
    # gather_listener_callback = asyncio.gather(handler.listen(callback_))

    await asyncio.gather(gather_requests, gather_listener, gather_solve_IK)

    loop.run_forever()


async def hello():
    await asyncio.sleep(0.1)
    print('Hello World:%s' % time.time())


if __name__ == '__main__':
    asyncio.run(main())

