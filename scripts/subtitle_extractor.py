import srt
import json
from datetime import timedelta
import os
import subprocess
import openai

# OpenAI API 키 설정
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# 입력 파일들
SRT_PATH = "original.srt"
VIDEO_PATH = "original.mp4"
VIDEO_DIR = "clips"
OUTPUT_DIR = "with_subs"
SUMMARY_PATH = "sample.txt"
HIGHLIGHT_PATH = "highlights.json"

# 출력 폴더 만들기
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# 자막 불러오기
def load_srt(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(srt.parse(f.read()))

# 자막 범위 필터링
def extract_subs(entries, start, end):
    return [e for e in entries if e.start >= start and e.start <= end]

# GPT를 통한 자동 요약
def generate_summary(subs):
    full_text = "\n".join([s.content for s in subs])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 시사 영상 자막을 요약하는 요약봇이야."},
            {"role": "user", "content": f"다음 자막 내용을 핵심만 문장 단위로 요약해줘:\n{full_text}"}
        ],
        temperature=0.5,
        max_tokens=1024
    )
    return response["choices"][0]["message"]["content"]

# 요약문으로부터 하이라이트 시간 추출 (GPT 활용)
def generate_highlight_times(subs, summary):
    full_text = "\n".join([s.content for s in subs])
    prompt = f"다음 자막 전체 내용에서 아래 핵심 요약 문장을 기준으로 해당 문장이 나타나는 자막의 시작~끝 시간 구간을 hh:mm:ss 형식으로 JSON 리스트로 만들어줘. 예: [{{\"highlight\": \"내용\", \"start\": \"00:01:23\", \"end\": \"00:01:29\"}}, ...]\n\n요약문:\n{summary}\n\n전체 자막:\n{full_text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 시사 영상에서 자막 기반으로 시간 구간을 추출하는 봇이야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=1500
    )
    return json.loads(response["choices"][0]["message"]["content"])

# 자막 자동 요약 + 하이라이트 추출 + 컷팅 + 자막 입히기 처리
def process():
    subs = load_srt(SRT_PATH)

    # 자동 요약 생성
    summary_text = generate_summary(subs)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write(summary_text)
    print("📝 자동 요약 완료 → sample.txt")

    # 하이라이트 시간 자동 추출
    highlights = generate_highlight_times(subs, summary_text)
    with open(HIGHLIGHT_PATH, "w", encoding="utf-8") as f:
        json.dump(highlights, f, ensure_ascii=False, indent=2)
    print("⏱ 자동 하이라이트 추출 완료 → highlights.json")

    for idx, item in enumerate(highlights, start=1):
        clip_name = f"highlight_{idx:02}.mp4"
        srt_name = f"highlight_{idx:02}.srt"
        output_name = f"with_subs_{idx:02}.mp4"

        start_parts = [int(x) for x in item["start"].split(":")]
        end_parts = [int(x) for x in item["end"].split(":")]

        start_time = timedelta(hours=start_parts[0], minutes=start_parts[1], seconds=start_parts[2])
        end_time = timedelta(hours=end_parts[0], minutes=end_parts[1], seconds=end_parts[2])

        # 하이라이트 영상 잘라내기
        cut_cmd = [
            "ffmpeg",
            "-i", VIDEO_PATH,
            "-ss", item["start"],
            "-to", item["end"],
            "-c:v", "libx264",
            "-c:a", "aac",
            os.path.join(VIDEO_DIR, clip_name)
        ]
        print(f"✂️ 영상 자르는 중: {item['start']} ~ {item['end']} → {clip_name}")
        subprocess.run(cut_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 자막 추출
        clip_subs = extract_subs(subs, start_time, end_time)
        with open(os.path.join(OUTPUT_DIR, srt_name), "w", encoding="utf-8") as f:
            f.write(srt.compose(clip_subs))

        # 자막 입히기
        cmd = [
            "ffmpeg",
            "-i", os.path.join(VIDEO_DIR, clip_name),
            "-vf", f"subtitles={os.path.join(OUTPUT_DIR, srt_name)}",
            "-c:a", "copy",
            os.path.join(OUTPUT_DIR, output_name)
        ]

        print(f"🎬 자막 입히는 중: {clip_name} → {output_name}")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n✅ 모든 자막 처리 완료 → {OUTPUT_DIR}/with_subs_*.mp4")

if __name__ == "__main__":
    process()
