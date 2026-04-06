# 🎬 Movie Recommender System (Streamlit App)

A modern, interactive **Movie Recommendation Web App** built using **Machine Learning + Streamlit**, designed with a sleek UI and real-time movie data integration.

---

## 📂 Project Structure

```
MOVIE PREDICTION/
│
├── artifacts/              # Saved models / intermediate files (optional)
├── data/                   # Raw or processed datasets
├── env/                    # Virtual environment (not required in repo)
│
├── movie_app.py            # Main Streamlit application (UI + logic)
├── movie.py                # Recommendation logic / preprocessing
├── test_api.py             # TMDb API testing script
│
├── requirements.txt        # Project dependencies
├── readme.md               # Project documentation
│
├── movie_list.pkl          # Movie dataset (required)
└── similarity.pkl          # Similarity matrix (required)
```

---

## 🚀 Features

### 🎨 Modern UI
- Glassmorphism + gradient design  
- Smooth animations & hover effects  
- Responsive layout (mobile-friendly)

### 🤖 Smart Recommendation Engine
- Content-based filtering  
- Uses:
  - Genres  
  - Keywords  
  - Cast  
  - Crew  
  - Overview  
- Powered by **Cosine Similarity**

### 🎥 Rich Movie Details
- Movie posters (via TMDb API)
- Release year
- Original language
- Director name

---

## ⚙️ Prerequisites

Make sure you have:

- Python **3.8+**
- Required files:
  - `movie_list.pkl`
  - `similarity.pkl`

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd MOVIE-PREDICTION
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run movie_app.py
```

App will open at:

```
http://localhost:8501
```

---

## 🧠 How It Works

1. User selects a movie  
2. System finds similarity scores  
3. Top 5 similar movies are recommended  
4. TMDb API fetches posters & metadata  

---

## 🧪 API Configuration (Important)

This project uses **TMDb API**.

### 🔑 Setup your API key:

1. Get key from: https://www.themoviedb.org/settings/api  
2. Replace in `movie_app.py`:

```python
TMDB_API_KEY = "your_api_key_here"
```

---

## 🛠️ Customization

You can easily modify:

### 🔢 Number of Recommendations
```python
recommend(movie_name, n_recommendations=5)
```

### 🎨 UI Design
Edit CSS inside:
```python
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)
```

### 📊 Layout
```python
st.columns(5)  # Change grid layout
```

---

## 🧰 Tech Stack

- **Streamlit** → Web UI  
- **Pandas** → Data processing  
- **Scikit-learn** → Similarity computation  
- **Pickle** → Model storage  
- **Requests** → API calls  
- **TMDb API** → Movie data  

---

## 🐞 Troubleshooting

### ❌ Missing `.pkl` files
✔ Ensure:
```
movie_list.pkl
similarity.pkl
```
are in root folder

---

### ❌ Posters not loading
✔ Check:
- Internet connection  
- Valid TMDb API key  

---

### ❌ Slow performance
✔ First run loads data → later runs faster (cached)

---

## 📌 Future Improvements

- Add **user-based recommendations**
- Add **search bar with autocomplete**
- Deploy on **Streamlit Cloud / AWS**
- Add **movie trailers**
- Use **vector DB (FAISS)** for scaling

---

## 📜 License

This project is open-source and intended for **learning purposes**.

---

## ❤️ Credits

- Dataset & posters: **TMDb (The Movie Database)**
- Built with **Streamlit + ML**