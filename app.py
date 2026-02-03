import streamlit as st
import pandas as pd
import time
import requests
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie_spinner

st.set_page_config(page_title="할 일 저장함", page_icon="✅", layout="wide")
st.title("✅ 할 일 저장함 (Navigation + Lottie)")

# --- Cache: 우선순위 옵션 로드 ---
@st.cache_data
def load_priorities():
    return ["낮음", "보통", "높음"]

priorities = load_priorities()

# --- Lottie 로드 함수 ---
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 로딩용 Lottie (원하는 걸로 바꿔도 됨)
LOTTIE_LOADING_URL = "https://assets4.lottiefiles.com/packages/lf20_fL5QbCnATl.json"
loading_json = load_lottie_url(LOTTIE_LOADING_URL)

# --- Session 초기화 ---
if "todos" not in st.session_state:
    st.session_state["todos"] = []

# --- Navigation ---
with st.sidebar:
    page = option_menu(
        "메뉴",
        ["할일추가", "목록", "설정"],
        icons=["plus-circle", "list-check", "gear"],
        menu_icon="list",
        default_index=0,
    )

st.caption(f"현재 선택: {page}")

# --- Pages ---
if page == "할일추가":
    st.subheader("➕ 할 일 추가")

    with st.form("todo_form"):
        todo = st.text_input("할 일", placeholder="예) Streamlit 과제 제출")
        pr = st.selectbox("우선순위", priorities)
        submitted = st.form_submit_button("저장")

    if submitted:
        if not todo.strip():
            st.error("할 일을 입력하세요.")
        else:
            # 로딩 연출
            if loading_json is not None:
                with st_lottie_spinner(loading_json, speed=1.5):
                    time.sleep(2)
            else:
                time.sleep(1)

            st.session_state["todos"].append({"할 일": todo.strip(), "우선순위": pr})
            st.success("저장 완료! 목록에서 확인하세요.")

elif page == "목록":
    st.subheader("📋 목록")

    if len(st.session_state["todos"]) == 0:
        st.info("아직 할 일이 없습니다. '할일추가'에서 추가해보세요.")
    else:
        df = pd.DataFrame(st.session_state["todos"])
        st.dataframe(df, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("마지막 항목 삭제"):
            if st.session_state["todos"]:
                removed = st.session_state["todos"].pop()
                st.warning(f"삭제됨: {removed}")
                st.rerun()
            else:
                st.info("삭제할 항목이 없습니다.")

    with c2:
        if st.button("전체 비우기"):
            st.session_state["todos"].clear()
            st.warning("전체 비우기 완료!")
            st.rerun()

elif page == "설정":
    st.subheader("⚙️ 설정")
    st.markdown(
        """
        <div style="padding:12px;border-radius:12px;border:1px solid #ddd;background:#fafafa;">
          <b>테마 적용 팁</b><br/>
          <span>.streamlit/config.toml 을 만들면 전체 UI가 바뀝니다.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(
        """# .streamlit/config.toml 예시
[theme]
base="dark"
primaryColor="#F97316"
backgroundColor="#0B1220"
secondaryBackgroundColor="#111B2E"
textColor="#E5E7EB"
font="sans serif"
""",
        language="toml",
    )