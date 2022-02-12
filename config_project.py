from models import CommandsServer
request_db = CommandsServer()

action_server = {'who_gaves': request_db.who_gaves, 'have_read': request_db.have_read,
                 'where_is_book': request_db.where_is_book, 'get_all_deptor': request_db.get_all_deptor}




config = {"commands": {"who_gaves": {"name_command":"who_gaves","params": {'member_family': "doughter"},
                                     'responce': {'person_id': [], 'first_name': [], 'last_name': [],
                                                  "start_read": []},
                                     "error": {"name": None, "text": None}},


                       "have_read": {"name_command":"have_read",'params': {'member_family': "mather"},
                                     'responce': {"how_much": None, "which_book": [], "start_read": [],
                                                  "finish_read": []},
                                     "error": {"name": None, "text": None}},

                       "where_is_book": {"name_command":"where_is_book",'params': {'book_name': "Улисск"},
                                         'responce': {"person_id": None, 'first_name': [], 'last_name': [],
                                                      "start_read": None},
                                         "error": {"name": None, "text": None}},

                       "get_all_deptor": {"name_command":"get_all_deptor",'params': {},
                                          'responce': {"person_id": [], 'first_name': [], 'last_name': [],
                                                       "book_name": [], "start_read": []},
                                          "error": {"name": None, "text": None}}
                       }
          }


commands = [config["commands"]["who_gaves"],config["commands"]["have_read"],
            config["commands"]["where_is_book"],config["commands"]["get_all_deptor"]]


