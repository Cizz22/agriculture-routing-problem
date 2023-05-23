
"""Main file for the project."""

from arpga.core import run_arpga
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from arpga.model import Arp

app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "status": "Server is running.",
        "message": "Hello this is the root of the server."

    }


@app.post("/runarp")
async def run_arp(arp: Arp):
   
    maxGen = 40* arp.track
    pSize = 20 * arp.track

    best_fitness, best_solution = run_arpga(
        track=arp.track,
        width=arp.width,
        radius=arp.radius,
        maxGen=maxGen,
        pSize=pSize,
        runNumbers=arp.runNumbers
    )

    return {
        "success": True,
        "message": "ARP Genetic Algorithm has been run successfully.",
        "data": {
            "best_fitness": best_fitness,
            "best_solution": best_solution.tolist()
        },
    }
