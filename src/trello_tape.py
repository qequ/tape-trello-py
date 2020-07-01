from trello import TrelloClient
import json
from random import randint
from parsers import *


class TrelloToTape(object):
    """
    The main class for the API between Trello and Tape.
    The __init__ function takes the api_key and the api_secret.
    There is no Auth needed.

    """

    def __init__(self, api_key, api_secret):
        self.client = TrelloClient(api_key=api_key, api_secret=api_secret)
        print("Succesfull login")

    def create_txt_board(self, board_name):
        """
        Main GET function; it takes a board and gets all the information.
        After that it will create an txt file with the json necessary to put into Tape 
        """

        board_wanted = None
        board_list = self.client.list_boards()
        for b in board_list:
            if b.name == board_name:
                board_wanted = b
                break

        board_obj = self.client.get_board(b.id)

        json_dict = {}

        for l in board_obj.all_lists():
            json_dict[str(l.name) + str(randint(10 ** 6, 10 ** 7))
                      ] = parse_list_to_dict(l)

        outf = open("tape_export{}.txt".format(randint(10 ** 6, 10 ** 7)), "w")
        print("writing the file...")
        outf.write(json.dumps(json_dict, indent=4))

        outf.close()
