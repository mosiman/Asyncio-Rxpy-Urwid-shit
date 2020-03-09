import asyncio
import logging

import jupyter_client as jc

########################
## v4
## - Start an async KernelClient (NEW for jupyter_client 6.0.0)
## - define an async loop waiting on iopub_msg
## - Run a command, and log the incoming iopub messages. 
########################

logging.basicConfig(level=logging.DEBUG, filename='client.log')

ksm = jc.kernelspec.KernelSpecManager()

kspecs = ksm.find_kernel_specs()
kernel_names = kspecs.keys()

kerMan = jc.KernelManager(kernel_name='python3')

kerMan.start_kernel()


# because there is no `KernelManager.async_client()`
# have to construct `AsyncKernelClient` ourself, yuck
kw = {}
kw.update(kerMan.get_connection_info(session=True))
kw.update(dict(
    connection_file=kerMan.connection_file,
    parent=kerMan
))

aclient = jc.AsyncKernelClient(**kw)
aclient.start_channels()

async def arecv():
    logging.debug("arecv called")
    while True:
        msg = await aclient.get_iopub_msg()
        logging.debug(f"received in arecv: {msg}")

async def main():
    asyncio.ensure_future(arecv())
    cmd = input("cmd: ")

    aclient.execute(cmd)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
