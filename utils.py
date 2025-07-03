from typing import Dict
import random

# 예시: 단순 rule-based 분석
def analyze_question(text: str) -> Dict:
    topic = "일차방정식" if "x" in text else "미분"
    q_type = "객관식" if "①" in text else "주관식"
    difficulty = "중"
    return {"단원": topic, "유형": q_type, "난이도": difficulty}

# 예시: 간단한 생성기
def generate_question(original_text: str, metadata: Dict, new_type: str, new_difficulty: str) -> Dict:
    # 실제로는 LLM으로 프롬프트 생성 필요
    question_bank = {
        ("일차방정식", "서술형", "상"): (
            "어떤 수에서 3을 빼고 2를 곱했더니 10이 되었습니다. 이 수를 구하고 풀이 과정을 서술하시오.", "8"
        ),
        ("일차방정식", "단답형", "중"): (
            "x + 7 = 12 일 때 x의 값을 구하시오.", "5"
        ),
    }
    key = (metadata["단원"], new_type, new_difficulty)
    return {
        "question": question_bank.get(key, ("[예시 문항 없음]", "?"))[0],
        "answer": question_bank.get(key, ("[예시 문항 없음]", "?"))[1]
    }