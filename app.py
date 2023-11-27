import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

def recommend(movie, movies_list, similarity, num_recommendations=5):
    try:
        movie_index = movies_list[movies_list["title"] == movie].index[0]
    except IndexError:
        st.error(f"No movie found with the title: {movie}")
        return []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
    recommend_movies = []
    recommend_movies_poster = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].id  # Get the movie ID for the current iteration
        recommend_movies.append(movies_list.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

# Load data
movies_list = pickle.load(open("themovies.pkl", "rb"))
similarity = pickle.load(open("thesimilarirty.pkl", "rb"))

# Display app title
st.title("Movie Recommender System By Lakshya Varshney")

# User selects a movie from the dropdown
selected_movie_name = st.selectbox('Choose a movie', movies_list["title"].values)

# Button to trigger recommendations
if st.button("Recommend"):
    num_recommendations = 5  # Set the number of recommendations you want to display
    names, posters = recommend(selected_movie_name, movies_list, similarity, num_recommendations)

    for name, poster in zip(names, posters):
        st.header(name)
        st.image(poster)
