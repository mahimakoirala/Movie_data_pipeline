from logger_config import get_logger

logger = get_logger(__name__)

class DataQualityError(Exception):
    pass

def check_no_duplicate_movie_ids(df):
    """
    Check for duplicate movie IDs in the DataFrame.
    Raises a DataQualityError if duplicates are found.
    """
    duplicates = df['movie_id'].duplicated().sum()
    if duplicates > 0:
        raise DataQualityError(f"Data quality issue: Found {duplicates} duplicate movie IDs in dim_movies")
    logger.info("dim_movies: no duplicates movie IDs found.")

def check_budget_non_negative(df):
    """check that the bidget has non-negative values"""
    invalid = df[df['budget'] < 0]  #find rows with negative budget. 
    if len(invalid) > 0:
        raise DataQualityError(f"data quality issue: found {len(invalid)} rows with negative budget in dim_movies")
    logger.info("fact_movies: no negative bidgets")

def check_vote_average_range(df):
    #check that the vote average is between 0 and 10
    invalid = df[(df['vote_average'] < 0) | (df['vote_average'] > 10)]
    if len(invalid) > 0:
        raise DataQualityError(f"{len(invalid)} movies have vote_average outside 0-10 range")
    logger.info("fact_movies: vote_average is within the valid range")
  
