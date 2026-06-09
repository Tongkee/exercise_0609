import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. 환경 변수 로드 (.env 파일에서 API 키 가져오기)
load_dotenv()
api_key_status = "OPENAI_API_KEY" in os.environ

# 페이지 기본 설정
st.set_page_config(page_title="파이썬 코드 리뷰어", page_icon="🐍", layout="wide")

# ==========================================
# 사이드바 (설정, 모델 선택 및 팁)
# ==========================================
with st.sidebar:
    st.header("⚙️ 설정")
    if api_key_status:
        st.success("✅ API Key 준비 완료 (.env 로드됨)")
    else:
        st.error("❌ API Key를 찾을 수 없습니다. .env 파일을 확인하세요.")
        
    # [추가된 기능] AI 모델 선택창 (selectbox)
    # 기본값을 가장 가성비가 좋은 gpt-4o-mini(index=1)로 설정합니다.
    selected_model = st.selectbox(
        "🤖 AI 모델을 선택하세요:",
        ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
        index=1,
        help="gpt-4o는 가장 똑똑하지만 비용이 더 많이 발생하며, mini는 빠르고 경제적입니다."
    )
    
    st.markdown("---")
    
    st.header("💡 비전공자를 위한 팁")
    st.info("코드가 작동하지 않을 때는 **'2. 에러 해결사'** 탭을, 코드가 무슨 뜻인지 알고 싶을 때는 **'1. 코드 설명기'** 탭을 사용하세요!")

# ==========================================
# 메인 화면
# ==========================================
st.title("🐍 왕초보를 위한 파이썬 코드 리뷰 & 디버깅 툴")
st.write("어려운 개발 용어 대신 일상적인 표현으로 파이썬 코드를 설명하고 고쳐줍니다.")

# 사용자가 사이드바에서 선택한 모델(selected_model)을 실시간으로 반영하여 LLM 초기화
llm = ChatOpenAI(model=selected_model, temperature=0.7) if api_key_status else None

# 탭 생성
tab1, tab2, tab3 = st.tabs(["🔍 1. 쉬운 코드 설명기", "🛠️ 2. 에러 해결사", "🚀 3. 내 코드 개선하기"])

# --- 탭 1: 쉬운 코드 설명기 ---
with tab1:
    st.subheader("🔍 코드 설명기")
    st.write(f"현재 선택된 모델: **{selected_model}**")
    st.write("이 코드가 무슨 일을 하는지 비유를 들어 쉽게 알려드립니다.")
    
    code_input_1 = st.text_area("여기에 파이썬 코드를 붙여넣으세요:", height=200, placeholder="print('Hello World') 등 아무 코드나 입력 가능", key="code1")
    
    if st.button("설명 시작하기", key="btn1"):
        if not api_key_status:
            st.warning("API 키가 설정되지 않아 AI를 호출할 수 없습니다.")
        elif code_input_1:
            with st.spinner(f"AI({selected_model})가 코드를 분석하는 중입니다..."):
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "당신은 코딩을 전혀 모르는 50대 비전공자도 이해할 수 있도록, 파이썬 코드를 일상생활의 쉬운 비유(예: 요리 레시피, 자동차 운전 등)를 들어 설명해주는 친절한 튜터입니다. 전문 용어는 최대한 풀어서 설명하세요."),
                    ("user", "다음 파이썬 코드를 아주 쉽게 설명해주세요:\n\n{code}")
                ])
                chain = prompt | llm
                response = chain.invoke({"code": code_input_1})
                
                st.success("✨ 설명이 완료되었습니다!")
                st.write(response.content)
        else:
            st.warning("설명할 코드를 먼저 입력해주세요.")

# --- 탭 2: 에러 해결사 ---
with tab2:
    st.subheader("🛠️ 에러 해결사")
    st.write(f"현재 선택된 모델: **{selected_model}**")
    st.write("빨간색 에러 메시지가 떴나요? 당황하지 마세요. 원인과 해결책을 알려드립니다.")
    
    code_input_2 = st.text_area("문제가 발생한 코드와 에러 메시지를 함께 붙여넣으세요:", height=200, key="code2")
    
    if st.button("에러 원인 찾기", key="btn2"):
        if code_input_2 and llm:
            with st.spinner(f"AI({selected_model})가 에러의 원인을 파악하고 있습니다..."):
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "당신은 파이썬 초보자의 에러를 다정하게 고쳐주는 디버깅 전문가입니다. 에러의 원인을 비전공자의 언어로 설명하고, 복사해서 바로 쓸 수 있는 수정된 코드를 제공하세요."),
                    ("user", "다음 코드에서 에러가 났습니다. 도와주세요:\n\n{code}")
                ])
                chain = prompt | llm
                response = chain.invoke({"code": code_input_2})
                st.write(response.content)

# --- 탭 3: 내 코드 개선하기 ---
with tab3:
    st.subheader("🚀 내 코드 개선하기")
    st.write(f"현재 선택된 모델: **{selected_model}**")
    st.write("작동은 하지만 더 깔끔하고 전문가스럽게 코드를 다듬고 싶을 때 사용하세요.")
    
    code_input_3 = st.text_area("개선하고 싶은 코드를 붙여넣으세요:", height=200, key="code3")
    
    if st.button("코드 다듬기", key="btn3"):
        if code_input_3 and llm:
            with st.spinner(f"AI({selected_model})가 코드를 더 효율적으로 리팩토링하고 있습니다..."):
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "당신은 파이썬 시니어 개발자입니다. 초보자가 짠 코드를 파이썬의 권장 스타일(PEP 8)과 효율성을 고려해 개선(리팩토링)해주세요. 어떤 부분을 왜 고쳤는지 초보자가 이해하기 쉽게 이유를 덧붙여주세요."),
                    ("user", "다음 코드를 더 깔끔하게 개선해주세요:\n\n{code}")
                ])
                chain = prompt | llm
                response = chain.invoke({"code": code_input_3})
                st.write(response.content)