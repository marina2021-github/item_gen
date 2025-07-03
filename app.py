import streamlit as st

# PDF 처리용 임포트
try:
    import fitz  # PyMuPDF
except ModuleNotFoundError:
    st.error("❌ PyMuPDF(fitz) 모듈이 설치되지 않았습니다.\nrequirements.txt에 `PyMuPDF`를 추가하세요.")
    st.stop()

# 앱 기본 설정
st.set_page_config(page_title="AI 기반 문항 생성기", layout="centered")
st.title("📚 AI 기반 기출 문항 생성기")

st.markdown("기존 문항 파일을 업로드하면 텍스트를 추출하고, AI 기반 문항 생성을 준비합니다.")

# 파일 업로더 (.txt, .pdf 모두 허용)
uploaded_file = st.file_uploader("기출 문항 파일을 업로드하세요 (.txt 또는 .pdf)", type=["txt", "pdf"])

# PDF 텍스트 추출 함수
def extract_text_from_pdf(file) -> str:
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

# 파일 처리
if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode('utf-8').strip()
    elif uploaded_file.name.endswith(".pdf"):
        input_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("❌ 지원하지 않는 파일 형식입니다.")
        st.stop()

    st.success("✅ 텍스트 추출 완료!")
    st.text_area("📄 추출된 문항 텍스트", input_text, height=300)
