# Risu Novel Extractor

RisuAI의 채팅 로그(JSON)를 소설 형식의 Markdown으로 변환하거나, 웹 브라우저에서 편리하게 읽을 수 있도록 도와주는 도구 모음입니다.

## 🛠 구성 요소

1. **risu_to_novel.py**: Python 기반의 변환 스크립트. 
   - RisuAI에서 내보낸 JSON 파일을 분석하여 인물별 대사, 지문, <details> 태그 내의 요약 정보 등을 깔끔한 마크다운 소설 포맷으로 추출합니다.
2. **viewer.html**: 로컬 HTML 뷰어.
   - 별도의 서버 없이 웹 브라우저에서 실행 가능합니다.
   - 드래그 앤 드롭으로 JSON 파일을 불러와 채팅 형식으로 렌더링합니다.

## 🚀 사용법

### Python 스크립트
```bash
python3 risu_to_novel.py [입력_파일.json] --output [출력_파일.md]
```

### 로컬 뷰어
1. `viewer.html` 파일을 웹 브라우저로 엽니다.
2. RisuAI에서 추출한 JSON 파일을 화면 위로 드래그 앤 드롭합니다.

---
*Created by Veritas Ratio (via OpenClaw)*
