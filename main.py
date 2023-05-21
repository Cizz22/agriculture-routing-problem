
"""Main file for the project."""

from arpga.core import run_arpga
from fastapi import FastAPI

app = FastAPI()



@app.get("/")
async def read_root():
    return {
        "status": "Server is running.",
        "message": "Hello this is the root of the server."
        
    }
    
    
@app.post("/runarp")
async def run_arp(track: int, width: float, radius: float, maxGen: int, pSize: int, runNumbers: int):
    
    result = run_arpga(
        track=track,
        width=width,
        radius=radius,
        maxGen=maxGen,
        pSize=pSize,
        runNumbers=runNumbers
    )
    
    return {
        "success": True,
        "message": "ARP Genetic Algorithm has been run successfully.",
        "data": result,
    }
