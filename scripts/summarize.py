import argparse
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 OpenAI API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    prompt = f"""다음 자막 내용을 핵심 요점만 요약해줘:\n\n{text}\n\n요약:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "user", "content": prompt }
        ],
        temperature=0.5,
        max_tokens=800
    )

    return response["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", type=str, required=True, help="자막 텍스트 파일 경로")
    args = parser.parse_args()

    # 텍스트 파일 읽기
    with open(args.transcript, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # 요약 수행
    summary = summarize_text(transcript_text)
    print("\n✅ 요약 결과:\n")
    print(summary)
