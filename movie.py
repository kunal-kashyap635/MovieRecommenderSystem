import pandas as pd
import ast
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movie = pd.read_csv("data/tmdb_5000_movies.csv")
print(movie.head())

credits = pd.read_csv("data/tmdb_5000_credits.csv")
print(credits.head())

print("Movie :- ",movie.shape)
print("Credits :- ",credits.shape)

movies = movie.merge(credits,on='title')
print(movies.head(5))

print(movies.shape)
print("columns :- ",movies.columns)

movies = movies.drop(['budget','homepage','original_language','original_title','popularity','production_companies','production_countries','release_date','revenue','runtime','spoken_languages','status','tagline','vote_average','vote_count','id'],axis='columns')
print(movies.head(2))

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

print(movies.head(5))

## removing Null values
print(movies.isnull().sum()) 
movies.dropna(inplace=True)
print(movies.isnull().sum())
print(movies.shape)

## detecting duplicated values
print('duplicate values : ',movies.duplicated().sum())

## ast is a module that we need for converting string into list. You can simply see the example below.
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

import ast
def convert(text):
    l = []
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l
movies['genres'] = movies['genres'].apply(convert)

def convert1(text):
    l = []
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l
movies['keywords'] = movies['keywords'].apply(convert1)

def convert_cast(text):
    l = []
    counter = 0
    for i in ast.literal_eval(text):
        if (counter < 3):
            l.append(i['name'])
        counter += 1
    return l
movies['cast'] = movies['cast'].apply(convert_cast)
print(movies.head(2))

def fetch_director(text):
    l = []
    for i in ast.literal_eval(text):
        if(i['job'] == 'Director'):
            l.append(i['name'])
            break
    return l
movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x : x.split()) ## converting overview by using lambda function takes a string x and splits it into a list of words.

## remove spaces from cast and crew
def remove_space(word):
    l = []
    for i in word:
        l.append(i.replace(" ",""))
    return l
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

dataframe1 = movies[['movie_id','title','tags']]
print(dataframe1.head(2))

dataframe1['tags'] = dataframe1['tags'].apply(lambda x : " ".join(x)) # lambda function takes x as input and joins all the elements in x into a single string, separated by spaces. for example :- ['python', 'data', 'analysis'] like this "python data analysis".

## converting the tags data into lower case
dataframe1['tags'] = dataframe1['tags'].apply(lambda x : x.lower())
print(dataframe1.iloc[0]['tags'])

## here we find the root word of same words
ps = PorterStemmer()
def stems(text):
    l = []
    for i in text.split():
        l.append(ps.stem(i))
    return " ".join(l)
dataframe1['tags'] = dataframe1['tags'].apply(stems)
dataframe1.iloc[0]['tags']

## ML & AI is working on numerical data so we convert into numerical data by using counter vectorizer
cv = CountVectorizer(max_features=5000,stop_words='english') ## here max_features = 5000 means most frequent 5000 words in tags
vector = cv.fit_transform(dataframe1['tags']).toarray() # Convert the 'tags' column into a numerical format using CountVectorizer and store it in 'vector'.
print(vector) # Print the dense array representation of 'tags'.
print(vector.shape) # Display the shape of the array: (number of rows, number of unique words).

## Cosine similarity is a formula used to measure how similar the movies are based on their similarities of different properties. It shows the cosine of the angle of two vectors projected in a multidimensional space. The cosine similarity is very beneficial since it helps in finding similar objects. Content-based filtering is a recommendation strategy that suggests items similar to those a user has previously liked. It calculates similarity (often using cosine similarity) between the user’s preferences and item attributes, such as lead actors, directors, and genres

similarity = cosine_similarity(vector)
print(similarity)

# calculating the index for recommending the movies
# Function to recommend movies based on similarity.
# Finds the index of the input movie, calculates similarity scores, and prints the top 5 most similar movies.
def recommend(movie):
    index = dataframe1[dataframe1['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x : x[1]) # enumerate(similarity[index]): Pairs each similarity score with its corresponding movie index.
    for i in distances[1:6]: # Iterates through the top 5 most similar movies (excluding the input movie itself, by skipping distances[0]).
        print(dataframe1.iloc[i[0]].title) # Retrieves the title of each similar movie from dataframe1 (using .iloc) and prints it.
recommend('Spider-Man')
recommend("Pirates of the Caribbean: At World's End")

## Necessary for deploying it to web app
import pickle
pickle.dump(dataframe1,open('artifacts/movie_list.pkl','wb'))
pickle.dump(similarity,open('artifacts/similarity.pkl','wb'))