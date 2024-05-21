import perspective

async def main():
    server = perspective.PyAsyncServer()
    session_id = server.register_session(lambda *args, **kwargs: print("session", args, kwargs))
    client = await perspective.create_async_client(server)
    table = await client.table({"x": [1,2,3]}, name="My Table")
    v = await table.view()
    await v.on_update(lambda x: print('first_on_update', x))
    second = await perspective.create_async_client(server)
    other = await second.open_table("My Table")
    view = await table.view()
    await view.on_update(lambda x: print('second_on_update', x))
    await other.update({"x": [4,5,6]})
    await table.update({"x": [7,8,9]})
    await table.size()
    

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())