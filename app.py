import streamlit as st
import requests
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

# PDF 텍스트 추출 시도용 (PyMuPDF)
try:
    import fitz
except ModuleNotFoundError:
    fitz = None

st.set_page_config(page_title="AI 기반 문항 생성기 (OCR + LLM)", layout="centered")
st.title("📚 AI 기반 기출 문항 생성기")
st.markdown("PDF나 텍스트 문서를 업로드하면, AI가 문항을 분석하고 새 문항을 생성합니다.")

uploaded_file = st.file_uploader("📎 파일 업로드 (.txt 또는 .pdf)", type=["txt", "pdf"])

def extract_text_from_image_pdf(file) -> str:
    images = convert_from_bytes(file.read())
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='kor+eng') + "\n"
    return text.strip()

def extract_text_from_pdf_or_image(file) -> str:
    file_bytes = file.read()
    text = ""

    # 1. 텍스트 기반 PDF 시도 (PyMuPDF)
    if fitz:
        try:
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        except:
            pass

    # 2. OCR로 fallback
    if not text.strip():
        try:
            text = extract_text_from_image_pdf(file)
        except Exception as e:
            st.error(f"OCR 처리 실패: {e}")
            return ""

    return text.strip()

def generate_question_llm(context_text, q_type, difficulty):
    prompt = f"""
다음은 기출 문항입니다:

{context_text}

이 문항과 동일한 단원에서, 유형은 '{q_type}', 난이도는 '{difficulty}'인 새로운 문항을 생성해 주세요.
문항 유형에 맞게 보기 또는 정답도 함께 작성해 주세요.
"""

    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourappname.streamlit.app"
    }

    body = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"[ERROR] {response.status_code}: {response.text}"

# 1. 문항 텍스트 추출
input_text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        input_text = uploaded_file.read().decode('utf-8').strip()
    elif uploaded_file.name.endswith(".pdf"):
        with st.spinner("📄 PDF에서 텍스트 추출 중..."):
            input_text = extract_text_from_pdf_or_image(uploaded_file)

    if not input_text:
        st.warning("⚠️ 추출된 텍스트가 없습니다. PDF가 이미지이고 OCR도 실패했을 수 있습니다.")
    else:
        st.success("✅ 텍스트 추출 완료!")
        st.text_area("📄 추출된 문항 텍스트", input_text, height=300)

# 2. 문항 생성 옵션 + LLM 호출
if input_text:
    st.markdown("### ⚙️ 문항 생성 옵션 선택")
    q_type = st.selectbox("문항 유형", ["객관식", "단답형", "서술형"])
    difficulty = st.selectbox("난이도", ["하", "중", "상"])

    if st.button("🧠 LLM으로 문항 생성하기"):
        with st.spinner("AI가 문항을 생성 중입니다..."):
            result = generate_question_llm(input_text, q_type, difficulty)
        st.success("✅ 생성된 문항:")
        st.text_area("📝 문항을 편집하세요", value=result, height=300, key="generated_question")
        if st.button("💾 최종 문항 저장"):
            st.success("✅ 문항 저장 완료! (데모 상태)")
