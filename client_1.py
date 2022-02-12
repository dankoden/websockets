import asyncio
import websockets
import json
from config_project import commands


async def send_message(websock):
    global actual_command
    coice_command = input(
          "0 - Кому давала книги дочка?\n"
          "1 - Какие книги прочитала мама?\n"
          "2 - У кого книга - Улисск?\n"
          "3 - Показать список должников книг\n"
          "Choice command:")
    actual_command = int(coice_command)
    await websock.send(json.dumps(commands[actual_command]))

async def handshake(websocket):
    try:
        await send_message(websocket)
        async for message in websocket:
            responce = json.loads(message)
            if responce["error"]["name"] is not None:
                print(f'''Exception:{responce["error"]["name"]} // {responce["error"]["text"]}''')
            else:
                print(responce["responce"])
    except Exception as exc:
        print(exc)


async def hello():
    uri = "ws://localhost:5588"
    async with websockets.connect(uri) as websocket:
        await handshake(websocket)


if __name__ == "__main__":
    asyncio.run(hello())
