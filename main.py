from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import json
from .minesweeper import Minesweeper
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
app.state.ms = None

class RowCol(BaseModel):
    row: int
    col: int


def start_game(row=10, col=10):
    # Initialize the Minesweeper game once at startup
    app.state.ms = Minesweeper(row, col)
    app.state.ms.build_grid()
    return app.state.ms

def get_game_instance():
    ms = app.state.ms 
    if ms is None:
        raise HTTPException(status_code=500, detail="Game not started.")
    if not ms.game:
        raise HTTPException(status_code=500, detail="You Hit a Bomb, restart to continue")
    return ms

@app.get("/")
def instructions():
    context = {
        "instructions": "These are the game instructoins"
    }
    return context

# Start the game
@app.get("/start")
def start(row_col: RowCol) -> dict:
    context = {
        "requested": f"Grid {row_col.row}x{row_col.col}"
    }


    ms = start_game(row_col.row, row_col.col)
    
    context["status"] = (
        f"Game Started: rows: {row_col.row}, cols: {row_col.col} "
        f"Number of bombs: {ms.n_of_bombs}"
    )

    context["response"] = ms.to_json_serializable_grid()


    return context

# Get info after it started
@app.get("/minesweeper/{item}")
def minesweeper(item):
    ms = get_game_instance()

    context = {
        "requested": item
    }

    match item:
        case "status":
            context["response"] = f"Game status is : {ms.game}"
        case "get_grid":           
            context["response"] = ms.to_json_serializable_grid()
            return context
        
        case "get_bombs_pos":
            context["response"] = list(ms.bombs_positions)
        case _:    
            context["response"] = "Invalid/ Unkown item"

    return context

@app.get("/click")
def click(click: RowCol):
    context = {"request": click}
    ms = get_game_instance()
    
    context["response"] = ms.click(click.row, click.col)

    # Check if we won
    if ms.check_win():
        context["win"] = 'Congratulations!'

    return context