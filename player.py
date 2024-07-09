import time
import os
import psutil
import shutil
from spinner import Spinner
import threading
import platform
import requests
import subprocess
import webbrowser
from urllib.parse import urlencode


def get_temp_directory():
    ram_disk_paths = ['R:\\PowderPlayerTemp', 'S:\\PowderPlayerTemp', 'T:\\PowderPlayerTemp']
    for path in ram_disk_paths:
        if os.path.exists(os.path.dirname(path)):
            return path
    
    # Fallback to a directory in the user's temp folder
    return os.path.join(os.environ['TEMP'], 'PowderPlayerTemp')

api_key = '8647e66c3eb65f11c331cdfd8ca059b3'
def is_powder_player_running():
    return any("powder.exe" in p.name().lower() for p in psutil.process_iter(['name']))


def play_trailer_with_powderplayer(movie_name, api_key, autoplay=True):
    try:
        # Search for the movie on TMDB
        search_url = "https://api.themoviedb.org/3/search/movie"
        search_params = {
            'api_key': api_key,
            'query': movie_name
        }
        
        search_response = requests.get(search_url, params=search_params)
        search_json = search_response.json()

        # Check if there are results for the search query
        if not search_json['results']:
            print(f"No results found for '{movie_name}' on TMDB.")
            return None

        # Get the movie ID of the first result
        movie_id = search_json['results'][0]['id']

        # Fetch trailers for the movie
        trailers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
        trailers_params = {
            'api_key': api_key
        }
        
        trailers_response = requests.get(trailers_url, params=trailers_params)
        trailers_json = trailers_response.json()

        # Extract YouTube trailers
        trailers = []
        for item in trailers_json.get('results', []):
            if item['type'] == 'Trailer' and item['site'] == 'YouTube':
                trailer_data = {
                    'name': item['name'],
                    'key': item['key']
                }
                trailers.append(trailer_data)

        # If trailers are found, play the first trailer with autoplay option
        if trailers:
            print(f"Found {len(trailers)} trailers for '{movie_name}':")
            trailer = trailers[0]
            print(f"Playing trailer '{trailer['name']}' {'with autoplay' if autoplay else 'without autoplay'}...")

            # Construct YouTube URL with parameters
            base_url = "https://www.youtube.com/watch"
            params = {
                'v': trailer['key'],
                'autoplay': 1 if autoplay else 0
            }
            full_url = f"{base_url}?{urlencode(params)}"

            # Open the YouTube URL in the default web browser
            webbrowser.open(full_url)

            return True

        else:
            print(f"No trailers found for '{movie_name}' on TMDB.")
            return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def is_vlc_installed():
    # Check if VLC is installed by attempting to run 'vlc' command and checking return code
    try:
        subprocess.run(['vlc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        # Check if VLC executable exists in common installation directory
        vlc_exe_path = [
        r'C:\Program Files\VideoLAN\VLC\vlc.exe',
        r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
    ]
        if os.path.isfile(vlc_exe_path):
            return True
        else:
            return False
    except Exception:
        return False
def play_with_vlc(url):
    # Launch VLC player with the given URL
    subprocess.Popen(['vlc', '--fullscreen', url])



def clean_temp_directory(temp_dir):
    try:
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.unlink(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
        print(f"Temporary files cleaned from: {temp_dir}")
    except Exception as e:
        print(f"Error cleaning temporary files: {e}")


def execute_powder_player(command):
    try:
        # Start the Powder Player process in the background
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("Powder Player started in background.")
        return process
    except Exception as e:
        print(f"Error starting Powder Player: {e}")
        return None

def bring_powder_player_to_foreground(process):
    try:
        # Placeholder for bringing Powder Player to foreground
        time.sleep(10)  # Simulate bringing to foreground after 20 seconds
        # print("Bringing Powder Player to foreground...")
        
        # Actual implementation to bring the window to foreground based on platform
        if process and platform.system() == 'Windows':
            # Windows specific code using ctypes
            import ctypes
            ctypes.windll.user32.SwitchToThisWindow(process.pid, True)
        elif process and platform.system() == 'Linux':
            # Linux specific code using wmctrl
            subprocess.run(['wmctrl', '-ia', f'{process.pid}'])
        else:
            print("Unsupported platform for foreground handling.")
        
        # For demonstration purposes, print a message indicating foreground operation
        # print("Powder Player is now in the foreground.")
    except Exception as e:
        print(f"Error bringing Powder Player to foreground: {e}")

def stream_movie_with_powderplayer(stripped_magnet_link):
    powderplayer_path = r'helpers\Powder Player\powder.exe'  # Adjust the path accordingly
    
    # Get the temporary directory
    temp_dir = get_temp_directory()
    
    # Ensure the temporary directory exists
    os.makedirs(temp_dir, exist_ok=True)
    
    # Set environment variable to tell Powder Player to use this directory for temporary files
    os.environ['POWDER_PLAYER_TEMP'] = temp_dir
    
    # Add the '--play' argument to start playing immediately
    command = [powderplayer_path, '--play', stripped_magnet_link]
    
    # Check if Powder Player is already running
    powder_running = any("powder.exe" in p.name().lower() for p in psutil.process_iter())
   
    if powder_running:
        print("Powder Player is already running. Please close it before starting a new stream.")
        return
    
    try:
        # Show spinner with "Searching..." text for 20 seconds
        with Spinner("Searching..."):
            # Start the Powder Player process in the background using threading
            thread = threading.Thread(target=execute_powder_player, args=(command,))
            thread.start()
            time.sleep(10)  # Simulate 10 seconds delay to allow startup
            
            # Get the running Powder Player process
            process = None
            for p in psutil.process_iter():
                if 'powder.exe' in p.name().lower():
                    process = p
                    break
            
            # Bring Powder Player to foreground after initial delay
            bring_powder_player_to_foreground(process)
        
        print(f"Streaming started with Powder Player for {stripped_magnet_link}.")
        
        # Wait for the user to interrupt (Ctrl+C)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStreaming process interrupted by user.")
            # Clean up temporary files
            clean_temp_directory(temp_dir)
    except OSError as e:
        print(f"Error streaming with Powder Player: {e}")
    except Exception as e:
        print(f"Unexpected error streaming with Powder Player: {e}")

# Example usage:
# magnet_link = "your_magnet_link_here"
# stream_movie_with_powderplayer(magnet_link)