import difflib
import srt
from datetime import timedelta
import argparse

def load_summary_lines(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_srt_entries(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        return list(srt.parse(f.read()))

def find_best_match(summary_line, srt_entries):
    best_score = 0
    best_entry = None
    for entry in srt_entries:
        score = difflib.SequenceMatcher(None, summary_line, entry.content).ratio()
        if score > best_score:
            best_score = score
            best_entry = entry
    return best_entry, best_score

def main(summary_path, srt_path, output_path):
    summary_lines = load_summary_lines(summary_path)
    srt_entries = load_srt_entries(srt_path)

    print("요약 문장 수:", len(summary_lines))
    print("자막 줄 수:", len(srt_entries))

    results = []
    for line in summary_lines:
        entry, score = find_best_match(line, srt_entries)
        if entry:
            results.append({
                "highlight": line,
                "start": str(entry.start).split(".")[0],
                "end": str(entry.end).split(".")[0]
            })

    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(results)}개의 하이라이트가 추출되었습니다. → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True, help="요약 파일 경로")
    parser.add_argument("--srt", required=True, help="자막 파일 경로 (.srt)")
    parser.add_argument("--output", default="highlights.json", help="출력 JSON 파일 이름")
    args = parser.parse_args()

    main(args.summary, args.srt, args.output)

    

