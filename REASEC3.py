"""
RIASEC 진로탐색 웹서비스
사용자가 문항에 응답하여 자신의 흥미 유형을 파악하고 관련 직업과 학과를 추천받습니다.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# 페이지 설정
# ============================================================
#st.set_page_config(
#    page_title="RIASEC 진로탐색",
#    page_icon="🎯",
#    layout="wide"
#)


# ============================================================
# 데이터 정의
# ============================================================

# RIASEC 유형 설명
RIASEC_INFO = {
    "R": {
        "name": "현실형 (Realistic)",
        "description": "기계나 도구를 다루는 것을 좋아하고, 실제적이고 체계적인 활동을 선호합니다.",
        "characteristics": "손재주, 신체활동, 기계적 능력"
    },
    "I": {
        "name": "탐구형 (Investigative)",
        "description": "관찰하고 분석하며 문제를 해결하는 것을 좋아하고, 지적 호기심이 강합니다.",
        "characteristics": "분석력, 논리적 사고, 탐구심"
    },
    "A": {
        "name": "예술형 (Artistic)",
        "description": "창의적이고 자유로운 환경을 선호하며, 예술적 표현을 즐깁니다.",
        "characteristics": "창의성, 감수성, 독창성"
    },
    "S": {
        "name": "사회형 (Social)",
        "description": "다른 사람을 돕고 가르치는 것을 좋아하며, 협력적인 활동을 선호합니다.",
        "characteristics": "친절함, 이해심, 봉사정신"
    },
    "E": {
        "name": "진취형 (Enterprising)",
        "description": "리더십을 발휘하고 목표를 달성하는 것을 좋아하며, 경쟁적인 환경을 선호합니다.",
        "characteristics": "설득력, 추진력, 리더십"
    },
    "C": {
        "name": "관습형 (Conventional)",
        "description": "체계적이고 규칙적인 업무를 선호하며, 정확성과 세밀함을 중요시합니다.",
        "characteristics": "정확성, 조직력, 책임감"
    }
}

# RIASEC 문항 (각 유형당 8개씩, 총 48개)
QUESTIONS = {
    "R": [
        "자동차나 기계를 수리하는 것을 좋아한다",
        "야외에서 일하는 것이 실내보다 좋다",
        "손으로 무언가를 만드는 활동을 즐긴다",
        "공구나 기계를 다루는 데 자신이 있다",
        "체력을 사용하는 일을 선호한다",
        "전기나 전자제품을 조립하는 것에 흥미가 있다",
        "건축이나 목공 작업에 관심이 있다",
        "농업이나 임업 관련 활동을 좋아한다"
    ],
    "I": [
        "과학적 현상에 대해 탐구하는 것을 좋아한다",
        "복잡한 문제를 분석하고 해결하는 것을 즐긴다",
        "실험이나 연구 활동에 흥미가 있다",
        "수학이나 과학 과목을 좋아한다",
        "새로운 이론이나 개념을 배우는 것을 좋아한다",
        "논리적으로 생각하고 추론하는 것을 잘한다",
        "자연현상이나 우주에 대한 호기심이 많다",
        "데이터를 분석하고 패턴을 찾는 것을 즐긴다"
    ],
    "A": [
        "그림 그리기나 디자인하는 것을 좋아한다",
        "음악을 연주하거나 노래하는 것을 즐긴다",
        "창의적인 아이디어를 내는 것을 잘한다",
        "글쓰기나 시 쓰기를 좋아한다",
        "연극이나 영화에 관심이 많다",
        "독특하고 개성 있는 것을 추구한다",
        "예술 작품을 감상하는 것을 즐긴다",
        "새로운 것을 창조하는 활동을 선호한다"
    ],
    "S": [
        "다른 사람을 돕는 일을 좋아한다",
        "아이들을 가르치거나 돌보는 것을 즐긴다",
        "사람들과 협력하여 일하는 것을 선호한다",
        "다른 사람의 고민을 들어주고 조언하는 것을 좋아한다",
        "봉사활동에 적극적으로 참여한다",
        "팀 프로젝트에서 조화를 중요시한다",
        "사람들과 대화하고 소통하는 것을 즐긴다",
        "사회 문제에 관심이 많고 해결하고 싶다"
    ],
    "E": [
        "다른 사람을 설득하는 것을 잘한다",
        "리더가 되어 팀을 이끄는 것을 좋아한다",
        "경쟁적인 환경에서 동기부여를 받는다",
        "사업이나 창업에 관심이 있다",
        "목표를 세우고 달성하는 것을 즐긴다",
        "판매나 마케팅 활동에 흥미가 있다",
        "새로운 프로젝트를 시작하는 것을 좋아한다",
        "영향력 있는 사람이 되고 싶다"
    ],
    "C": [
        "정리정돈을 잘하고 체계적으로 일한다",
        "규칙과 절차를 따르는 것을 선호한다",
        "세밀한 작업을 정확하게 수행하는 것을 좋아한다",
        "데이터나 숫자를 다루는 일에 흥미가 있다",
        "계획을 세우고 그대로 실행하는 것을 잘한다",
        "문서 작성이나 기록 관리를 잘한다",
        "반복적이고 안정적인 업무를 선호한다",
        "사무 업무에 적합하다고 생각한다"
    ]
}

# 직업 데이터
JOBS_DATA = {
    "R": ["기계공학기술자", "전기기사", "자동차정비사", "건축기사", "토목기사", "항공정비사", "용접공", "농업기술자"],
    "I": ["과학자", "의사", "약사", "생명공학연구원", "데이터분석가", "소프트웨어개발자", "화학연구원", "수학자"],
    "A": ["그래픽디자이너", "음악가", "작가", "영화감독", "배우", "사진작가", "패션디자이너", "웹디자이너"],
    "S": ["교사", "상담사", "사회복지사", "간호사", "유치원교사", "심리상담사", "작업치료사", "요양보호사"],
    "E": ["CEO", "영업관리자", "마케팅전문가", "변호사", "정치인", "광고기획자", "인사관리자", "창업가"],
    "C": ["회계사", "경리직원", "은행원", "비서", "사무원", "세무사", "감정평가사", "행정공무원"]
}

# 학과 데이터
MAJORS_DATA = {
    "R": ["기계공학과", "전기전자공학과", "건축공학과", "토목공학과", "항공우주공학과", "산업공학과", "신소재공학과", "농업학과"],
    "I": ["의학과", "약학과", "생명공학과", "컴퓨터공학과", "화학과", "물리학과", "수학과", "통계학과"],
    "A": ["시각디자인학과", "음악과", "문예창작과", "영화영상학과", "연극영화과", "사진학과", "패션디자인과", "미술학과"],
    "S": ["교육학과", "사회복지학과", "심리학과", "유아교육과", "간호학과", "상담학과", "재활학과", "아동학과"],
    "E": ["경영학과", "광고홍보학과", "법학과", "행정학과", "국제통상학과", "무역학과", "경제학과", "부동산학과"],
    "C": ["회계학과", "경영정보학과", "금융학과", "세무학과", "문헌정보학과", "사무행정학과", "통계학과", "경제학과"]
}


# ============================================================
# 유틸리티 함수
# ============================================================

def initialize_session_state():
    """세션 스테이트 초기화"""
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0


def calculate_scores(answers):
    """
    RIASEC 점수 계산
    
    Args:
        answers (dict): {문항번호: 점수} 형태의 딕셔너리
    
    Returns:
        dict: {유형: 점수} 형태의 딕셔너리
    """
    scores = {riasec_type: 0 for riasec_type in RIASEC_INFO.keys()}
    
    question_num = 0
    for riasec_type, questions in QUESTIONS.items():
        for _ in questions:
            if question_num in answers:
                # answers에 None이 저장될 수 있으므로 확인
                if answers[question_num] is not None:
                    scores[riasec_type] += answers[question_num]
            question_num += 1
    
    return scores


def get_top_types(scores, n=3):
    """
    상위 N개 유형 반환
    
    Args:
        scores (dict): RIASEC 점수
        n (int): 반환할 상위 유형 개수
    
    Returns:
        list: 상위 유형 리스트
    """
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [riasec_type for riasec_type, score in sorted_types[:n]]


def create_radar_chart(scores):
    """레이더 차트 생성"""
    categories = [RIASEC_INFO[t]["name"] for t in scores.keys()]
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='내 점수',
        line_color='#1f77b4'
    ))
    
    # 차트의 최댓값을 0점이 아닐 경우에만 여유있게 설정
    max_val = max(values) if values else 0
    range_max = max(max_val * 1.2, 5) # 최소 5점 척도
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, range_max]
            )
        ),
        showlegend=False,
        height=400
    )
    
    return fig


# ============================================================
# 페이지 함수
# ============================================================

def show_intro_page():
    """소개 페이지"""
    st.title("🎯 RIASEC 진로탐색 검사")
    
    st.markdown("""
    ### 환영합니다! 👋
    
    이 검사는 **홀랜드(Holland)의 RIASEC 이론**을 기반으로 당신의 흥미와 적성을 파악하여 
    맞춤형 직업과 학과를 추천해드립니다.
    
    #### 📋 검사 정보
    - **문항 수**: 48개 문항
    - **소요 시간**: 약 10-15분
    - **응답 방식**: 5점 척도 (전혀 그렇지 않다 ~ 매우 그렇다)
    
    #### 🔤 RIASEC 유형
    """)
    
    cols = st.columns(3)
    types_list = list(RIASEC_INFO.items())
    
    for idx, (riasec_type, info) in enumerate(types_list):
        with cols[idx % 3]:
            st.markdown(f"""
            **{info['name']}** {info['description']}
            """)
    
    st.markdown("---")
    
    if st.button("검사 시작하기 🚀", type="primary", use_container_width=True):
        st.session_state.page = 'test'
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.rerun()


def show_test_page():
    """검사 페이지"""
    total_questions = sum(len(questions) for questions in QUESTIONS.values())
    current_q = st.session_state.current_question
    
    # 답변 완료된 개수로 진행률 표시
    answered_count = len([ans for ans in st.session_state.answers.values() if ans is not None])
    progress = answered_count / total_questions
    
    st.progress(progress)
    st.caption(f"진행률: {answered_count}/{total_questions} ({int(progress * 100)}%)")
    
    # 현재 문항의 유형과 문항 찾기
    question_num = 0
    current_type = None
    current_question_text = None
    
    for riasec_type, questions in QUESTIONS.items():
        for question_text in questions:
            if question_num == current_q:
                current_type = riasec_type
                current_question_text = question_text
                break
            question_num += 1
        if current_type:
            break
    
    # 문항 표시
    st.markdown(f"### 문항 {current_q + 1}")
    st.markdown(f"**유형: {RIASEC_INFO[current_type]['name']}**")
    st.markdown(f"#### {current_question_text}")
    
    # 응답 선택
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 이전에 답변한 기록이 있는지 확인
        previous_answer = st.session_state.answers.get(current_q)
        
        # 기록이 있으면 해당 답변의 index를, 없으면 None (선택 안 함)으로 설정
        default_index = None
        if previous_answer is not None:
            default_index = previous_answer - 1 # options가 [1, 2, 3, 4, 5]이므로
        
        answer = st.radio(
            "응답을 선택해주세요",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"][x-1],
            key=f"q_{current_q}",
            horizontal=False,
            index=default_index
        )
        
        st.markdown("---")
        
        col_prev, col_next = st.columns(2)
        
        with col_prev:
            if current_q > 0:
                if st.button("⬅️ 이전", use_container_width=True):
                    # "이전" 버튼은 현재 답을 저장하지 않고 페이지만 이동
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col_next:
            button_label = "다음 ➡️" if current_q < total_questions - 1 else "결과 보기 ✅"
            if st.button(button_label, type="primary", use_container_width=True):
                
                # 답변을 선택했는지 확인
                if answer is None:
                    st.warning("응답을 선택해주세요!", icon="⚠️")
                else:
                    # 답변 저장
                    st.session_state.answers[current_q] = answer
                    
                    if current_q < total_questions - 1: # 다음 질문이 있다면
                        st.session_state.current_question += 1
                        st.rerun()
                    else: # 마지막 질문이라면
                        # 모든 답변이 완료되었는지 최종 확인
                        answered_count = len([ans for ans in st.session_state.answers.values() if ans is not None])
                        if answered_count == total_questions:
                            st.session_state.page = 'result'
                            st.rerun()
                        else:
                            st.error(f"아직 답변하지 않은 문항이 {total_questions - answered_count}개 있습니다. '이전' 버튼으로 확인해주세요.", icon="🚨")



def show_result_page():
    """결과 페이지"""
    st.title("🎉 검사 결과")
    
    # 점수 계산
    scores = calculate_scores(st.session_state.answers)
    top_types = get_top_types(scores, 3)
    
    # 결과 요약
    st.markdown("### 📊 당신의 RIASEC 유형")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, riasec_type in enumerate(top_types):
        with [col1, col2, col3][idx]:
            st.metric(
                label=f"{idx + 1}순위",
                value=RIASEC_INFO[riasec_type]["name"],
                delta=f"{scores[riasec_type]}점"
            )
    
    # 레이더 차트
    st.markdown("### 📈 전체 유형별 점수")
    fig = create_radar_chart(scores)
    st.plotly_chart(fig, use_container_width=True)
    
    # 상위 유형 상세 설명
    st.markdown("### 🔍 당신의 주요 유형 분석")
    
    for idx, riasec_type in enumerate(top_types):
        with st.expander(f"**{idx + 1}. {RIASEC_INFO[riasec_type]['name']}** ({scores[riasec_type]}점)", expanded=(idx == 0)):
            st.markdown(f"**특징:** {RIASEC_INFO[riasec_type]['description']}")
            st.markdown(f"**주요 특성:** {RIASEC_INFO[riasec_type]['characteristics']}")
    
    # 추천 직업
    st.markdown("### 💼 추천 직업")
    
    for idx, riasec_type in enumerate(top_types):
        st.markdown(f"**{RIASEC_INFO[riasec_type]['name']} 관련 직업**")
        jobs = JOBS_DATA[riasec_type]
        cols = st.columns(4)
        for i, job in enumerate(jobs):
            with cols[i % 4]:
                st.info(job)

    st.write("") # 버튼 위에 약간의 여백 추가
    st.link_button(
        label="직업 정보 및 더 많은 직업 살펴보기 🖱️", 
        url="https://www.career.go.kr/cloud/w/job/list", # 직업 정보 링크
        use_container_width=True
    )
    # ============================================

    st.markdown("---") # 섹션 구분선
    # ============================================

    # 추천 학과
    st.markdown("### 🎓 추천 학과")
    
    for idx, riasec_type in enumerate(top_types):
        st.markdown(f"**{RIASEC_INFO[riasec_type]['name']} 관련 학과**")
        majors = MAJORS_DATA[riasec_type]
        cols = st.columns(4)
        for i, major in enumerate(majors):
            with cols[i % 4]:
                st.success(major)

    st.write("") # 버튼 위에 약간의 여백 추가
    st.link_button(
        label="학과 정보 및 더 많은 학과 살펴보기 🖱️", 
        url="https://www.career.go.kr/cloud/w/major/uList", # 학과 정보 링크
        use_container_width=True
    )
    
    # 다시하기 버튼
    st.markdown("---")
    if st.button("🔄 검사 다시하기", use_container_width=True):
        st.session_state.page = 'intro'
        st.session_state.answers = {}
        st.session_state.current_question = 0
        st.rerun()
# ===================================================


# ============================================================
# 메인 실행
# ============================================================

def main():
    """메인 함수"""
    initialize_session_state()
    
    # 페이지 라우팅
    if st.session_state.page == 'intro':
        show_intro_page()
    elif st.session_state.page == 'test':
        show_test_page()
    elif st.session_state.page == 'result':
        show_result_page()


main()