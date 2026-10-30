import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
url = "https://api.themoviedb.org/3/discover/movie"

def fetch_from_api(language):
  temp_list = []
  count_results = 0
  file_name = f"raw_{language}_movies.json"

  for page in range(1,101):
    params = {"api_key": api_key, "with_original_language": language, "page": page}
    try:
      response = requests.get(url, params = params, timeout = 30)
      response.raise_for_status()  # Raise an exception for HTTP errors

      print("Fetching data from API...")
      print(f"fetching page {page}, currently stored results = {count_results}")

      data = response.json() 
      temp_list.extend(data['results']) # Extend the temporary list with the results from the current page
      count_results += len(data["results"]) 
    except requests.exceptions.RequestException as e:
      print(f"error fetching page {page}: {e}")
    time.sleep(0.4) # Sleep for 0.4 seconds to avoid hitting the API rate limit
    

  with open(file_name, "w", encoding = "utf-8") as f:
    json.dump(temp_list, f, indent = 4, ensure_ascii = False) 
  print(f"\nSaved {count_results} results to {file_name}")


fetch_from_api("en")
fetch_from_api("hi")
