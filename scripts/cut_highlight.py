import json
import os
import subprocess
import argparse

def cut_highlights(video_path, highlights_path, output_dir):
    with open(highlights_path, "r", encoding="utf-8") as f:
        highlights = json.load(f)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, item in enumerate(highlights, start=1):
        start = item["start"]
        end = item["end"]
        output_file = os.path.join(output_dir, f"highlight_{idx:02}.mp4")

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", start,
            "-to", end,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "experimental",
            output_file
        ]

        print(f"✂️  하이라이트 {idx} 추출 중: {start} ~ {end} → {output_file}")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n✅ 총 {len(highlights)}개의 하이라이트가 저장되었습니다 → {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="원본 영상 경로 (.mp4)")
    parser.add_argument("--highlights", default="highlights.json", help="하이라이트 JSON 경로")
    parser.add_argument("--output", default="clips", help="저장할 클립 폴더명")
    args = parser.parse_args()

    cut_highlights(args.video, args.highlights, args.output)
