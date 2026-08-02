import ssl
import certifi

from pathlib import Path

from src.downloader import download_url

DEFAULT_OUTPUT_DIR = "~/Downloads"

def print_banner() -> None:
    print("=" * 50)
    print("   유튜브 / 인스타그램 릴스 다운로더")
    print("=" * 50)
    print("URL을 붙여넣고 엔터")
    print("명령어:  q 종료  |  o 저장위치변경  |  a 오디오모드전환")

def prompt_line(output_dir: str, audio_mode: bool) -> str:
    mode_label = "🎵 오디오만" if audio_mode else "🎬 영상"
    print(f"\n저장 위치: {Path(output_dir).expanduser()}   |   모드: {mode_label}")
    return input("▶ ").strip()

def main() -> None:
    ssl._create_default_https_context = lambda: ssl.create_default_context(
        cafile=certifi.where()
    )

    print_banner()
    output_dir = DEFAULT_OUTPUT_DIR
    audio_mode = False

    while True:
        try:
            raw = prompt_line(output_dir, audio_mode)
        except (EOFError, KeyboardInterrupt):
            print("\n종료함.")
            break

        if not raw:
            continue

        cmd = raw.lower()

        if cmd in ("q", "quit", "exit"):
            print("종료함.")
            break

        if cmd == "o":
            new_dir = input("  새 저장 위치 (엔터: 취소): ").strip()
            if new_dir:
                output_dir = new_dir
                print(f"  → 저장 위치 변경: {Path(output_dir).expanduser()}")
            continue

        if cmd == "a":
            audio_mode = not audio_mode
            print(f"  → {'오디오만(mp3) 모드' if audio_mode else '영상(mp4) 모드'}로 전환")
            continue

        urls = [tok for tok in raw.split() if tok.startswith("http")]
        if not urls:
            print("  ⚠️ 올바른 URL이 아님 (http로 시작해야 함)")
            continue

        for url in urls:
            download_url(url, output_dir, audio_mode)

        print(f"\n📁 저장 위치: {Path(output_dir).expanduser()}")

if __name__ == "__main__":
    main()
