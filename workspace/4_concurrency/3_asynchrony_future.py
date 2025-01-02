# Asynchronous operations with Future
import asyncio

# simulating an asynchronous operation using future
async def async_operation(future, data):
    await asyncio.sleep(1)

    if data =="success":
        future.set_result("Operation successful!")
    else:
        future.set_exception(Exception("Operation failed!"))


# creating a future object to be called when future is done
def future_callback(future):
    try:
        print(f"Future result: {future.result()}")
    except Exception as e:
        print(f"Future exception: {e}")

async def main():
    # creating a future object
    future = asyncio.Future()

    # Adding a callback to the future object
    future.add_done_callback(future_callback)

    # start the async operation& pass the future object
    await async_operation(future, "success")

    if future.done():
        try:
            print(f"Future result: {future.result()}")
        except Exception as e:
            print(f"Future exception: {e}")

if __name__ == '__main__':
    asyncio.run(main())

# Output: