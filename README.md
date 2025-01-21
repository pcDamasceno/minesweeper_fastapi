## Instructions

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


        localhost/minesweeper/{item}
            item[status, get_grid, show_bombs]
                status: True if game is still ongoing
                get_grid: return the grid of the system
                show_bombs: display the position of the bombs (used for validation)
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