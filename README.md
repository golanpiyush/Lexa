# Lexa

## Movie on CLI – Stream Torrents with Ease

**Lexa** is a command-line based torrent streaming client that allows you to watch movies, web series, and more — directly from magnet or torrent links. Designed with accessibility in mind, it works seamlessly across all countries thanks to its **built-in proxy** support.

### Features

- **Torrent-based streaming** with real-time playback
- **Built-in proxy** for global access (no VPN required)
- **PowderPlayer integration** for smooth and flexible media playback
- **Subtitle support** in multiple languages
- Lightweight and easy to use from your terminal

### How It Works

Lexa uses available seeders to stream torrent files. The more seeds, the better the streaming experience. If a torrent has low seeders, streaming may be slow or delayed.

### Requirements

- [PowderPlayer](https://github.com/jaruba/PowderPlayer)
- Node.js (if applicable)
- Python 3.x (if you use a Python wrapper)
- Internet connection with reasonable speed

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/lexa.git
cd lexa

# Install dependencies (if any)
npm install # or pip install -r requirements.txt


#Usage

# Basic usage with a magnet link
lexa "magnet:?xt=urn:btih:..."

# You can also use .torrent files
lexa path/to/file.torrent


Subtitles will be auto-loaded when available and can be selected in different languages during playback via PowderPlayer.

Disclaimer

Lexa is intended for educational and personal use only. Please ensure you have the legal right to access any content you stream using this tool. The developer is not responsible for any misuse.


---

Contributing

Feel free to fork the project, submit issues, or open pull requests to contribute!

License

MIT License

---

Let me know if you want to include screenshots, badges, or a project roadmap.