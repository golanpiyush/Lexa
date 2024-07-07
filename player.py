import time
import os
import psutil
import shutil
from spinner import Spinner
import threading
import platform
import subprocess
def get_temp_directory():
    ram_disk_paths = ['R:\\PowderPlayerTemp', 'S:\\PowderPlayerTemp', 'T:\\PowderPlayerTemp']
    for path in ram_disk_paths:
        if os.path.exists(os.path.dirname(path)):
            return path
    
    # Fallback to a directory in the user's temp folder
    return os.path.join(os.environ['TEMP'], 'PowderPlayerTemp')

def clean_temp_directory(temp_dir):
    try:
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
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