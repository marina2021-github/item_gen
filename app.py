import streamlit as st
from utils import analyze_question, generate_question
from pathlib import Path

st.set_page_config(page_title="문항 생성기", layout="centered")

st.title("📚 AI 기반 기출 문항 생성기")
st.markdown("기존 문항을 업로드하면, 단원·유형·난이도를 분석하고 새로운 문항을 생성합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("기존 문항 파일을 업로드하세요 (.txt)", type=['txt'])
if uploaded_file:
    input_text = uploaded_file.read().decode('utf-8')
    st.text_area("원본 문항", input_text, height=150)

    # 분석
    metadata = analyze_question(input_text)
    st.write("### 문항 분석 결과:")
    st.json(metadata)

    # 설정
    st.write("### 생성 문항 옵션 선택")
    new_type = st.selectbox("문항 유형", ["객관식", "단답형", "서술형"])
    new_difficulty = st.selectbox("난이도", ["하", "중", "상"])

    if st.button("📌 새 문항 생성"):
        generated = generate_question(input_text, metadata, new_type, new_difficulty)
        st.success("✅ 새 문항이 생성되었습니다:")
        st.markdown(f"**{generated['question']}**")
        st.markdown(f"**[정답]** {generated['answer']}")
