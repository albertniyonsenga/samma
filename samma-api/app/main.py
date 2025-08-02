from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException


load_dotenv()

app = FastAPI(
    title="Summa API 🎬",
    description="Backend API for Summa CLI tool.",
    version="0.1.0"
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
