import requests
from colorama import Fore
import re
# init(autoreset=True)
def fetchMovie(site, query, categories=None, season_filter=None, episode_filter=None):
    api_url = f"https://torrent-api-py-nx0x.onrender.com/api/v1/search?site={site}&query={query}&limit=10&page=1"

    if categories:
        api_url += f"&categories={','.join(categories)}"

    quality_keywords = ['BRip', 'BDRip', 'Blu-Ray', 'BluRay', 'WEBRip', 'WEBDL', 'WEB DL', 'WEB-DL', 'HDRip']
    low_quality_keywords = ['telesync', 'hdts', 'ts', 'cam-rip', 'hdcam', 'cam','TELE-SYNC', 'HDTS','TELESYNC', 'HD-TS', 'TS', 'CAM-RIP', 'HDCAM', 'CAM']

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        if response.status_code == 200:
            print("Connection Successful: 200")
            torrents = response.json()
            quality_torrents = []
            low_quality_torrents = []

            if 'data' in torrents and torrents['data']:
                for torrent_info in torrents['data']:
                    torrent_name = torrent_info.get('name', 'Unknown')

                    # Check if all query words are in the torrent name
                    query_words = query.lower().split()
                    if not all(word.lower() in torrent_name.lower() for word in query_words):
                        continue

                    if season_filter and season_filter.lower() not in torrent_name.lower():
                        continue
                    if episode_filter and episode_filter.lower() not in torrent_name.lower():
                        continue

                    magnet_url = torrent_info.get('magnet')
                    seeders = int(torrent_info.get('seeders', '0'))
                    leechers = int(torrent_info.get('leechers', '0'))
                    total_size_gb = parse_size(torrent_info.get('size', '0'))

                    torrent_data = {
                        'name': torrent_name,
                        'magnet': magnet_url,
                        'seeders': seeders,
                        'leechers': leechers,
                        'size': total_size_gb
                    }

                    if any(qual.lower() in torrent_name.lower() for qual in quality_keywords):
                        quality_torrents.append(torrent_data)
                    elif any(low_qual.lower() in torrent_name.lower() for low_qual in low_quality_keywords):
                        low_quality_torrents.append(torrent_data)

            quality_torrents.sort(key=lambda x: x['seeders'], reverse=True)
            low_quality_torrents.sort(key=lambda x: x['seeders'], reverse=True)

            if quality_torrents:
                if 's' in query.lower() and re.search(r's\d+', query, re.IGNORECASE):
                    print(Fore.WHITE + f"Found the following quality seasons for {query[:-4].strip()}:\n")
                else:
                    print(Fore.WHITE + "Found the following quality movies:\n")
                for i, torrent in enumerate(quality_torrents[:3], 1):
                    size_mb = torrent['size']
                    if size_mb >= 1024:
                        size_str = f"{size_mb / 1024:.2f} GB"
                    else:
                        size_str = f"{size_mb:.2f} MB"
                    print(f"{i}. {torrent['name']} - Seeders: {torrent['seeders']}, Size: {size_str}")
                
                return "high_quality", quality_torrents[0]['magnet'], quality_torrents
            elif low_quality_torrents:
                if 's' in query.lower() and re.search(r's\d+', query, re.IGNORECASE):
                    print(Fore.RED + f"Only lower quality seasons are available for {query[:-4].strip()}:\n")
                else:
                    print(Fore.RED + "Only lower quality movies are available:\n")
                for i, torrent in enumerate(low_quality_torrents[:3], 1):
                    size_mb = torrent['size']
                    if size_mb >= 1024:
                        size_str = f"{size_mb / 1024:.2f} GB"
                    else:
                        size_str = f"{size_mb:.2f} MB"
                    print(f"{i}. {torrent['name']} - Seeders: {torrent['seeders']}, Size: {size_str}")
                
                return "low_quality", low_quality_torrents[0]['magnet'], low_quality_torrents
            else:
                print(f"Could not find any torrents for: {query}")
                return "no_torrents", None, []

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"Error 403: Access Forbidden. The movie '{query}' might not be available or the server is blocking the request.")
        else:
            print(f"HTTP Error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    return "error", None, []

def parse_size(size_str):
    size_str = size_str.replace('MiB', 'MB').replace('GiB', 'GB').replace('KiB', 'KB')
    size, unit = size_str.split()
    size = float(size)
    if unit.lower() == 'kb':
        size /= 1024
    elif unit.lower() == 'mb':
        pass
    elif unit.lower() == 'gb':
        size *= 1024
    return size
