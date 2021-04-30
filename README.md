# Tape-o-Trello

A little API to exchange information between your [Trello](https://trello.com/) Boards and [Tape](https://aeriform.itch.io/tape)

# Requirements
* py-trello package

it can be installed by the requirements.txt;

```
pip install -r requirements.txt
```

# Usage

It requires the `api_key` and `api_secret`, both are [generated here](https://trello.com/app-key).


To dump a trello board into a .txt which can be dropped into Tape:

```python
from  trello_tape import TrelloToTape
tt = TrelloToTape(api_key='your-key', api_secret='your-secret')
tt.create_txt_board(board_name='your-board')
```

To create a Trello board from a .txt Tape savefile:

```python
from trello_tape import TapetoTrello
tt = TapetoTrello(api_key='your-key', api_secret='your-secret')
tt.export_txt_to_trello(filepath="path/to/your/.txt", board_name="new-board-name")
```
