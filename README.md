## Instructions
Minesweeper is a single player game. In this game we have a field (grid with squares) with some hidden
bombs and the goal is to open/clean all the squares without a bomb and if the player hits a bomb, then s/he
loses the game. If the player can open all the squares without a bomb, then s/he wins the game! For more
details, please see https://en.wikipedia.org/wiki/Minesweeper_(video_game)
You are going to build a version of this game with the following requirements:

### Requirements:
1. Single player game.
2. Computer will randomly choose squares to place the bombs.
3. If the grid is a safe one, it should show the number of bombs in its neighbouring squares.
4. If the player loses the game by pressing on a bomb, then the new game should start with the same
grid. (same bombs)
5. Until the player wants to quit, they should be able to continue with a new game.
6. Flagging a square as a bomb is optional. You can skip this feature if you would like. (As long as the
player opens all the squares without a bomb, the player wins the game)

## Build DOCKER environment

### Build the docker image
docker build . -t minesweeper

### Running it
docker run -p 8000:80 minesweeper

---
## Run Locally
If you already have fastapi on you system

    fastapi run main.py

### Start game
    The game was developed to be played via API requests.

    You can use whatever tool of your choice (Postman, requests, curl...)

    Start:
        curl -X 'GET' \
            'http://localhost:8000/start' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "row": 5,
            "col": 5
            }' 

    Check Items
        localhost/minesweeper/{item}
            item[status, get_grid, show_bombs]
                status: True if game is still ongoing
                get_grid: return the grid of the system
                **show_bombs**: display the position of the bombs (used for validation)
            
            curl -X 'GET' \
                'http://localhost:8000/minesweeper/show_bombs' \
                -H 'accept: application/json'


### Click Button
    curl -X 'GET' \
        'http://localhost:8000/click' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "row": 0,
        "col": 0
        }'

    You will receive a response with the grid and the clicked value opened

### Restart
    Just send another start and you shall start another game

### Win
    If you win, you will receive a win message on the json body response