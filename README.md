# 🔢 Streamlit으로 만든 스도쿠 게임
Anaconda 환경에서 Python과 Streamlit을 활용하여 개발한 동적인 웹 기반 스도쿠 게임입니다. 사용자는 난이도를 선택하여 스도쿠 퍼즐을 풀고, 자신의 기록을 실시간 랭킹 보드에 저장할 수 있습니다.

# 🚀 라이브 데모 (Live Demo)
아래 링크를 통해 배포된 앱을 직접 플레이해볼 수 있습니다.

🔗 배포 링크: https://sudokuapp-spulybxwmfjv4ghwyx9qwy.streamlit.app

# 🎯 주요 기능 (Key Features)
 - 난이도 조절: 쉬움, 보통, 어려움, 전문가 4단계의 난이도를 슬라이더로 쉽게 선택할 수 있습니다.
 - 실시간 타이머: 게임이 시작되면 경과 시간이 실시간으로 표시됩니다.
 - 정답 확인: 모든 칸을 채운 후 '정답 확인' 버튼으로 정답 여부를 즉시 확인할 수 있습니다.
 - 스코어 랭킹 시스템: 게임 완료 시 이름과 시간을 ranking.json 파일에 기록하고, 순위를 사이드바에 표시합니다.

# 🛠️ 기술 스택 (Tech Stack)
 - ```Python``` (from Anaconda Distribution)
 - ```Streamlit```
 - ```Pandas```
 - ```NumPy```

# ⚙️ 시작하기 (Getting Started)
이 프로젝트는 Anaconda 환경에 최적화되어 있습니다.

## 필수 요구사항
 - Anaconda Distribution (Python 3.8 이상 포함)

## 설치 방법
1. GitHub 저장소를 복제합니다.

```bash
git clone https://github.com/funrace2/sudoku_streamlit.git
cd sudoku_streamlit
```

2. Conda 가상 환경을 생성하고 활성화합니다.

```bash
conda create -n sudoku-env python=3.9
conda activate sudoku-env
```

3. requirements.txt 파일의 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

# ▶️ 실행 방법 (Usage)
터미널에 아래 명령어를 입력하여 스도쿠 게임을 실행합니다.

```bash
streamlit run Sudoku_Streamlit.py
```

# 📁 파일 구조 (File Structure)

```
.
├── Sudoku_Streamlit.py              # 메인 Streamlit 애플리케이션 코드
├── requirements.txt      # 프로젝트 실행에 필요한 라이브러리 목록
└── ranking.json        # 사용자 랭킹이 저장되는 파일 (앱 실행 후 자동 생성)
```

