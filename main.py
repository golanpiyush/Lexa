import re
import requests
from player import stream_movie_with_powderplayer 
from day import get_current_day
import threading
import psutil
import time


def parse_size(size_str):
    size_str = size_str.replace('\xa0', '')  # Remove non-breaking space
    size_str = size_str.strip()  # Remove any leading/trailing whitespace

    try:
        if 'GiB' in size_str:
            return float(size_str.replace('GiB', '').strip())  # Remove 'GiB' and convert to float
        elif 'MiB' in size_str:
            return float(size_str.replace('MiB', '').strip()) / 1024  # Convert MiB to GiB
        elif 'KiB' in size_str:
            return float(size_str.replace('KiB', '').strip()) / (1024 * 1024)  # Convert KiB to GiB
        else:
            return 0
    except ValueError as e:
        print(f"Error converting size string '{size_str}' to float: {e}")
        return 0

import time
import sys

def fetch_torrent(site, query):
    while True:
        api_url = f"https://torrent-api-py-nx0x.onrender.com/api/v1/search?site={site}&query={query}&limit=1&page=1"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                print("Connection Successful: 200")
                torrents = response.json()

                if 'data' in torrents and torrents['data']:
                    torrent_info = torrents['data'][0]  # Get the first result
                    magnet_url = torrent_info.get('magnet')
                    seeders = int(torrent_info.get('seeders', '0'))  # Convert seeders to int
                    total_size_gb = parse_size(torrent_info.get('size', '0'))

                    if seeders >= 20 and total_size_gb < 6:
                        return magnet_url, torrent_info
                    else:
                        print(f"The torrent '{query}' does not meet the criteria (>= 20 seeders and < 6 GB).")
                        print(f"Seeders: {seeders}, Size: {total_size_gb:.2f} GB")
                        while True:
                            print("Do you want to continue with this torrent? (y/n): ", end='', flush=True)
                            time.sleep(0.1)  # Small delay to ensure prompt is displayed
                            sys.stdin.flush()  # Flush the input buffer
                            choice = sys.stdin.readline().strip().lower()
                            if choice == 'y':
                                return magnet_url, torrent_info
                            elif choice == 'n':
                                break
                            elif choice == '':
                                print("No input received. Please enter 'y' or 'n'.")
                            else:
                                print("Invalid input. Please enter 'y' or 'n'.")
                        
                        print("Enter a new search query (or 'exit' to quit): ", end='', flush=True)
                        time.sleep(0.1)  # Small delay to ensure prompt is displayed
                        sys.stdin.flush()  # Flush the input buffer
                        query = sys.stdin.readline().strip()
                        if query.lower() == 'exit':
                            print("Exiting...")
                            exit(0)
                else:
                    print(f"No torrents found for '{query}' on {site}.")
                    print("Enter a new search query (or 'exit' to quit): ", end='', flush=True)
                    time.sleep(0.1)  # Small delay to ensure prompt is displayed
                    sys.stdin.flush()  # Flush the input buffer
                    query = sys.stdin.readline().strip()
                    if query.lower() == 'exit':
                        print("Exiting...")
                        exit(0)
            else:
                print(f"Error fetching data: {response.status_code}")
                print("Enter a new search query (or 'exit' to quit): ", end='', flush=True)
                time.sleep(0.1)  # Small delay to ensure prompt is displayed
                sys.stdin.flush()  # Flush the input buffer
                query = sys.stdin.readline().strip()
                if query.lower() == 'exit':
                    print("Exiting...")
                    exit(0)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            print("Enter a new search query (or 'exit' to quit): ", end='', flush=True)
            time.sleep(0.1)  # Small delay to ensure prompt is displayed
            sys.stdin.flush()  # Flush the input buffer
            query = sys.stdin.readline().strip()
            if query.lower() == 'exit':
                print("Exiting...")
                exit(0)

    return None, None


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

                print(f"Streaming '{query}' using Powder Player...\n")
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
        print("Could not find a suitable torrent to stream.")

# Initialize threading lock
streaming_lock = threading.Lock()

# Example usage:
if __name__ == "__main__":
    print(f"Hey! It's a Beautiful {get_current_day()}")
    time.sleep(1)
    print("\nWhat movie would you like to watch?")
    site = "piratebay"
    
    while True:
        query = input("Enter search query: ").strip()
        if query == '-h':
            print("To Play Movies use the (MovieName)")
            continue
        magnet_url, torrent_info = fetch_torrent(site, query)
        if magnet_url:
            stream_torrent(magnet_url, query, streaming_lock)
            break
        else:
            print("Could not find a suitable torrent.")
