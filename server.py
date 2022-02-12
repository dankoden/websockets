import asyncio
import json
import websockets
from websockets import server
from config_project import action_server
import logging



def logging_conf():
    global log
    log = logging.getLogger("bot")
    log.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("bot_logging.log",mode="w")

    formater_stream = logging.Formatter("%(asctime)s %(levelname)s %(message)s",datefmt="%d-%m-%Y %H:%M")
    formater_file = logging.Formatter("%(asctime)s %(levelname)s %(message)s",datefmt="%d-%m-%Y %H:%M")

    stream_handler.setFormatter(formater_stream)
    file_handler.setFormatter(formater_file)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    stream_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)


class Server():

    async def generate_error_message(self,config_dict, text_error):
       config_dict["error"]['name'] = "Not supported command"
       config_dict["error"]['text'] = str(text_error)
       responce = json.dumps(config_dict)
       log.info("Сгенерировали сообщение ошибки")
       return responce


    async def who_gaves(self,config_dict):
           params = config_dict['params']
           log.info("Формируем запрос")
           pre_responce = await action_server["who_gaves"](**params)
           if not isinstance(pre_responce,Exception):
               for i in pre_responce:
                   config_dict["responce"]['person_id'].append(i[1])
                   config_dict["responce"]['first_name'].append(i[2])
                   config_dict["responce"]['last_name'].append(i[3])
                   config_dict["responce"]['start_read'].append(i[0])
               responce = json.dumps(config_dict,default=str)
               log.info('Готов JSON ответ')
               return responce
           else:
               return pre_responce




    async def have_read(self,config_dict):
           params = config_dict['params']
           log.info("Формируем запрос")
           pre_responce = await action_server["have_read"](**params)
           if not isinstance(pre_responce,Exception):
               config_dict["responce"]["how_much"] = len(pre_responce)
               for i in pre_responce:
                   config_dict["responce"]["which_book"].append(i[3])
                   config_dict["responce"]["start_read"].append(i[1])
                   config_dict["responce"]["finish_read"].append(i[2])
               responce = json.dumps(config_dict,default=str)
               log.info('Готов JSON ответ')
               return responce
           else:
               return pre_responce



    async def where_is_book(self,config_dict):
           params = config_dict['params']
           log.info("Формируем запрос")
           pre_responce =  action_server["where_is_book"](**params)
           if not isinstance(pre_responce,Exception):
               for i in pre_responce:
                   config_dict["responce"]["person_id"] = i[3]
                   config_dict["responce"]["first_name"] = i[1]
                   config_dict["responce"]["last_name"] = i[2]
                   config_dict["responce"]["start_read"] = i[0]
               responce = json.dumps(config_dict,default=str)
               log.info('Готов JSON ответ')
               return responce
           else:
               return pre_responce




    async def get_all_deptor(self,config_dict):
           log.info("Формируем запрос")
           pre_responce = await action_server["get_all_deptor"]()
           if not isinstance(pre_responce,Exception):
               for i in pre_responce:
                   config_dict["responce"]["person_id"].append(i[0])
                   config_dict["responce"]["first_name"].append(i[2])
                   config_dict["responce"]["last_name"].append(i[3])
                   config_dict["responce"]["book_name"].append(i[4])
                   config_dict["responce"]["start_read"].append(i[1])
               responce = json.dumps(config_dict,default=str)
               log.info('Готов JSON ответ')
               return responce
           else:
               return pre_responce



    async def read_message(self,websocket):
        """
        Listening client websocket
        Generate responce
        :param websocket:
        :return: responce for client or error message for client
        """
        try:
            async for message in websocket:
                config_dict = json.loads(message)
                log.info("Получили сообщение")
                print(config_dict)
                action = config_dict['name_command']
                responce = await server_methods[action](config_dict)
                if isinstance(responce,Exception):
                    return await self.generate_error_message(config_dict,responce)
                else:
                    return responce
        except Exception as exc:
            return await self.generate_error_message(config_dict, exc)


    async def handler(self,websocket):
        """
        handler for new_connection
        work with connection and close him after all actions
        :param websocket:
        """
        log.info("New_connection")
        responce = await self.read_message(websocket)
        log.info("Отправили ответ")
        await websocket.send(responce)
        await websocket.close()
        log.info("Закрыли сокет")


    async def start_server(self):
        """
        Server initialization
        :return:
        """
        async with websockets.server.serve(self.handler, 'localhost', 5588) as serv:
            await serv.wait_closed()

if __name__ == "__main__":
    serv = Server()
    server_methods = {"who_gaves": serv.who_gaves, "have_read": serv.have_read,
                      "where_is_book": serv.where_is_book, "get_all_deptor": serv.get_all_deptor}
    logging_conf()
    asyncio.run(serv.start_server())
