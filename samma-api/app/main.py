from pydantic import BaseModel
from fastapi import FastAPI, Query
import httpx, os
from typing import List
from fastapi.middleware.cors import CORSMiddleware   

app = FastAPI()

app.add_middleware(                    
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OMDB_KEY = os.getenv("OMDB_API_KEY")

class MovieResult(BaseModel):        
    Title: str
    Released: str
    Runtime: str
    Genre: str
    Actors: str
    Plot: str
    Poster: str
    imdbRating: str

@app.get("/api/search", response_model=List[MovieResult])  
async def search(q: str = Query(..., min_length=2)):
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(
            "http://www.omdbapi.com/",
            params={"apikey": OMDB_KEY, "s": q, "type": "movie"}
        )
        data = r.json()
        if data.get("Response") == "False":
            return []

        imdb_ids = [item["imdbID"] for item in data["Search"]]

        # fetch full details for each movie
        movies = []
        for iid in imdb_ids:
            detail = await client.get(
                "http://www.omdbapi.com/",
                params={"apikey": OMDB_KEY, "i": iid, "plot": "short"}
            )
            d = detail.json()
            movies.append(MovieResult(
                Title=d["Title"],
                Released=d.get("Released", ""),
                Runtime=d.get("Runtime", ""),
                Genre=d.get("Genre", ""),
                Actors=d.get("Actors", ""),
                Plot=d.get("Plot", ""),
                Poster=d.get("Poster", ""),
                imdbRating=d.get("imdbRating", "")
            ))
        return movies