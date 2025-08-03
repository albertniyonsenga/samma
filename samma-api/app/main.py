from pydantic import BaseModel
import requests
import httpx, os
from typing import List
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

app = FastAPI(
    title="Summa API 🎬",
    description="Backend API for Summa CLI tool.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = "http://www.omdbapi.com/"

class MovieQuery(BaseModel):
    title: str

class MovieData(BaseModel):
    title: str
    year: str
    cast: str
    plot: str


class MovieResult(BaseModel):           # New model
    Title: str
    Released: str
    Runtime: str
    Genre: str
    Actors: str
    Plot: str
    Poster: str
    imdbRating: str

@app.get("/api/search", response_model=List[MovieResult])   # NEW response_model
async def search(q: str = Query(..., min_length=2)):
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(
            "http://www.omdbapi.com/",
            params={"apikey": OMDB_API_KEY, "s": q, "type": "movie"}
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
                params={"apikey": OMDB_API_KEY, "i": iid, "plot": "short"}
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

@app.get("/")
async def root():
    return {"message": "🎬 Welcome to the Summa API!"}

@app.post("/movie", response_model=MovieData)
def get_movie(query: MovieQuery):
    if not OMDB_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OMDB_API_KEY")

    response = requests.get(
        OMDB_API_URL,
        params={"t": query.title, "apikey": OMDB_API_KEY}
    )

    data = response.json()
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Movie not found")

    return MovieData(
        title=data.get("Title"),
        year=data.get("Year"),
        cast=data.get("Actors"),
        plot=data.get("Plot")
    )

@app.get("/search")
def search_movies(keyword: str):
    if not OMDB_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OMDB_API_KEY")

    response = requests.get(
        OMDB_API_URL,
        params={"s": keyword, "apikey": OMDB_API_KEY}
    )

    data = response.json()
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail=data.get("Error", "No results"))

    return {"results": data.get("Search", [])}

@app.get("/health")
def health():
    return {"status": "ok"}
