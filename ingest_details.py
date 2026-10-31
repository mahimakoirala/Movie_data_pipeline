import json
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("API_KEY")

def fetch_movie_details(language):
  results = []
  file_name = f"filtered/filtered_{language}_movies.json"
  os.makedirs("details", exist_ok=True)  # Create the 'details' directory if it doesn't exist
  with open(file_name, "r", encoding = "utf-8") as file:
    movies = json.load(file)

  for movie in movies:
    movie_id = movie['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    params = {
        "api_key": api_key
    }
    try:
      response = requests.get(url, params=params, timeout = 10)
      cast_response = requests.get(cast_url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
       print(f"error fetching details for movie ID {movie_id}: {e}")
       continue #skip to next if error

    # Extract information
    if response.status_code == 200 and cast_response.status_code == 200:
      print(f"Fetched details for movie ID {movie_id} : {movie['title']}")
      data = response.json()
      cast_data = cast_response.json()

      genres = [genre['name'] for genre in data.get('genres', [])]  # Get genre names
      cast_names = [actor['name'] for actor in cast_data['cast'][:5]]  # Get the first 5 cast members]
      temp_dict = {
              "id": data.get("id"),
              "title": data.get("original_title"),
              "original_language": data.get("original_language"),
              "release_date": data.get("release_date"),
              "budget" : data.get("budget"),
              "revenue" : data.get("revenue"),
              "runtime" : data.get("runtime"),
              "popularity": data.get("popularity"),
              "vote_average": data.get("vote_average"),
              "genres": genres,
              "cast": cast_names
              }
      results.append(temp_dict)

    else:
      print(f"Error occured:", {response.status_code}, {cast_response.status_code})
    time.sleep(0.4)

  with open(f"details/{language}_movie_details.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent = 4, ensure_ascii = False)

# fetch_movie_details("en")
fetch_movie_details("hi")


  
