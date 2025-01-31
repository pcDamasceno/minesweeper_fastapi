from fastapi import FastAPI, HTTPException
from minesweeper import Minesweeper
from pydantic import BaseModel

app = FastAPI()
app.state.minesweeper = None


class GridCoordinates(BaseModel):
    row: int
    col: int


def start_game(row=10, col=10):
    # Initialize the Minesweeper game
    app.state.minesweeper = Minesweeper(row, col)
    app.state.minesweeper.build_grid()
    return app.state.minesweeper


def get_game_instance():
    minesweeper = app.state.minesweeper
    if minesweeper is None:
        raise HTTPException(status_code=500, detail="Game not started.")
    if not minesweeper.game:
        raise HTTPException(
            status_code=500, detail="You Hit a Bomb. Restart to continue"
        )
    return minesweeper


@app.get("/")
def instructions():
    context = {"instructions": "These are the game instructoins"}
    return context


# Start the game
@app.get("/start")
def start(grid_coordinates: GridCoordinates) -> dict:
    context = {"requested": f"Grid {grid_coordinates.row}x{grid_coordinates.col}"}

    minesweeper = start_game(grid_coordinates.row, grid_coordinates.col)

    context["status"] = (
        f"Game Started: rows: {grid_coordinates.row}, cols: {grid_coordinates.col} "
        f"Number of bombs: {minesweeper.n_of_bombs}"
    )

    context["response"] = minesweeper.to_json_serializable_grid()

    return context


# Get info after it started
@app.get("/minesweeper/{item}")
def check_status(item):
    minesweeper = get_game_instance()

    context = {"requested": item}

    match item:
        case "status":
            context["response"] = f"Game status is : {minesweeper.game}"
        case "get_grid":
            context["response"] = minesweeper.to_json_serializable_grid()
            return context
        case "show_bombs":
            context["response"] = list(minesweeper.bombs_positions)
        case _:
            context["response"] = "Invalid/ Unkown item"

    return context


@app.get("/click")
def click(click: GridCoordinates):
    context = {"request": click}
    minesweeper = get_game_instance()

    context["response"] = minesweeper.click(click.row, click.col)

    # Check if we won
    if minesweeper.check_win():
        context["win"] = "Congratulations!"

    return context

@app.get("/flag")
def click(click: GridCoordinates):
    context = {"request": click}
    minesweeper = get_game_instance()

    context["response"] = minesweeper.flag(click.row, click.col)

    return context