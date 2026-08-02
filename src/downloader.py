import yt_dlp
import subprocess

from pathlib import Path
from yt_dlp.postprocessor.common import PostProcessor

def get_video_codec(path: Path) -> str | None:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=codec_name",
                "-of", "csv=p=0",
                str(path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        return result.stdout.strip() or None
    except FileNotFoundError:
        return None

def ensure_quicktime_compatible(path: Path) -> None:
    codec = get_video_codec(path)
    if codec is None:
        return
    if codec == "h264":
        return

    print(f"  🔄 QuickTime 비호환 코덱({codec}) 감지, h264로 재인코딩 중...")
    tmp = path.with_name(path.stem + ".qtfix.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(tmp),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and tmp.exists():
        tmp.replace(path)
        print("  ✅ 재인코딩 완료, QuickTime에서 재생 가능")
    else:
        tmp.unlink(missing_ok=True)
        print(f"  ⚠️ 재인코딩 실패, 원본 유지 (VLC로는 재생 가능): {result.stderr[-200:]}")

class QuickTimeFixPP(PostProcessor):
    def run(self, info):
        filepath = info.get("filepath")
        if filepath:
            ensure_quicktime_compatible(Path(filepath))
        return [], info

def build_format(audio_only: bool) -> str:
    if audio_only:
        return "bestaudio/best"

    return (
        "bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]"
        "/best[vcodec^=avc1]"
        "/bestvideo+bestaudio"
        "/best"
    )

def progress_hook(d) -> None:
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r  ⬇ {pct}  {speed}  ETA {eta}   ", end="", flush=True)
    elif d["status"] == "finished":
        print("\r  ✅ 다운로드 완료, 후처리 중...                    ")

def make_opts(output_dir: str, audio_only: bool) -> dict:
    outdir = Path(output_dir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    opts = {
        "format": build_format(audio_only),
        "outtmpl": str(outdir / "%(uploader)s - %(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
        "noprogress": False,
        "concurrent_fragment_downloads": 4,
    }

    if audio_only:
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
        opts.pop("merge_output_format", None)

    return opts

def download_url(url: str, output_dir: str, audio_only: bool) -> None:
    print(f"\n🔗 {url}")
    try:
        opts = make_opts(output_dir, audio_only)
        with yt_dlp.YoutubeDL(opts) as ydl:
            if not audio_only:
                ydl.add_post_processor(QuickTimeFixPP(), when="after_move")
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"  ❌ 실패: {e}")
