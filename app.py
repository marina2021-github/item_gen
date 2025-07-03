import streamlit as st
import requests

# PDF 처리용
try:
    import fitz  # PyMuPDF
except ModuleNotFoundError:
    st.error("❌ PyMuPDF(fitz) 모듈이 설치되지 않았습니다. requirements.txt에 'PyMuPDF'를 추가하세요.")
    st.stop()

st.set_page_config(page_title="AI 기반 문항 생성기 (LLM)", layout="centered")
st.title("📚 AI 기반 기출 문항 생성기")
st.markdown("PDF나 텍스트 문서를 업로드하면, AI가 문항을 분석하고 새 문항을 생성합니다.")

uploaded_file = st.file_uploader("📎 파일 업로드 (.txt 또는 .pdf)", type=["txt", "pdf"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def generate_question_llm(context_text, q_type, difficulty):
    prompt = f"""
다음은 기출 문항입니다:

{context_text}

이 문항과 동일한 단원에서, 유형은 '{q_type}', 난이도는 '{difficulty}'인 새로운 문항을 생성해 주세요.
문항 유형에 맞게 보기 또는 답도 함께 작성해 주세요.
"""

    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourappname.streamlit.app"  # 여기에 앱 URL 지정 가능
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
        st.text_area("기존 문항", input_text, height=250, key="input_text")
    else:
        st.warning("⚠️ 추출된 텍스트가 없습니다. PDF가 이미지일 수 있습니다.")

# 옵션 선택 후 문항 생성
if input_text:
    st.markdown("### ⚙️ 문항 생성 옵션 선택")
    q_type = st.selectbox("문항 유형", ["객관식", "단답형", "서술형"])
    difficulty = st.selectbox("난이도", ["하", "중", "상"])

    if st.button("🧠 LLM으로 문항 생성하기"):
        with st.spinner("AI가 새로운 문항을 생성 중입니다..."):
            generated = generate_question_llm(input_text, q_type, difficulty)
        st.success("✅ 생성된 문항:")
        st.text_area("📝 문항을 편집하세요", value=generated, height=300, key="generated_question")
        if st.button("💾 최종 문항 저장"):
            st.success("📝 저장 완료! (데모)")
