# Subtitle Extractor 프로젝트

이 리포지토리는 시사 유튜브 영상을 자동으로 요약하고, 하이라이트를 추출하며, 자막을 입힌 클립 영상까지 자동으로 생성하는 파이썬 도구입니다.

## 📂 폴더 구조
```
project_root/
├── original.mp4            # 원본 영상
├── original.srt            # 원본 자막 파일
├── sample.txt              # 요약 결과 저장 파일
├── highlights.json         # 하이라이트 타임코드 저장
├── clips/                  # 자른 클립 영상
├── with_subs/              # 자막 입힌 최종 영상 + 자막 파일
├── subtitle_extractor.py   # 메인 실행 파일
├── requirements.txt        # 설치 필요한 라이브러리 목록
└── .gitignore              # GitHub에 올리지 않을 파일 목록
```

## ▶️ 실행 방법
1. `.env` 파일에 OpenAI API 키를 넣거나 PowerShell에서 환경변수로 설정합니다:
   ```bash
   $env:OPENAI_API_KEY="sk-..."
   ```
2. Python 환경을 만들고 필요한 패키지를 설치:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. 영상(`original.mp4`)과 자막(`original.srt`) 준비 후 실행:
   ```bash
   python subtitle_extractor.py
   ```

## 🧠 기능 요약
- 전체 자막 텍스트 기반 자동 요약
- 요약문에 해당하는 하이라이트 구간 추출 (시간)
- 해당 구간 영상 클립 자르기
- 각 클립에 자막 입히기 (ffmpeg 사용)

## 📦 requirements.txt 내용:
```txt
openai
python-dotenv
srt
```

## 🙈 .gitignore 내용:
```txt
.env
__pycache__/
*.pyc
venv/
```

---

필요한 기능이 있으면 `issue` 또는 `pull request`로 알려주세요! 😊
