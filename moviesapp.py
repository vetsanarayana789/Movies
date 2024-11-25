import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd

# Title for the app
st.title("🎬 Movie Recommendations 🎬")
st.write("Select your favorite genre, and we'll recommend some movies!")

# Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch the available genres from the database
genres_df = session.table("MOVIE_RECOMMENDATIONS.PUBLIC.MOVIE_OPTIONS").select(col("GENRE")).distinct().to_pandas()

# Allow the user to select a genre
selected_genre = st.selectbox('Choose your favorite genre:', genres_df['GENRE'])

# Fetch and display movie recommendations based on the selected genre
if selected_genre:
    st.write(f"You selected *{selected_genre}*. Here are some movie recommendations:")
    movies_df = session.table("MOVIE_RECOMMENDATIONS.PUBLIC.MOVIE_OPTIONS").filter(col("GENRE") == selected_genre).select(col("MOVIE")).to_pandas()
    st.write(movies_df)

# Option to add a new movie recommendation
st.write("Have a favorite movie? Add your own recommendation!")
new_movie = st.text_input("Movie Title")
new_genre = st.selectbox("Movie Genre", genres_df['GENRE'])

if st.button('Submit Movie Recommendation'):
    if new_movie and new_genre:
        insert_query = f"INSERT INTO MOVIE_RECOMMENDATIONS.PUBLIC.MOVIE_OPTIONS (GENRE, MOVIE) VALUES ('{new_genre}', '{new_movie}')"
        session.sql(insert_query).collect()
        st.success(f"Movie '{new_movie}' added to {new_genre} genre!")
    else:
        st.error("Please fill out both the movie title and genre!")
