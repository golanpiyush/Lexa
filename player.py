import time
import os
import psutil
import shutil
import threading
import platform
import subprocess
# from urllib.parse import urlencode
from spinner import Spinner
import traceback
import yt_dlp as ydl



# Constants and Configuration
name1 = 'Lexa: '
powderplayer_path = r'helpers\Powder Player\powder.exe'
mpv_path = r'helpers\mpv.exe'

def get_temp_directory():
    ram_disk_paths = ['R:\\PowderPlayerTemp', 'S:\\PowderPlayerTemp', 'T:\\PowderPlayerTemp']
    for path in ram_disk_paths:
        if os.path.exists(os.path.dirname(path)):
            return path
    
    # Fallback to a directory in the user's temp folder
    return os.path.join(os.environ['TEMP'], 'PowderPlayerTemp')



def playTralier(movie_name):
    try:

        ydl_opts = {
            'quiet': True,
            'format': 'best[ext=mp4]',
            'extract_flat': True,
            'default_search': 'ytsearch',
            'noplaylist': True
        }

        with ydl.YoutubeDL(ydl_opts) as ydl_obj:
            result = ydl_obj.extract_info(f'ytsearch:{movie_name} official trailer', download=False)

            if 'entries' in result and result['entries']:
                first_result = result['entries'][0]
                youtube_url = first_result['url']
                mpv_command = [mpv_path, youtube_url]
                subprocess.run(mpv_command, check=True)

                return True
            else:
                print(f"No official trailer found for '{movie_name}' on YouTube.")
                return False

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

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



def bring_powder_player_to_foreground(process):
    try:
        # Placeholder for bringing Powder Player to foreground
        time.sleep(10)  # Simulate bringing to foreground after 10 seconds
        
        # Actual implementation to bring the window to foreground based on platform
        if process and platform.system() == 'Windows':
            import ctypes
            ctypes.windll.user32.SwitchToThisWindow(process.pid, True)
        elif process and platform.system() == 'Linux':
            subprocess.run(['wmctrl', '-ia', f'{process.pid}'])
        else:
            print("Unsupported platform for foreground handling.")
    except Exception as e:
        print(f"Error bringing Powder Player to foreground: {e}")


def playMusic(song_name):
    youtube_url = None
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'default_search': 'ytsearch',
            'extract_flat': True,
        }
        with ydl.YoutubeDL(ydl_opts) as ydl_obj:
            result = ydl_obj.extract_info(f'ytsearch:{song_name} official song with lyrics', download=False)
            if 'entries' in result:
                youtube_url = result['entries'][0]['url']
            else:
                youtube_url = result['url']

        if youtube_url:
            with Spinner(f"Playing {youtube_url} with mpv..."):
            # Play the video as audio using mpv
                mpv_command = [
                    mpv_path, '--quiet', '--ontop=no',
                    '--af=equalizer=f=32:width_type=h:width=50:g=10,equalizer=f=64:width_type=h:width=50:g=10,equalizer=f=125:width_type=h:width=50:g=5',
                    youtube_url
                ]
                subprocess.run(mpv_command, check=True)  # Ensure mpv starts correctly

    except ydl.utils.DownloadError as e:
        print(f"Error fetching video URL: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error playing video with mpv: {e}")
        print(traceback.format_exc())  # Print full traceback for better diagnostics
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(traceback.format_exc())


# executer

def execute_powder_player(command):
    try:
        # Start the Powder Player process in the background
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error starting Powder Player: {e}")
        return None


# function which streams movies


def movieStreamer(stripped_magnet_link):
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
            print(f"\n{name1}Movies may take from a few seconds to a few minutes to process depending on our fellow seeders.")
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


