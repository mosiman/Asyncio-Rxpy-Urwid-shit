import zmq
import asyncio
import time
import logging

import rx

import math
import random

from aioconsole.stream import ainput

logging.basicConfig(level=logging.DEBUG, filename='client.log')

context = zmq.Context()

print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")
# 
#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))

async def observable_recv():
    while True:
        output = socket.recv()
        logging.debug(f"received from server: {output}")

def test_observable(observer, scheduler):
    msg = socket.recv_string()
    if msg == "done":
        observer.on_completed()
    else:
        observer.on_next(msg)

    

def main():
    done_exec = False
    def setDoneExec(b):
        done_exec = b
    while not done_exec:
        cmd = "9 + 10"
        cmd = input("cmd: ")
        socket.send_string(cmd)
        server_source = rx.create(test_observable)
        server_source.subscribe(
                on_next = lambda x: print(f"recv from observable {x}"),
                on_completed = lambda x: setDoneExec(True)
        )
    # asyncio.ensure_future(observable_recv())
    # while True:
    #     cmd = input("cmd: ")
    #     socket.send_string(cmd)
    #     # t = socket.recv()
    #     # logging.debug(f"received from server: {t}")


def main2():
    asyncio.ensure_future(observable_recv())
    while True:
        cmd = input("cmd: ")
        socket.send_string(cmd)


main2()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# cleanup
# pending = asyncio.Task.all_tasks()
# loop.run_until_complete(asyncio.gather(*pending))
