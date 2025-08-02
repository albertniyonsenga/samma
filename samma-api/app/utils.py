import os, csv, json
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = f"http://www.omdbapi.com/"

def get_movie_data(title):
    response = requests.get(OMDB_URL, params={"t": title, "apikey": API_KEY})
    data = response.json()
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail=data.get("Error"))
    return {
        "title": data["Title"],
        "year": data["Year"],
        "plot": data["Plot"],
        "cast": data["Actors"]
    }

def save_as_json(title):
    data = get_movie_data(title)
    return data  # return as JSON automatically by FastAPI

def save_as_csv(title):
    data = get_movie_data(title)
    response = {"csv": f"{title}.csv", "data": data}
    return response