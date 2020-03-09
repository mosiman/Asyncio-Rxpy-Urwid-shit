import asyncio
import time
import logging

import math
import random

from aioconsole.stream import ainput

#########
## Asks user for input. "Fire and forgets" `execute_command`
## and lets execute_command do shit, while we wait
##
## Todo for v2: Continuously ask for input, be able to execute lots of stuff
##   simultaneously. Note: In Jupytui it will be queued but whatever.
## Todo for v3: Turn execute_command into an async observable
##   as in [here](https://blog.oakbits.com/rxpy-and-asyncio.html)
##   and update stuff in the "main" thread
#########



def rand_sec(ubound):
    return math.floor(random.random() * 10 % ubound)

logging.basicConfig(level=logging.DEBUG, filename='loggy.log')

async def execute_command(cmd):
    logging.debug(f"executing command {cmd}")
    for i in [1,2,3,4,5]:
        rsec = rand_sec(5)
        logging.debug(f"randsleep: {rsec}")
        await asyncio.sleep(rsec)

async def main():
    # asyncio.ensure_future(timer())

    cmd = input("cmd: ")
    asyncio.ensure_future(execute_command(cmd))

logging.debug("starto")
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

pending = asyncio.Task.all_tasks()
loop.run_until_complete(asyncio.gather(*pending))
