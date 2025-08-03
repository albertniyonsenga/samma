from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
from typing import Optional

load_dotenv()

app = FastAPI(
    title="Movie Search API",
    description="Fetch movie details via OMDb API",
) 


app.add_middleware(         
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OMDB_BASE = "http://www.omdbapi.com/"
OMDB_KEY = os.getenv("OMDB_API_KEY")
if not OMDB_KEY:
    raise RuntimeError("Environment variable OMDB_API_KEY must be set")

class Movie(BaseModel):
    Title: str
    Year: str
    Rated: Optional[str]
    Released: Optional[str]
    Runtime: Optional[str]
    Genre: Optional[str]
    Director: Optional[str]
    Writer: Optional[str]
    Actors: Optional[str]
    Plot: Optional[str]
    Language: Optional[str]
    Country: Optional[str]
    Awards: Optional[str]
    Poster: Optional[str]
    Ratings: Optional[list]
    Metascore: Optional[str]
    imdbRating: Optional[str]
    imdbVotes: Optional[str]
    imdbID: Optional[str]
    Type: Optional[str]
    DVD: Optional[str]
    BoxOffice: Optional[str]
    Production: Optional[str]
    Website: Optional[str]
    Response: str

class SearchResultItem(BaseModel):
    Title: str
    Year: str
    imdbID: str
    Type: str
    Poster: str

class SearchResponse(BaseModel):
    Search: Optional[list[SearchResultItem]]
    totalResults: Optional[str]
    Response: str
    Error: Optional[str]

@app.get("/")
async def root():
   return {
        "message": "🎬 Welcome to Movie Search API powered by Samma Backend",
        "endpoints": {
            "movie": "/movie?title=<TITLE>",
            "search": "/search?query=<TERM>&page=<PAGE_NUMBER>"
        }
    }

@app.get("/movie", response_model=Movie)
async def get_movie(title: str = Query(..., min_length=1, description="Exact movie title")):
    """
    Get detailed information about one movie, by exact title.
    """
    params = {"t": title, "apikey": OMDB_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(OMDB_BASE, params=params, timeout=10.0)
    data = resp.json()
    if data.get("Response") != "True":
        msg = data.get("Error", "Unknown error from OMDb")
        raise HTTPException(status_code=404, detail=f"OMDb API error: {msg}")
    return data

@app.get("/search", response_model=SearchResponse)
async def search_movies(query: str = Query(..., min_length=1, description="Search term"),
                        page: int = Query(1, ge=1, le=100, description="Page number (10 results per page)")):
    """
    Search for movies by keyword; returns up to 10 results per page for better experience.
    """
    params = {"s": query, "page": page, "apikey": OMDB_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(OMDB_BASE, params=params, timeout=10.0)
    data = resp.json()
    return data
