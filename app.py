import streamlit as st
import pickle
import pandas as pd
import requests
import bz2

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=c1d76c9d5aa6141f10006d5cb7ac99f9&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
#https://api.themoviedb.org/3/movie/550?api_key=c1d76c9d5aa6141f10006d5cb7ac99f9
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id =movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from
        recommended_movies_poster.append(fetch_poster(movie_id))
    return (recommended_movies,recommended_movies_poster)

movies_dict = pickle.load(open("movie_dict.pkl","rb"))
#similarity = pickle.load(open("similarity.pkl","rb"))
ifile = bz2.BZ2File("similarity1.pkl",'rb')
similarity = pickle.load(ifile)
movies = pd.DataFrame(movies_dict)
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
"type your movie name",
movies["title"].values
)

if st.button("Recommend"):
    names,poster = recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.beta_columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])