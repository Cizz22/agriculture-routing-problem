from pydantic import BaseModel, Field


class Arp(BaseModel):
        track: int = Field(..., example=100)
        width: float = Field(..., example=0.5)
        radius: float = Field(..., example=0.5)
        runNumbers: int = Field(..., example=10)