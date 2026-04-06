# import streamlit as st
# import pickle
# import requests
# import time
# from requests.adapters import HTTPAdapter # Handle network issues gracefully
# from urllib3.util.retry import Retry # Retry failed requests automatically
# import os
# from dotenv import load_dotenv

# # load env
# load_dotenv()

# # =========================
# # 🔥 SESSION (IMPORTANT FIX)
# # =========================
# session = requests.Session() # Keep the connection open instead of reconnecting every time

# # Without session ❌
#     # Every request = new connection
#     # Slow + unstable
#     # More chance of failure
# # With session ✅
#     # Reuses connection
#     # Faster + stable
#     # Less chance of ConnectionResetError

# # | Parameter          | Meaning                             |
# # | ------------------ | ----------------------------------- |
# # | `total=5`          | Try max 5 times if request fails    |
# # | `backoff_factor=1` | Wait before retry (1s → 2s → 4s...) |
# # | `status_forcelist` | Retry only for these errors         |

# retries = Retry(
#     total=5,
#     backoff_factor=1,
#     status_forcelist=[429, 500, 502, 503, 504],
# )

# adapter = HTTPAdapter(max_retries=retries) # means: Apply retry logic to all HTTPS requests
# session.mount("https://", adapter)

# headers = {
#     "User-Agent": "Mozilla/5.0",
#     "Accept-Language": "en-US,en;q=0.9",
# }

# # =========================
# # 🎬 CONFIG
# # =========================
# st.set_page_config(
#     page_title="Movie Recommender System",
#     page_icon="🎬",
#     layout="wide",
# )

# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# # print(TMDB_API_KEY)
# TMDB_BASE_URL = "https://api.themoviedb.org/3"
# TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# # =========================
# # 📦 LOAD DATA
# # =========================
# @st.cache_data
# def load_data():
#     movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
#     similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))
#     return movies, similarity


# # =========================
# # 🔥 FIXED API FUNCTION
# # =========================
# @st.cache_data
# def fetch_movie_details(movie_title):
#     try:
#         clean_title = movie_title.strip()

#         # 🔍 SEARCH
#         search_url = f"{TMDB_BASE_URL}/search/movie"
#         params = {
#             "api_key": TMDB_API_KEY,
#             "query": clean_title,
#             "include_adult": False,
#         }

#         res = session.get(search_url, headers=headers, params=params, timeout=10)
#         res.raise_for_status()
#         data = res.json()

#         if data.get("results"):
#             movie = data["results"][0]
#             movie_id = movie["id"]

#             # 🎬 DETAILS + CREDITS
#             details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
#             credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"

#             details_res = session.get(
#                 details_url,
#                 headers=headers,
#                 params={"api_key": TMDB_API_KEY},
#                 timeout=10,
#             )

#             credits_res = session.get(
#                 credits_url,
#                 headers=headers,
#                 params={"api_key": TMDB_API_KEY},
#                 timeout=10,
#             )

#             details_res.raise_for_status()
#             credits_res.raise_for_status()

#             details = details_res.json()
#             credits = credits_res.json()

#             # 🎬 Director
#             director = "N/A"
#             for crew in credits.get("crew", []):
#                 if crew.get("job") == "Director":
#                     director = crew.get("name", "N/A")
#                     break

#             # 🖼️ Poster
#             poster_path = movie.get("poster_path")
#             poster_url = (
#                 f"{TMDB_IMAGE_BASE_URL}{poster_path}"
#                 if poster_path
#                 else "https://via.placeholder.com/500x750?text=No+Poster"
#             )

#             # 🌐 Language
#             lang = details.get("original_language", "N/A").upper()
#             lang_map = {
#                 "EN": "English",
#                 "HI": "Hindi",
#                 "ES": "Spanish",
#                 "FR": "French",
#                 "DE": "German",
#                 "IT": "Italian",
#                 "JA": "Japanese",
#                 "KO": "Korean",
#                 "ZH": "Chinese",
#                 "RU": "Russian",
#                 "PT": "Portuguese",
#                 "AR": "Arabic",
#             }
#             language = lang_map.get(lang, lang)

#             # 📅 Year
#             release_date = details.get("release_date", "")
#             year = release_date.split("-")[0] if release_date else "N/A"

#             return {
#                 "poster": poster_url,
#                 "year": year,
#                 "language": language,
#                 "director": director,
#                 "title": movie.get("title", movie_title),
#             }

#     except Exception as e:
#         print(f"Error fetching '{movie_title}': {e}")

#     return {
#         "poster": "https://via.placeholder.com/500x750?text=No+Poster",
#         "year": "N/A",
#         "language": "N/A",
#         "director": "N/A",
#         "title": movie_title,
#     }


# # =========================
# # 🎯 RECOMMEND FUNCTION
# # =========================
# def recommend(movie, movies_df, similarity_matrix, n=5):
#     index = movies_df[movies_df["title"] == movie].index[0]
#     distances = sorted(
#         list(enumerate(similarity_matrix[index])),
#         reverse=True,
#         key=lambda x: x[1],
#     )

#     return [movies_df.iloc[i[0]].title for i in distances[1 : n + 1]]


# # =========================
# # 🚀 MAIN APP
# # =========================
# def main():
#     st.title("🎬 Movie Recommender System")

#     movies_df, similarity_matrix = load_data()

#     selected_movie = st.selectbox("Select a movie:", movies_df["title"].values)

#     if st.button("Recommend"):

#         names = recommend(selected_movie, movies_df, similarity_matrix)

#         st.subheader("Recommended Movies")

#         cols = st.columns(5)

#         movie_details = []
#         for movie in names:
#             movie_details.append(fetch_movie_details(movie))
#             time.sleep(0.5)  # 🔥 prevents API blocking

#         for col, details in zip(cols, movie_details):
#             with col:
#                 st.image(details["poster"])
#                 st.write(f"**{details['title']}**")
#                 st.write(f"📅 {details['year']}")
#                 st.write(f"🌐 {details['language']}")
#                 st.write(f"🎬 {details['director']}")

#     st.balloons()


# if __name__ == "__main__":
#     main()

import streamlit as st
import pickle
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from dotenv import load_dotenv

# load env
load_dotenv()

# =========================
# 🔥 SESSION (IMPORTANT FIX)
# =========================
session = requests.Session()

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

# =========================
# 🎬 CONFIG
# =========================
st.set_page_config(
    page_title="Netflix Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Netflix Style Custom CSS
st.markdown(
    """
    <style>
    /* Import Netflix-like font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Netflix Dark Theme */
    .stApp {
        background: linear-gradient(to bottom, #141414 0%, #0a0a0a 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Netflix Style Hero Section */
    .hero-section {
        background: linear-gradient(90deg, #141414 0%, rgba(20,20,20,0.8) 50%, rgba(20,20,20,0) 100%);
        padding: 4rem 3rem;
        margin: -1rem -1rem 2rem -1rem;
        position: relative;
        overflow: hidden;
    }

    .hero-content {
        max-width: 800px;
        position: relative;
        z-index: 2;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #E50914 0%, #ff4d4d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        animation: slideInLeft 0.8s ease-out;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #e5e5e5;
        line-height: 1.5;
        margin-bottom: 2rem;
        animation: slideInLeft 0.8s ease-out 0.2s both;
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Netflix Style Select Box */
    .stSelectbox label {
        color: #e5e5e5 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.5px;
    }

    .stSelectbox div[data-baseweb="select"] {
        background: rgba(51, 51, 51, 0.9);
        border-radius: 4px;
        border: 1px solid #333;
        transition: all 0.3s ease;
    }

    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #E50914;
        background: rgba(68, 68, 68, 0.9);
    }

    /* Netflix Style Button */
    .stButton button {
        background: #E50914;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 4px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
    }

    .stButton button:hover {
        background: #f40612;
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(229, 9, 20, 0.4);
    }

    /* Netflix Row Title */
    .netflix-row {
        margin: 2rem 0 1rem 0;
        position: relative;
    }

    .netflix-row h2 {
        color: #e5e5e5;
        font-size: 1.8rem;
        font-weight: 600;
        margin-left: 2rem;
        position: relative;
        display: inline-block;
    }

    .netflix-row h2::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        height: 100%;
        width: 4px;
        background: #E50914;
        border-radius: 2px;
    }

    /* Netflix Style Movie Cards */
    .movie-card-netflix {
        background: #1a1a1a;
        border-radius: 4px;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        cursor: pointer;
        position: relative;
        animation: fadeInUp 0.6s ease-out;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .movie-card-netflix:hover {
        transform: scale(1.05);
        z-index: 10;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
    }

    .movie-card-netflix:hover .movie-info-netflix {
        background: #2a2a2a;
    }

    .movie-poster-netflix {
        width: 100%;
        height: auto;
        aspect-ratio: 2/3;
        object-fit: cover;
        transition: all 0.3s ease;
    }

    .movie-info-netflix {
        padding: 1rem;
        background: #1a1a1a;
        transition: all 0.3s ease;
        flex-grow: 1;
    }

    .movie-title-netflix {
        font-size: 0.9rem;
        font-weight: 600;
        color: #e5e5e5;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        min-height: 2.4rem;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    .movie-meta-netflix {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #999;
    }

    .movie-year-netflix {
        background: rgba(229, 9, 20, 0.2);
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        color: #E50914;
        font-weight: 600;
    }

    .movie-language-netflix {
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }

    .movie-director-netflix {
        font-size: 0.7rem;
        color: #666;
        margin-top: 0.5rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* Hover Badge */
    .movie-badge {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        background: rgba(0, 0, 0, 0.7);
        padding: 0.3rem 0.6rem;
        border-radius: 3px;
        font-size: 0.7rem;
        font-weight: 600;
        color: #E50914;
        opacity: 0;
        transition: opacity 0.3s ease;
        backdrop-filter: blur(5px);
    }

    .movie-card-netflix:hover .movie-badge {
        opacity: 1;
    }

    /* Loading Animation */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }

    .netflix-loader {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid rgba(229, 9, 20, 0.3);
        border-radius: 50%;
        border-top-color: #E50914;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Divider */
    .netflix-divider {
        height: 2px;
        background: linear-gradient(90deg, #E50914, transparent);
        margin: 2rem 0;
    }

    /* Footer */
    .netflix-footer {
        text-align: center;
        padding: 3rem 2rem 2rem;
        color: #666;
        font-size: 0.8rem;
        border-top: 1px solid #222;
        margin-top: 3rem;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }

    ::-webkit-scrollbar-thumb {
        background: #E50914;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #f40612;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .hero-subtitle {
            font-size: 1rem;
        }

        .netflix-row h2 {
            font-size: 1.3rem;
            margin-left: 1rem;
        }

        .movie-title-netflix {
            font-size: 0.8rem;
        }
    }

    /* Success/Warning Messages */
    .stAlert {
        background: rgba(229, 9, 20, 0.1);
        border-left: 4px solid #E50914;
        color: #e5e5e5;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #E50914 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# print(TMDB_API_KEY)
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# =========================
# 📦 LOAD DATA
# =========================
@st.cache_data
def load_data():
    movies = pickle.load(open("artifacts/movie_list.pkl", "rb"))
    similarity = pickle.load(open("artifacts/similarity.pkl", "rb"))
    return movies, similarity


# =========================
# 🔥 FIXED API FUNCTION
# =========================
@st.cache_data
def fetch_movie_details(movie_title):
    try:
        clean_title = movie_title.strip()

        # 🔍 SEARCH
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": clean_title,
            "include_adult": False,
        }

        res = session.get(search_url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if data.get("results"):
            movie = data["results"][0]
            movie_id = movie["id"]

            # 🎬 DETAILS + CREDITS
            details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
            credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"

            details_res = session.get(
                details_url,
                headers=headers,
                params={"api_key": TMDB_API_KEY},
                timeout=10,
            )

            credits_res = session.get(
                credits_url,
                headers=headers,
                params={"api_key": TMDB_API_KEY},
                timeout=10,
            )

            details_res.raise_for_status()
            credits_res.raise_for_status()

            details = details_res.json()
            credits = credits_res.json()

            # 🎬 Director
            director = "N/A"
            for crew in credits.get("crew", []):
                if crew.get("job") == "Director":
                    director = crew.get("name", "N/A")
                    break

            # 🖼️ Poster
            poster_path = movie.get("poster_path")
            poster_url = (
                f"{TMDB_IMAGE_BASE_URL}{poster_path}"
                if poster_path
                else "https://via.placeholder.com/500x750?text=No+Poster"
            )

            # 🌐 Language
            lang = details.get("original_language", "N/A").upper()
            lang_map = {
                "EN": "English",
                "HI": "Hindi",
                "ES": "Spanish",
                "FR": "French",
                "DE": "German",
                "IT": "Italian",
                "JA": "Japanese",
                "KO": "Korean",
                "ZH": "Chinese",
                "RU": "Russian",
                "PT": "Portuguese",
                "AR": "Arabic",
            }
            language = lang_map.get(lang, lang)

            # 📅 Year
            release_date = details.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"

            return {
                "poster": poster_url,
                "year": year,
                "language": language,
                "director": director,
                "title": movie.get("title", movie_title),
            }

    except Exception as e:
        print(f"Error fetching '{movie_title}': {e}")

    return {
        "poster": "https://via.placeholder.com/500x750?text=No+Poster",
        "year": "N/A",
        "language": "N/A",
        "director": "N/A",
        "title": movie_title,
    }


# =========================
# 🎯 RECOMMEND FUNCTION
# =========================
def recommend(movie, movies_df, similarity_matrix, n=5):
    index = movies_df[movies_df["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity_matrix[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    return [movies_df.iloc[i[0]].title for i in distances[1 : n + 1]]


# =========================
# 🚀 MAIN APP
# =========================
def main():
    # Netflix Hero Section
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-content">
                <div class="hero-title">NETFLIX</div>
                <div class="hero-title" style="font-size: 2.5rem; -webkit-text-fill-color: white; background: none;">
                    Movie Recommender
                </div>
                <div class="hero-subtitle">
                    Find your next favorite movie. Personalized recommendations based on what you love.
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    movies_df, similarity_matrix = load_data()

    # Netflix Style Selection Panel
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            '<div style="background: #1a1a1a; padding: 2rem; border-radius: 8px; margin: 1rem 0;">',
            unsafe_allow_html=True,
        )

        selected_movie = st.selectbox(
            "🎬 SELECT A MOVIE YOU LOVE",
            movies_df["title"].values,
            help="Choose a movie and we'll find similar recommendations",
        )

        if st.button("🔍 GET RECOMMENDATIONS", use_container_width=True):
            with st.spinner("🎬 Finding your next watch..."):
                names = recommend(selected_movie, movies_df, similarity_matrix)

                # Netflix Style Row
                st.markdown(
                    f"""
                    <div class="netflix-row">
                        <h2>Because you watched {selected_movie}</h2>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                # Fetch movie details
                movie_details = []
                progress_bar = st.progress(0)
                for idx, movie in enumerate(names):
                    movie_details.append(fetch_movie_details(movie))
                    progress_bar.progress((idx + 1) / len(names))
                    time.sleep(0.3)
                progress_bar.empty()

                # Display Netflix Style Row
                cols = st.columns(5)

                for idx, (col, details) in enumerate(zip(cols, movie_details)):
                    with col:
                        # Get rating stars for visual appeal
                        rating_stars = (
                            "⭐" * (5 - idx) + "☆" * idx if idx < 5 else "⭐⭐⭐"
                        )

                        st.markdown(
                            f"""
                            <div class="movie-card-netflix">
                                <div class="movie-badge">{rating_stars}</div>
                                <img src="{details['poster']}" class="movie-poster-netflix" loading="lazy">
                                <div class="movie-info-netflix">
                                    <div class="movie-title-netflix">{details['title']}</div>
                                    <div class="movie-meta-netflix">
                                        <span class="movie-year-netflix">{details['year']}</span>
                                        <span class="movie-language-netflix">
                                            <span>🌐</span> {details['language']}
                                        </span>
                                    </div>
                                    <div class="movie-director-netflix">
                                        🎬 {details['director']}
                                    </div>
                                </div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                # Additional Recommendations Row (Top Picks For You)
                st.markdown(
                    f"""
                    <div class="netflix-row" style="margin-top: 3rem;">
                        <h2>Top Picks For You</h2>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                # Create second row with same movies but different layout
                cols2 = st.columns(5)
                for idx, (col, details) in enumerate(zip(cols2, movie_details)):
                    with col:
                        st.markdown(
                            f"""
                            <div class="movie-card-netflix" style="animation-delay: {idx * 0.1}s">
                                <img src="{details['poster']}" class="movie-poster-netflix" loading="lazy">
                                <div class="movie-info-netflix">
                                    <div class="movie-title-netflix">{details['title']}</div>
                                    <div class="movie-meta-netflix">
                                        <span class="movie-year-netflix">{details['year']}</span>
                                    </div>
                                </div>
                            </div>
                        """,
                            unsafe_allow_html=True,
                        )

                st.markdown(
                    '<div class="netflix-divider"></div>', unsafe_allow_html=True
                )

                # Success message
                st.success(
                    f"✨ Found {len(names)} great recommendations for you! Enjoy watching! 🍿"
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # Netflix Footer
    st.markdown(
        """
        <div class="netflix-footer">
            <p>🎬 Netflix Style Movie Recommender System</p>
            <p>Powered by TMDB API | AI-Powered Recommendations</p>
            <p style="font-size: 0.7rem; margin-top: 1rem;">© 2024 - Find Your Next Favorite Movie</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Balloons animation for that Netflix celebration moment
    st.balloons()


if __name__ == "__main__":
    main()
