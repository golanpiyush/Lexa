import re
import psutil
import time
import threading
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from player import stream_movie_with_powderplayer, play_trailer_with_powderplayer 
from utils import get_current_day
from input_cache import InputCache
from torrent import fetch_torrent, parse_size
from movieDetails import fetch_movie_details


name = "Lexa: "
api_key = 'api-key'
site = "piratebay"
cache_file = 'input_cache.pkl'

# Initialize InputCache
input_cache = InputCache(cache_file=cache_file)

powder_player_running = False

def is_powder_player_running():
    return any("powder.exe" in p.name().lower() for p in psutil.process_iter(['name']))

def stream_torrent(magnet_url, query, lock):
    global powder_player_running
    
    if magnet_url:
        stripped_magnet_link = re.search(r"magnet:\?xt=urn:btih:[a-zA-Z0-9]+", magnet_url).group(0)

        try:
            with lock:
                if powder_player_running or is_powder_player_running():
                    print("Powder Player is already running. Please close it before starting a new stream.")
                    return

                powder_player_running = True
                process = stream_movie_with_powderplayer(stripped_magnet_link)

                if process:
                    print("Powder Player is now running. Press Ctrl+C to stop streaming and return to search.")
                    
                    try:
                        while is_powder_player_running():
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
        print(f"{name}Could not find a suitable torrent to stream.")

# Initialize threading lock
streaming_lock = threading.Lock()

def handle_special_commands(query):
    if query.endswith('--tr'):
        movie_name = query[:-4].strip()  # Remove '--tr' from query
        play_trailer_with_powderplayer(movie_name, api_key)
        return True
    elif query.endswith('-sy'):
        movie_name = query[:-4].strip()
        movie_details = fetch_movie_details(movie_name)
        if movie_details:
            print(f"\nTitle: {movie_details['title']} ({movie_details['release_year']})")
            print(f"Synopsis: {movie_details['synopsis']}\n")
            # print(f"Release Date: {movie_details['release_date']}")
        else:
            print("No details found for the specified movie.")
        return False  
    elif query.lower() in ['-e', '-q']:
        
        print(f"{name}Goodbye...")
        time.sleep(4)
        return True
    
    return False


if __name__ == "__main__":
    print(f"{name}Hey! It's a Beautiful {get_current_day()}")
    time.sleep(1)
    print(f"\n{name}What movie would you like to watch?")
   
    while True:
        suggestions = input_cache.get_suggestions()
        special_commands = ['-sy', '--tr', '-h', '-q','-e']

        completer = WordCompleter(special_commands + suggestions, ignore_case=True)

        query = prompt(f"{name}Enter search query (or type '-e' or '-q' to quit): ", completer=completer).strip()
        
        if handle_special_commands(query):
            if query.lower() in ['-e', '-q']:
                break  
        elif '-sy' in query:
                continue
        elif query == '''-h ''':
            print(f"{name}To Play Movies use the (MovieName)")
            print(f"{name} Use '-sy' : Synopsis, '--tr' : Tralier")
            continue
            # return False
        elif query == '':
            print(f'{name}No input found')
            continue
        
        print(f"{name}Searching for: {query}")
        quality, magnet_url, torrents = fetch_torrent(site, query)
        
        if quality == "high_quality" or quality == "low_quality":
            if quality == "low_quality":
                choice = input(f"{name}Only lower quality torrents are available. Do you want to proceed? (y/n): ").strip().lower()
                if choice != 'y':
                    print(f"{name}Torrent streaming cancelled.")
                    continue

            choice = input(f"{name}Enter the number of the torrent you want to stream (or 'n' to cancel): ").strip().lower()
            if choice == 'n':
                print(f"{name}Torrent streaming cancelled.")
            elif choice.isdigit() and 1 <= int(choice) <= len(torrents):
                selected_torrent = torrents[int(choice) - 1]
                stream_torrent(selected_torrent['magnet'], query, streaming_lock)
                input_cache.add(query)
                break
            else:
                print(f"{name}Invalid choice. Torrent streaming cancelled.")
        elif quality == "no_torrents":
            print(f"{name}Could not find any torrents for: {query}")
        else:
            print(f"{name}An error occurred while searching for torrents.")
        
        print(f"\n{name}What else would you like to watch?")

    # After exiting the loop, save the cache to file
    input_cache.add(query, is_history=True)
    input_cache.save_cache()
