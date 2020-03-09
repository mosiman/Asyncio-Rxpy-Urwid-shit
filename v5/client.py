import asyncio
import logging

import rx

import jupyter_client as jc

########################
## v5
## - Incoming iopub messages as observables
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

def create_my_observable():
    # Creates an observable that emits messages on the iopub channel.
    def on_subscribe(observer, scheduler):
        # When the observable is subscribed to, the function `f` passed
        # to `rx.create(f)` is run.
        async def observable_iopub():
            # Awaits on iopub messages
            while True:
                msg = await aclient.get_iopub_msg()
                logging.debug(f"received in observable: {msg}")
                observer.on_next(msg)

        # creates the task in the loop returned by 
        # asyncio.get_running_loop()
        task = asyncio.create_task(observable_iopub())
        return rx.disposable.Disposable(
                lambda: task.cancel()
        )
    return rx.create(on_subscribe)

async def main():
    cmd = input("cmd: ")
    aclient.execute(cmd)
    iopub_obs = create_my_observable()
    iopub_obs.subscribe(
            on_next = lambda x: print(f"observable received {x}")
    )

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
