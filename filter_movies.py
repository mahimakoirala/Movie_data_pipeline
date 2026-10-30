import json
import pandas as pd

languages = ['en', 'hi']

def fetch_details_from_json():
  for lang in languages:
    file_name_1 = f"raw_{lang}_movies.json"
    file_name_2 = f"filtered_{lang}_movies.json"
    try:
      with open(file_name_1, "r", encoding = "utf-8") as file:
         movies = json.load(file)

      df = pd.DataFrame(movies)
      #filter movies by release date
      new_df = df.loc[(df['release_date'] >= '2018-01-01') & (df['release_date'] <= '2025-12-31')]
      #convert filterted df to JSON
      json_str =  new_df.to_json(orient = 'records', force_ascii = False, indent = 4, date_format = 'iso')

      #save filtered json
      with open(file_name_2, "w", encoding = "utf-8") as file:
        file.write(json_str)
      print(f"saved {len(new_df)} movies to {file_name_2}")
    except FileNotFoundError:
      print(f"File {file_name_1} not found. Please ensure the raw data file exists.")

fetch_details_from_json()
