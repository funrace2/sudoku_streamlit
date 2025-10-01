import streamlit as st
import numpy as np
import random
import json
import time
import pandas as pd
from datetime import timedelta
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="스도쿠",
    page_icon="🔢",
    layout="wide"
)

BASE_BOARD = np.array([
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
])

def generate_sudoku(difficulty):
    nums = list(range(1, 10))
    random.shuffle(nums)
    mapping = {i + 1: nums[i] for i in range(9)}

    solution = np.vectorize(mapping.get)(BASE_BOARD)

    puzzle_board = solution.copy()
    total_cells = 81
    cells_to_remove = int(total_cells * difficulty)
    
    indices = np.random.choice(total_cells, cells_to_remove, replace=False)
    puzzle_board.flat[indices] = 0

    return puzzle_board, solution

def save_score(name, time_seconds):
    new_score = {"name": name, "time": time_seconds}
    try:
        with open("ranking.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = []
    
    scores.append(new_score)
    scores_sorted = sorted(scores, key=lambda x: x["time"])
    
    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(scores_sorted, f, indent=4, ensure_ascii=False)

def load_scores():
    try:
        with open("ranking.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
        return scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []

st.markdown("""
    <style>
    /* 제목 중앙 정렬 */
    h1 { text-align: center; }
    /* 입력 필드를 스도쿠 칸처럼 보이게 스타일링 */
    .stTextInput input {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        height: 50px;
        width: 50px;
        border-radius: 5px;
        border-width: 2px;
    }
    div[data-testid="stColumn"]:nth-of-type(3),
    div[data-testid="stColumn"]:nth-of-type(6) {
        border-right: 2px solid #999;
        padding-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- 세션 상태(Session State) 초기화 ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.puzzle_board = None
    st.session_state.solution_board = None
    st.session_state.start_time = None
    st.session_state.game_over = False

# --- UI 레이아웃 ---
st.title("🔢 스도쿠")
st.write("---")

with st.sidebar:
    st.header("게임 설정")
    difficulty_map = {"쉬움": 0.3, "보통": 0.5, "어려움": 0.7, "전문가": 0.8}
    difficulty_level = st.select_slider(
        "난이도 선택",
        options=difficulty_map.keys(),
        value="보통"
    )
    difficulty_value = difficulty_map[difficulty_level]

    if st.button("새 게임 시작", type="primary"):
        st.session_state.puzzle_board, st.session_state.solution_board = generate_sudoku(difficulty_value)
        st.session_state.start_time = time.time()
        st.session_state.game_started = True
        st.session_state.game_over = False
        st.rerun()

    st.write("---")
    st.header("랭킹")
    scores = load_scores()
    if scores:
        df = pd.DataFrame(scores)
        df.index = np.arange(1, len(df) + 1) # 순위
        df['time'] = df['time'].apply(lambda s: str(timedelta(seconds=int(s))))
        st.dataframe(df.rename(columns={'name': '이름', 'time': '기록'}), use_container_width=True)
    else:
        st.info("아직 기록이 없습니다. 첫 번째 주인공이 되어보세요!")

# --- 메인 게임 영역 ---
if not st.session_state.game_started:
    st.info("사이드바에서 '새 게임 시작' 버튼을 눌러주세요!")
else:
    main_cols = st.columns([2, 1]) # 보드와 컨트롤 영역 분리
    
    with main_cols[0]:
        st.header("스도쿠 보드")
        # 모든 입력 위젯을 form으로 묶어, 키 입력마다 앱이 재실행되는 것을 방지
        with st.form(key='sudoku_form'):
            user_board = st.session_state.puzzle_board.copy()
            
            # 9x9 입력 그리드 생성
            for r in range(9):
                cols = st.columns(9)
                for c in range(9):
                    cell_val = st.session_state.puzzle_board[r, c]
                    key = f"cell_{r}_{c}"
                    
                    if cell_val != 0:
                        # 미리 채워진 숫자 (수정 불가)
                        cols[c].text_input(key, value=str(cell_val), disabled=True, label_visibility="collapsed")
                    else:
                        # 사용자 입력 칸
                        user_input = cols[c].text_input(
                            key, value="", max_chars=1, label_visibility="collapsed", placeholder=""
                        )
                        # 입력값이 유효한 숫자인 경우 보드에 기록
                        if user_input.isdigit() and 1 <= int(user_input) <= 9:
                            user_board[r, c] = int(user_input)
                        else:
                            user_board[r, c] = 0 # 비어있거나 잘못된 입력은 0으로 처리

                if r == 2 or r == 5:
                        st.markdown("<div style='margin-top: 5px; margin-bottom: 5px; border-top: 2px solid #999;'></div>", unsafe_allow_html=True)
            st.session_state.user_board = user_board
            # form 내부에 '정답 확인' 버튼 배치
            submit_button = st.form_submit_button(label='정답 확인')

    with main_cols[1]:
        st.header("게임 정보")
        if not st.session_state.game_over:
            st_autorefresh(interval=1000, key="timer")
            elapsed_time = int(time.time() - st.session_state.start_time)
            st.metric("경과 시간", str(timedelta(seconds=elapsed_time)))
            st.info("모든 칸을 채우고 '정답 확인' 버튼을 누르세요.")
        else:
            # 최종 시간 및 성공 메시지 표시
            elapsed_time = st.session_state.final_time
            st.metric("최종 기록", str(timedelta(seconds=int(elapsed_time))))
            st.success(f"🎉 축하합니다! {int(elapsed_time)}초 만에 해결했습니다!")
            
            # 점수 저장을 위한 입력 폼
            with st.form("score_form"):
                user_name = st.text_input("이름을 입력하고 점수를 저장하세요:")
                if st.form_submit_button("점수 저장"):
                    if user_name:
                        save_score(user_name, elapsed_time)
                        st.toast(f"{user_name}님의 기록이 저장되었습니다!")
                    else:
                        st.warning("이름을 입력해주세요.")
    
    # --- 정답 확인 로직 (form 제출 후 실행) ---
    if submit_button:
        if np.array_equal(user_board, st.session_state.solution_board):
            st.balloons()
            st.session_state.game_over = True
            st.session_state.final_time = time.time() - st.session_state.start_time
            st.rerun()
        else:
            st.error("정답이 아닙니다. 다시 시도해보세요! 🤔")
