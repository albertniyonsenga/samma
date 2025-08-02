from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_movie_success():
    response = client.get("/movie", params={"title": "Inception"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert "plot" in data
    assert "cast" in data

def test_get_movie_not_found():
    response = client.get("/movie", params={"title": "nonexistentmovie123"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found!"

def test_export_json_success():
    response = client.get("/movie/export/json", params={"title": "Inception"})
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert data["title"] == "Inception"

def test_export_csv_structure():
    response = client.get("/movie/export/csv", params={"title": "Inception"})
    assert response.status_code == 200
    data = response.json()
    assert "csv" in data
    assert data["csv"].endswith(".csv")
    assert isinstance(data["data"], dict)