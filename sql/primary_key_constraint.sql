ALTER TABLE dim_movies
ADD CONSTRAINT pk_dim_movies PRIMARY KEY (movie_id);
GO
ALTER TABLE dim_genres
ADD CONSTRAINT pk_dim_genres PRIMARY KEY (genre_id);
GO
ALTER TABLE dim_cast
ADD CONSTRAINT pk_dim_cast PRIMARY KEY (cast_id);
GO
ALTER TABLE fact_movies
ADD CONSTRAINT pk_fact_movies PRIMARY KEY (movie_id);
GO
ALTER TABLE bridge_genres
ADD CONSTRAINT pk_bridge_genres PRIMARY KEY (movie_id, genre_id);
GO
ALTER TABLE bridge_cast
ADD CONSTRAINT pk_bridge_cast
PRIMARY KEY (movie_id, cast_id);
