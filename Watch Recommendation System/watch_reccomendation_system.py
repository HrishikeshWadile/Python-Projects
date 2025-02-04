# API_KEY = "7b846efcca6bb00569864d3950b1ed54"
# API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3Yjg0NmVmY2NhNmJiMDA1Njk4NjRkMzk1MGIxZWQ1NCIsIm5iZiI6MTcyNDM5NDMwOS4wMDUwOTUsInN1YiI6IjY2YzgyOGJlNjEzMTEyZmQ1YmIyZmUzZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4SPjNzN7Ezt9BiZ2UBN24_Gx6PodDkVgERgUPFnUkTA"
import requests
import pycountry
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings


def convert_language_code_to_name(language_code):
    try:
        # Lookup the language using the language code
        language = pycountry.languages.get(alpha_2=language_code)
        if language:
            return language.name
        else:
            return language_code
    except KeyError:
        return "Invalid language code"


# Suppress specific FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# TMDb API key
API_KEY = '7b846efcca6bb00569864d3950b1ed54'
BASE_URL = 'https://api.themoviedb.org/3'


def convert_language_code_to_name_func(language_code):
    try:
        # Lookup the language using the language code
        language = pycountry.languages.get(alpha_2=language_code)
        if language:
            return language.name
        else:
            return language_code
    except KeyError:
        return "Invalid language code"


def search_movie(query):
    search_url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1,
        # 'include_adult': False  # Avoid adult content in results
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return None


def get_similar_movies(movie_id):
    similar_url = f"{BASE_URL}/movie/{movie_id}/similar"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(similar_url, params=params)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return None


# Main function
def main():
    # Get user input for the movie search
    user_input = input("Enter the name of a movie: ")

    # Search for the movie using the user's input
    search_results = search_movie(user_input)

    if not search_results:
        print("No movies found. Please try again.")
        return

    # Use difflib to find the closest match to the user's input
    movie_titles = [movie['title'] for movie in search_results]
    best_match = difflib.get_close_matches(user_input, movie_titles, n=1, cutoff=0.5)

    if not best_match:
        print("No close matches found. Please try again.")
        return

    # Ask the user for confirmation
    print(f"Did you mean '{best_match[0]}'? (yes/no)")
    confirmation = input().lower()

    if confirmation != 'yes':
        print("Operation cancelled.")
        return

    # Find the selected movie in the search results
    selected_movie = next(movie for movie in search_results if movie['title'] == best_match[0])

    # Get similar movies based on the selected movie's ID
    similar_movies = get_similar_movies(selected_movie['id'])

    if similar_movies:
        print("\nSimilar Movies:")
        for movie in similar_movies:
            print(f"\nTitle: {movie['title']}")
            language_code = movie['original_language']
            full_language_name = convert_language_code_to_name_func(language_code)
            print(f"Original Language: {full_language_name}")
            print(f"Original Title: {movie['original_title']}")
            print(f"Adult: {movie['adult']}")
            print(f"Description: {movie['overview']}")
            print(f"Release Date: {movie['release_date']}")
    else:
        print("No similar movies found.")


# Run the main function
if __name__ == "__main__":
    main()
