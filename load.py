from sqlalchemy import create_engine, URL
from sqlalchemy.types import Integer, DateTime, BIGINT
from logger_config import get_logger
import os
from dotenv import load_dotenv

logger= get_logger(__name__)

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT") 
POSTGRES_DB = os.getenv("POSTGRES_DB")

url_object = URL.create(
    "postgresql+psycopg2",
    username = POSTGRES_USER,
    password = POSTGRES_PASSWORD,
    host = POSTGRES_HOST,
    database = POSTGRES_DB,
    port = POSTGRES_PORT
)

engine = create_engine(url_object)

def load_data_to_postgres(dim_movies_df,dim_genres_df, dim_cast_df, fact_movies_df, bridge_genres_df, bridge_cast_df):
    dtype_dict = {
        'release_date' : DateTime(),
        'revenue': BIGINT(),
        'runtime': Integer(),
        'budget': BIGINT(),
    }
    tables = [
    (dim_movies_df, 'dim_movies', None),
    (dim_genres_df, 'dim_genres', None),
    (dim_cast_df, 'dim_cast', None),
    (bridge_genres_df, 'bridge_genres', None),
    (bridge_cast_df, 'bridge_cast', None)
]
    for df, table_name, dtype in tables:
        try:
            df.to_sql(name = table_name, con = engine, if_exists = 'replace', index = False, dtype = dtype_dict)
            logger.info(f"data {len(df)} rows into '{table_name}' table in postgres")
        except Exception as e:
            logger.error(f"error loading data into '{table_name}' table in postgres: {e}")

    fact_movies_df.to_sql(name = 'fact_movies', con = engine, if_exists = 'replace', index = False, dtype = dtype_dict)
    logger.info(f"loaded {len(fact_movies_df)} rows into 'fact_movies' table.")

if __name__ == "__main__":
    from transform import load_movie_details, create_dataframes 
    logger.info("starting data load pipeline....")
    all_movie_details = load_movie_details()

    dim_movies_df, dim_genres_df, dim_cast_df, fact_movies_df, bridge_genres_df, bridge_cast_df = create_dataframes(all_movie_details)
    load_data_to_postgres(dim_movies_df, dim_genres_df, dim_cast_df, fact_movies_df, bridge_genres_df, bridge_cast_df)

    logger.info("data load pipeline completed successfully.")