--purpose: identify duplicate and NULL primary keys

--1. check duplicate movie id
SELECT movie_id, count(*) 
FROM dim_movies 
GROUP BY movie_id
HAVING count(*) > 1;

--2. Check null movie IDs;
SELECT COUNT(*)
FROM dim_movies
WHERE movie_id is NULL;

--3. Check duplicate genre ID;
SELECT genre_id, COUNT(*)
FROM dim_genres
GROUP BY genre_id
HAVING COUNT(*) > 1;

--4. Check duplicate cast ID
SELECT cast_id, COUNT(*)
FROM dim_cast
GROUP BY cast_id
HAVING COUNT(*) > 1;

-- Referential integrity check: bridge_genres
-- Result: 0 orphan records found.
-- All movie_id and genre_id values have matching dimension records.
SELECT bg.*
FROM bridge_genres bg
LEFT JOIN dim_movies dm
    ON bg.movie_id = dm.movie_id
LEFT JOIN dim_genres dg
    ON bg.genre_id = dg.genre_id
WHERE dm.movie_id IS NULL
   OR dg.genre_id IS NULL;

--bridge_cast
SELECT bc.*
FROM bridge_cast bc
LEFT JOIN dim_movies dm
    ON bc.movie_id = dm.movie_id
LEFT JOIN dim_cast dc
    ON bc.cast_id = dc.cast_id
WHERE dm.movie_id IS NULL
   OR dc.cast_id IS NULL;

--fact_movies
SELECT fm.*
FROM fact_movies fm
LEFT JOIN dim_movies dm
    ON fm.movie_id = dm.movie_id
WHERE dm.movie_id IS NULL;
