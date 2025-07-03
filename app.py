import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="문항 생성기", layout="centered")
st.title("📚 AI 기반 기출 문항 생성기")

uploaded_file = st.file_uploader("기출 문항 파일을 업로드하세요 (.txt 또는 .pdf)", type=["txt", "pdf"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode('utf-8')
    elif uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("지원하지 않는 파일 형식입니다.")
        st.stop()

    st.text_area("📄 추출된 문항 텍스트", input_text, height=200)
