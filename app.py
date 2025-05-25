import pickle
import streamlit as st
import requests

# --- Page setup ---
st.set_page_config(layout="wide", page_title="🎬 Movie Recommender")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
    }
    .main-title {
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        color: #00ffd5;
        font-size: 42px;
        padding-bottom: 20px;
    }
    .subtitle {
        color: #ffffff;
        font-size: 20px;
        padding-bottom: 10px;
    }
    .movie-title {
        color: #FFD700;
        font-size: 16px;
        text-align: center;
        margin-top: 10px;
    }
    .stSelectbox > div {
        font-size: 18px;
    }
    .stButton>button {
        background-color: #00ffd5;
        color: black;
        font-weight: bold;
        font-size: 18px;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00bfa5;
    }
    img:hover {
        transform: scale(1.05);
        transition: transform 0.3s;
        border: 2px solid #00ffd5;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("<div class='main-title'>🎬 Movie Recommender System Using Machine Learning</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Select a movie from the dropdown to get recommendations</div>", unsafe_allow_html=True)

# --- Fetch Poster Function ---
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750.png?text=Unavailable"

# --- Recommend Movies Function ---
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Selected movie not found in dataset.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Top 5
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# --- Load Data ---
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# --- Movie Dropdown ---
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Choose a movie", movie_list)

# --- Show Recommendations ---
if st.button('🔍 Show Recommendation'):
    names, posters = recommend(selected_movie)
    if names and posters:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_column_width=True)
                st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
