import asyncio
import time


def hello_world(loop):
    print('Hello World')
    loop.call_later(1, hello_world, loop)

def good_evening(loop):
    print('Good Evening')
    loop.call_later(1, good_evening, loop)

@asyncio.coroutine
def hello_world_coroutine():
    while True:
        yield from asyncio.sleep(1)
        print('Hello World Coroutine')

@asyncio.coroutine
def good_evening_coroutine():
    while True:
        yield from asyncio.sleep(1)
        print('Good Evening Coroutine')

print('step: asyncio.get_event_loop()')
loop = asyncio.get_event_loop()

print('step: loop.call_soon(hello_world, loop)')
loop.call_soon(hello_world, loop)
print('step: loop.call_soon(good_evening, loop)')
loop.call_soon(good_evening, loop)
print('step: asyncio.async(hello_world_coroutine)')
asyncio.async(hello_world_coroutine())
print('step: asyncio.async(good_evening_coroutine)')
asyncio.async(good_evening_coroutine())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print('step: loop.close()')
    loop.close()
