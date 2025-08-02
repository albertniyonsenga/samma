from fastapi import APIRouter, Query
import requests
from app.utils import get_movie_data, save_as_json, save_as_csv

router = APIRouter()

@router.get("/movie")
def get_movie(title: str = Query(..., min_length=1)):
    return get_movie_data(title)

@router.get("/movie/export/json")
def export_json(title: str):
    return save_as_json(title)

@router.get("/movie/export/csv")
def export_csv(title: str):
    return save_as_csv(title)