

#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import logging

logging.basicConfig(level=logging.DEBUG, filename='server.log')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    logging.debug("Received request: %s" % message)

    for i in [1,2,3]:
        #  Do some 'work'
        time.sleep(1)

        #  Send reply back to client
        socket.send_string(f"executed {message}")
    socket.send_string("done")

