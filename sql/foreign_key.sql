-- Fact table
ALTER TABLE fact_movies
ADD CONSTRAINT fk_fact_movies_dim_movies
FOREIGN KEY (movie_id)
REFERENCES dim_movies(movie_id);

-- Genre bridge
ALTER TABLE bridge_genres
ADD CONSTRAINT fk_bridge_genres_dim_movies
FOREIGN KEY (movie_id)
REFERENCES dim_movies(movie_id);

ALTER TABLE bridge_genres
ADD CONSTRAINT fk_bridge_genres_dim_genres
FOREIGN KEY (genre_id)
REFERENCES dim_genres(genre_id);

-- Cast bridge
ALTER TABLE bridge_cast
ADD CONSTRAINT fk_bridge_cast_dim_movies
FOREIGN KEY (movie_id)
REFERENCES dim_movies(movie_id);

ALTER TABLE bridge_cast
ADD CONSTRAINT fk_bridge_cast_dim_cast
FOREIGN KEY (cast_id)
REFERENCES dim_cast(cast_id);
