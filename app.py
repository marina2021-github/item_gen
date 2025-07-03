import streamlit as st

st.set_page_config(
    page_title="AI 기반 기출 문항 생성기",
    page_icon="📄",
    layout="centered",
)

st.markdown("## 📄 AI 기반 기출 문항 생성기")
st.markdown("PDF나 텍스트 문서를 업로드하면, AI가 문항을 분석하고 새 문항을 생성합니다.")

# 파일 업로드
st.markdown("### 📎 파일 업로드 (.txt 또는 .pdf)")
uploaded_file = st.file_uploader("Drag and drop file here", type=["txt", "pdf"])

# 추출된 텍스트 영역
st.markdown("### 📝 추출된 텍스트 (또는 입력 텍스트)")
text_input = st.text_area("텍스트 내용", height=300)

# 문항 수 및 생성 버튼
st.markdown("### ⚙️ 문항 생성 설정")
col1, col2 = st.columns(2)
with col1:
    num_questions = st.number_input("생성할 문항 수", min_value=1, max_value=20, value=3)
with col2:
    difficulty = st.selectbox("난이도 선택", ["초급", "중급", "고급"])

# 문항 생성 버튼
if st.button("📚 문항 생성"):
    st.success(f"{num_questions}개의 문항을 생성했습니다. (예시 출력)")

    for i in range(1, num_questions + 1):
        st.markdown(f"**Q{i}. 예시 문항 내용입니다.**")
