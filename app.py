import streamlit as st

# PDF 처리용
try:
    import fitz  # PyMuPDF
except ModuleNotFoundError:
    st.error("❌ PyMuPDF(fitz) 모듈이 설치되지 않았습니다. requirements.txt에 'PyMuPDF'를 추가하세요.")
    st.stop()

st.set_page_config(page_title="AI 기반 기출 문항 생성기", layout="centered")
st.title("📚 AI 기반 기출 문항 생성기")
st.markdown("기출 문항 파일을 업로드하고 유형 및 난이도를 선택하면 새로운 문항을 생성합니다.")

uploaded_file = st.file_uploader("📎 파일 업로드 (.txt 또는 .pdf)", type=["txt", "pdf"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

# 문항 추출 및 입력
input_text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode('utf-8').strip()
    elif uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)

    if input_text:
        st.success("✅ 텍스트 추출 완료!")
        st.markdown("#### 📄 추출된 문항 텍스트")
        st.text_area("추출된 문항", input_text, height=250, key="input_text")
    else:
        st.warning("⚠️ 추출된 텍스트가 없습니다. PDF가 이미지일 수 있습니다.")

# 옵션 선택 후 문항 생성
if input_text:
    st.markdown("### ⚙️ 문항 생성 옵션 선택")
    q_type = st.selectbox("문항 유형", ["객관식", "단답형", "서술형"])
    difficulty = st.selectbox("난이도", ["하", "중", "상"])

    if st.button("🧠 문항 생성하기"):
        # 간단한 예시 문항 생성
        dummy_question = {
            ("객관식", "중"): "x + 3 = 7 일 때 x의 값은?
① 3 ② 4 ③ 5 ④ 6",
            ("단답형", "중"): "x + 3 = 7 일 때 x의 값을 구하시오.",
            ("서술형", "상"): "어떤 수에 3을 더했더니 7이 되었습니다. 이 수를 구하는 과정을 서술하시오."
        }
        result = dummy_question.get((q_type, difficulty), "문항 유형에 해당하는 예시가 없습니다.")
        st.success("✅ 문항 생성 결과")
        st.text_area("📝 생성된 문항을 편집하세요", value=result, height=200, key="generated_question")

        if st.button("💾 최종 문항 저장"):
            st.success("✅ 문항이 저장되었습니다. (데모: 실제 저장 기능은 구현되지 않음)")
