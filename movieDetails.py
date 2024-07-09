import requests
tmdb_api_key = 'api-key'

# ex: movieName = 'man of steel'


def fetch_movie_details(movieName):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': tmdb_api_key,
        'query': movieName
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        if results:
            movie = results[0]
            title = movie.get('title', 'Unknown')
            synopsis = movie.get('overview', 'No synopsis available.')
            release_date = movie.get('release_date', 'Unknown')
            # Format the synopsis to include new lines
            formatted_synopsis = synopsis.replace('. ', '.\n\t')
            release_year = release_date.split('-')[0] if release_date != 'Unknown' else 'Unknown'
            return {
                'title': title,
                'synopsis': formatted_synopsis,
                'release_year': release_year
            }
        else:
            return None
    except requests.exceptions.ConnectionError as e:
        print("API response error!")
