import streamlit as st
import pickle
import pandas as pd

# Load the movie dictionary and similarities
movie_dict = pickle.load(open('Movies-dict1_new.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarities = pickle.load(open('Similarties_new.pkl', 'rb'))

# Set the title of the app
st.title('🎬 Movie Recommendation System')

# Dropdown for selecting a movie
select_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

# Define recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarities[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    poster_paths = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])

        poster_path = movies.iloc[i[0]].get('poster_path', '')
        if poster_path:
            full_poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            full_poster_url = ''
        poster_paths.append(full_poster_url)

    return recommended_movies, poster_paths


# Recommend button
if st.button("Recommend"):
    recommendations, poster_paths = recommend(select_movie)
    st.subheader("Recommended Movies:")
    for title, poster in zip(recommendations, poster_paths):
        st.markdown(f"**{title}**")
        if poster:
            st.image(poster, width=150)
        else:
            st.write("Poster not available.")
