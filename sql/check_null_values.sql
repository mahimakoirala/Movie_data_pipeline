SELECT 'dim_movies.movie_id' AS column_name,
       COUNT(*) AS null_count
FROM dim_movies
WHERE movie_id IS NULL

UNION ALL

SELECT 'dim_genres.genre_id',
       COUNT(*)
FROM dim_genres
WHERE genre_id IS NULL

UNION ALL

SELECT 'dim_cast.cast_id',
       COUNT(*)
FROM dim_cast
WHERE cast_id IS NULL

UNION ALL

SELECT 'fact_movies.movie_id',
       COUNT(*)
FROM fact_movies
WHERE movie_id IS NULL;
