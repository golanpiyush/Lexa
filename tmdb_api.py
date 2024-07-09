import requests

def find_movie_trailers_tmdb(movie_name, api_key):
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_params = {
        'api_key': api_key,
        'query': movie_name
    }
    
    search_response = requests.get(search_url, params=search_params)
    search_json = search_response.json()

    if not search_json['results']:
        return []

    movie_id = search_json['results'][0]['id']

    trailers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    trailers_params = {
        'api_key': api_key
    }
    
    trailers_response = requests.get(trailers_url, params=trailers_params)
    trailers_json = trailers_response.json()

    trailers = []
    for item in trailers_json.get('results', []):
        if item['type'] == 'Trailer' and item['site'] == 'YouTube':
            trailer_data = {
                'name': item['name'],
                'key': item['key'],
                'url': f"https://www.youtube.com/watch?v={item['key']}"
            }
            trailers.append(trailer_data)
    
    return trailers
