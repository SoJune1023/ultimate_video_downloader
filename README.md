# Readme

Just simple video cli downloader.  
Made by claude, not me.

## Packageing

### Step 1. Install dependencies

- Window : `winget install ffmpeg`  
- macOS : `brew install ffmpeg`  
- Ubuntu/Debian : `sudo apt install ffmpeg`

#### Install UV
You should install uv even you are not using macOS
- macOS : `brew install uv`

```bash
pip install -e . 
```

### Step 2. Run pyinstaller  

```bash
uv run pyinstaller \  --name ultimate-video-downloader \
  --onefile \
  --paths src \
  --collect-all yt_dlp \
  --add-data certifi \
  src/ultimate_video_downloader/main.py
```

### Step 3. Run file

<download_path>/dist/ultimate_downloader
