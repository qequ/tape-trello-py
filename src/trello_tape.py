import json
from random import randint
from parsers import parse_list_to_dict
from trello import TrelloClient


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class SearchError(Error):
    """
    Exception raised for errors trying to find a value
    """

    def __init__(self, message):
        self.message = message


class TrelloToTape(object):
    """
    The main class for the API between Trello to Tape functions.
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

        if board_wanted is None:
            raise SearchError("Couldn't find {} board".format(board_name))

        board_obj = self.client.get_board(b.id)

        json_dict = {}
        id_stamp = b.id
        for l in board_obj.all_lists():
            json_dict[str(l.name) + str(id_stamp)
                      ] = parse_list_to_dict(l)

        with open("tape_trelloimport_{}.txt".format(id_stamp), "w") as outf:
            outf.write(json.dumps(json_dict, indent=4))


class TapetoTrello():
    """
    The main class for the API between Tape to Trello functions.
    """

    def __init__(self, api_key, api_secret):
        self.client = TrelloClient(api_key=api_key, api_secret=api_secret)

    def export_txt_to_trello(self, filepath='', board_name="TapeBoard"+str(randint(1, 25**4))):
        """
        Given the path to the .txt tape savefile and a name of the new board
        it creates a new board on trello
        """
        with open(filepath) as tape_file:
            tape_str = tape_file.read()

        json_tape = json.loads(tape_str)

        new_board = self.client.add_board(board_name)

        for k in json_tape:
            # creates lists of the new board
            new_list = new_board.add_list(json_tape[k]["name"])

            # creates the cards of the new list
            list_cards = json_tape[k]["items"]

            for json_card in list_cards:
                new_list.add_card(
                    json_card["name"], desc="State: {}".format(json_card["state"].capitalize()))
