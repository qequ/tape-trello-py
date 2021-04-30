from trello import TrelloClient
import json
from parsers import parse_list_to_dict


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
