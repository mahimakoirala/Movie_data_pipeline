import json
import logging
import os
import pandas as pd
from logger_config import get_logger

logger = get_logger(__name__)

languages = ['en', 'hi']  # List of languages to process

def load_movie_details():
    all_movie_details = []
    for lang in languages:
        file_name = f"details/{lang}_movie_details.json"

        try:
            with open(file_name, "r", encoding = 'utf-8') as file:
              movie_details = json.load(file)
            if movie_details:
                logger.info(f"First movie record: {movie_details[0]}")
                logger.info(f"Available keys: {movie_details[0].keys()}")
            all_movie_details.extend(movie_details)
            logger.info(f"loaded {len(movie_details)} movie details for language '{lang}' from  {file_name}")
        except FileNotFoundError:
            logger.error(f"error: the file {file_name}")
    logger.info(f'total loaded movies: {len(all_movie_details)}.')
    return all_movie_details

def create_fact_movies(all_movie_details):
    fact_movies = []
    for movie in all_movie_details:
        temp_dict = {
            'movie_id': movie['id'],
            'release_date': movie['release_date'],
            'popularity': movie['popularity'],
            'revenue': movie['revenue'],
            'runtime': movie['runtime'],
            'vote_average': movie['vote_average'],
            'budget': movie['budget'],
        }
        fact_movies.append(temp_dict)
    return fact_movies

def create_dim_movies(all_movie_details):
    dim_movies = []
    for movie in all_movie_details:
        temp_dict = {
          'movie_id': movie['id'],
          'title': movie['title'],
          'original_language': movie['original_language'],
        }
        dim_movies.append(temp_dict)
    df = pd.DataFrame(dim_movies)
    df = df.drop_duplicates(subset = ['movie_id'], keep = 'first')  # Remove duplicates based on 'id' column
    return df.to_dict(orient = 'records')  # Convert DataFrame back to list of dictionaries

def create_dim_genres(all_movie_details):
    all_genre_names = []
    dim_genres = []
    for movie in all_movie_details:
        for genre in movie['genres']:
            if genre not in all_genre_names:
                all_genre_names.append(genre)
    unique_genres = sorted(all_genre_names)

    for genre_id, genre_name in enumerate(unique_genres, start = 1):
        temp_dict = {
            'genre_id': genre_id,
            'genre_name': genre_name
        }
        dim_genres.append(temp_dict)
    return dim_genres

def create_bridge_genres(all_movie_details, dim_genres):
    bridge_genres = []
    genre_lookup = {g['genre_name']: g['genre_id'] for g in dim_genres} #lookup dictionary for genre_name to genre_id mapping

    for movie in all_movie_details:
        for genre_name in movie['genres']:
            temp_dict = {
                'movie_id': movie['id'],
                'genre_id': genre_lookup[genre_name]
            }
            bridge_genres.append(temp_dict)
    return bridge_genres

def create_dim_cast(all_movie_details):
    all_cast_names = []
    dim_cast = []

    for movie in all_movie_details:
        for cast in movie['cast']:
            if cast not in all_cast_names:
                all_cast_names.append(cast)
    unique_cast = sorted(all_cast_names)

    for cast_id, cast_name in enumerate(unique_cast, start = 1):
        temp_dict = {
            'cast_id': cast_id,
            'cast_name': cast_name
        }
        dim_cast.append(temp_dict)
    return dim_cast
            
def create_bridge_cast(all_movies_details, dim_cast):
    bridge_cast =[]
    cast_lookup = {c['cast_name']: c['cast_id'] for c in dim_cast} #lookup dictionary for cast_name to cast_id mapping

    for movie in all_movies_details:
      for cast_order, cast_name in enumerate(movie['cast'], start = 1):
          temp_dict = {
              'movie_id': movie['id'],
              'cast_id': cast_lookup[cast_name],
              'cast_order': cast_order
          }
          bridge_cast.append(temp_dict)
    return bridge_cast

def check_nulls(df, table_name):
    count = df.isnull().sum()

    if count.sum() == 0:
        logger.info(f"{table_name}: No null values found.")
    else:
        logger.warning(f"{table_name} null counts:\n{count}")

def create_dataframes(all_movie_details):
    #building dimension tables
    dim_movies = create_dim_movies(all_movie_details)
    dim_genres = create_dim_genres(all_movie_details)
    dim_cast = create_dim_cast(all_movie_details)

    #building fact and bridge tables  
    fact_movies = create_fact_movies(all_movie_details)

    bridge_genres = create_bridge_genres(all_movie_details, dim_genres)
    bridge_cast = create_bridge_cast(all_movie_details, dim_cast)

    #creating dataframes
    dim_movies_df = pd.DataFrame(dim_movies)
    dim_genres_df = pd.DataFrame(dim_genres)
    dim_cast_df = pd.DataFrame(dim_cast)

    fact_movies_df = pd.DataFrame(fact_movies)
    bridge_genres_df = pd.DataFrame(bridge_genres)
    bridge_cast_df = pd.DataFrame(bridge_cast)

    #type fix and handling null values
    fact_movies_df['release_date'] = pd.to_datetime(fact_movies_df['release_date'])
    fact_movies_df['revenue'] = (fact_movies_df['revenue'].fillna(0).astype(int))
    fact_movies_df['runtime'] = fact_movies_df['runtime'].replace(0, pd.NA).astype('Int64')  # Replace 0 with NA and convert to nullable integer type
    fact_movies_df['budget'] = fact_movies_df['budget'].replace(0, pd.NA).astype('Int64')  # Replace 0 with NA and convert to nullable integer type

  
    #popularity and vore_average stay as float

    #checking for nulls
    check_nulls(dim_movies_df, "dim_movies")
    check_nulls(dim_genres_df, "dim_genres")    
    check_nulls(dim_cast_df, "dim_cast")
    check_nulls(fact_movies_df, "fact_movies")
    check_nulls(bridge_genres_df, "bridge_genres")
    check_nulls(bridge_cast_df, "bridge_cast")

    return dim_movies_df, dim_genres_df, dim_cast_df, fact_movies_df, bridge_genres_df, bridge_cast_df
