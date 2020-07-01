def parse_card_to_dict(card):
    """
    Takes a card object and returns a dict with id, name and state
    """
    return {"id": card.id, "name": card.name, "state": ""}


def parse_list_to_dict(list):
    json_dict = {"name": list.name, "items": [], "vis": True, "pin": False}

    for c in list.list_cards():
        json_dict["items"].append(parse_card_to_dict(c))

    return json_dict
