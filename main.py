import re
import psutil
import time
import threading
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from player import movieStreamer, playTralier, playMusic
from utils import currentDay, ClearScreen
from input_cache import InputCache
from movies import fetchMovie
from movieDetails import fetchmovieDetails


devName = 'Piyush Golan'
name1 = 'Lexa: '
site = "piratebay"

api_key = '8647e66c3eb65f11c331cdfd8ca059b3'
# Initialize InputCache
input_cache = InputCache(cache_file='input_cache.pkl')

powder_player_running = False

def powderPlayerStaus():
    return any("powder.exe" in p.name().lower() for p in psutil.process_iter(['name']))

def streamMovie(magnet_url, query, lock):
    global powder_player_running
    
    if magnet_url:
        stripped_magnet_link = re.search(r"magnet:\?xt=urn:btih:[a-zA-Z0-9]+", magnet_url).group(0)

        try:
            with lock:
                if powder_player_running or powderPlayerStaus():
                    print("Powder Player is already running. Please close it before starting a new stream.")
                    return

                powder_player_running = True
                process = movieStreamer(stripped_magnet_link)

                if process:
                    print("Powder Player is now running. Press Ctrl+C to stop streaming and return to search.")
                    
                    try:
                        while powderPlayerStaus():
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\nStreaming interrupted by user.")
                    finally:
                        powder_player_running = False
                        if process.poll() is None:
                            process.terminate()
                else:
                    print("Failed to start Powder Player. Please try again.")
                    powder_player_running = False
        except Exception as e:
            print(f"Error streaming: {e}")
            powder_player_running = False
    else:
        print(f"{name1}Could not find a suitable torrent to stream.")

# Initialize threading lock
streaming_lock = threading.Lock()

def handle_special_commands(query):
    if query.endswith('-sng'):
        search_query = query[:-4].strip()  # Remove '-sng' and any trailing spaces
        playMusic(search_query) 
    elif '-clean' in query:
        print(f"{name1}Cleaning CLI...")
        time.sleep(2)
        ClearScreen()   
        print(f"{name1}Hey! It's a Beautiful {currentDay()}...")
    elif query.endswith('--tr'):
        movie_name = query[:-4].strip()  # Remove '--tr' from query
        playTralier(movie_name)
    elif query.endswith('-sy'):
        movie_name = query[:-4].strip()
        movie_details = fetchmovieDetails(movie_name)
        if movie_details:
            print(f"\nTitle: {movie_details['title']} ({movie_details['release_year']})")
            print(f"Synopsis: {movie_details['synopsis']}\n")
            # print(f"Release Date: {movie_details['release_date']}")
        else:
            print("No details found for the specified movie.")
    elif query.lower() in ['-e', '-q']:
        print(f"{name1}Goodbye...")
        time.sleep(3)
        return True
    
    return False

if __name__ == "__main__":
    print(f"{name1}Hey! It's a Beautiful {currentDay()}...")
    time.sleep(1)
    print(f"\n{name1}What movie would you like to watch?")
   
    while True:
        suggestions = input_cache.get_suggestions()
        special_commands = ['-sy', '--tr', '-h', '-q', '-e', '-sng']

        completer = WordCompleter(special_commands + suggestions, ignore_case=True)

        query = prompt(f"{name1}Enter search query (or type '-e' or '-q' to quit): ", completer=completer).strip()
        
        if handle_special_commands(query):
            if query.lower() in ['-e', '-q']:
                break
            
            else:
                continue
        elif query == '':
                print(f"{name1}No Input Found!")
                continue
        # Check if the query ends with any special commands
        elif query.endswith(('-sng', '--tr', '-sy', '-e', '-q')):
            continue
        elif '-clean' in query:
            continue
        elif '-abt' in query:
            print(f"{name1}Developer - {devName}")
            continue
        elif '-h' in query:
           print(f'''{name1} Usage: '[input] --tr' \n-sy: Gives the movie plots.\n --tr: Gives the specifed movie tralier.\n
                  -sng: Recognises any input as song.\n -e & -q: are used to exit.\n
                  Any input without the special characters will be considered as a movie name.''')
           continue
        print(f"{name1}Searching for: {query}")
        quality, magnet_url, torrents = fetchMovie(site, query)
        
        if quality == "high_quality" or quality == "low_quality":
            if quality == "low_quality":
                choice = input(f"{name1}Only lower quality torrents are available. Do you want to proceed? (y/n): ").strip().lower()
                if choice != 'y':
                    print(f"{name1}Torrent streaming cancelled.")
                    continue

            choice = input(f"{name1}Enter the number of the torrent you want to stream (or 'n' to cancel): ").strip().lower()
            if choice == 'n':
                print(f"{name1}Torrent streaming cancelled.")
            elif choice.isdigit() and 1 <= int(choice) <= len(torrents):
                selected_torrent = torrents[int(choice) - 1]
                streamMovie(selected_torrent['magnet'], query, streaming_lock)
                input_cache.add(query)
                break
            else:
                print(f"{name1}Invalid choice. Torrent streaming cancelled.")
        elif quality == "no_torrents":
            print(f"{name1}Could not find any torrents for: {query}")
        else:
            print(f"{name1}An error occurred while searching for torrents.")
        
        print(f"\n{name1}What else would you like to watch?")

    # After exiting the loop, save the cache to file
    input_cache.add(query, is_history=True)
    input_cache.save_cache()