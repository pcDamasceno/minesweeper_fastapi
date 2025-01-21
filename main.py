from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import json
from .minesweeper import Minesweeper
from typing import Optional

app = FastAPI()
ms: Optional[Minesweeper] = None

@app.get("/")
def instructions():
    context = {
        "instructions": "These are the game instructoins"
    }
    return context

@app.get('/minesweeper/{item}')
def minesweeper(
    item: str,
    row: int = 10,
    col: int = 10,
    click_row = False,
    click_col = False
    ) -> dict:

    global ms
    context = {
        "requested": item
    }

    match item:
        case 'start':
            ms = Minesweeper(row, col)
            context['status'] = f"Game Started: rows: {row}, cols: {col}"
            context['response'] = ms.grid
        
        case 'get_grid':
            if ms is None:
                raise HTTPException(status_code=500, detail="Game not started.")
             
            context['response'] = ms.grid
        
        
        case 'click':
            # Make sure we have started
            if ms is None:
                raise HTTPException(status_code=500, detail="Game not started.")
            
            if (not click_row) or (not click_col):
                raise HTTPException(status_code=500, detail="Make sure To Click Somewhere")
            
            context['response'] = ms.click(click_row, click_col)

        case _:    
            context["response"] = "Invalid/ Unkown item"
    
    return context
