# Readme

Just simple video cli downloader.  
Made by claude, not me.

## Packageing

### Step 1. Install dependencies

- Window : `winget install ffmpeg`  
- macOS : `brew install ffmpeg`  
- Ubuntu/Debian : `sudo apt install ffmpeg`  

```bash
pip install -e . 
```

### Step 2. Run pyinstaller  

```bash
python -m PyInstaller --onefile \
  --name ultimate_downloader \
  --collect-all yt_dlp \
  --collect-all certifi \
  src/__main__.py
```

### Step 3. Run file

<download_path>/dist/ultimate_downloader
