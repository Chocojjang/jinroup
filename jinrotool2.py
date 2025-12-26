"""
진로의사결정 검사 웹서비스
진로결정 수준, 하위요인, 의사결정 유형을 종합적으로 분석합니다.
"""

import streamlit as st
import plotly.graph_objects as go


# ============================================================
# 페이지 설정
# ============================================================
#st.set_page_config(
#    page_title="진로의사결정 검사",
#    page_icon="🎯",
#    layout="wide"
#)


# ============================================================
# 데이터 정의
# ============================================================

# 진로결정 수준 문항 (10문항)
DECISION_LEVEL_QUESTIONS = [
    {"text": "미래 진로에 대해 현실적이고 구체적인 방향성이 결정되어 있다", "reverse": False},
    {"text": "진로에 대한 결정을 내리지 못해 불안하고 답답하다", "reverse": True},
    {"text": "진로 방향을 정하지 못해 스트레스를 받는다", "reverse": True},
    {"text": "진로 선택에 대해 확신을 가지고 있다", "reverse": False},
    {"text": "진로를 결정했지만 불안감이 든다", "reverse": True},
    {"text": "진로 목표가 명확하게 설정되어 있다", "reverse": False},
    {"text": "진로 결정을 미루고 있다", "reverse": True},
    {"text": "선택한 진로에 대해 만족하고 편안하다", "reverse": False},
    {"text": "진로를 정하지 못해 조급한 마음이 든다", "reverse": True},
    {"text": "진로 방향에 대한 확신이 있다", "reverse": False}
]

# 하위요인 문항 (6개 요인 × 5문항 = 30문항)
SUBFACTOR_QUESTIONS = {
    "자기명확성부족": [
        "나의 적성과 흥미를 잘 모르겠다",
        "나에게 맞는 직업이 무엇인지 확신이 없다",
        "나의 강점과 약점을 명확히 파악하지 못했다",
        "나의 가치관과 목표가 불명확하다",
        "내 성격에 맞는 진로를 찾기 어렵다"
    ],
    "진로관련정보부족": [
        "다양한 직업에 대한 정보가 부족하다",
        "관심 분야의 직업 전망을 잘 모른다",
        "각 직업의 업무 내용을 구체적으로 알지 못한다",
        "진로 정보를 어디서 얻어야 할지 모르겠다",
        "직업별 필요한 자격이나 능력을 잘 모른다"
    ],
    "결단성부족": [
        "중요한 결정을 내리는 것이 어렵다",
        "여러 선택지 중 하나를 고르기가 힘들다",
        "결정을 내린 후에도 자주 후회한다",
        "결정을 미루고 회피하는 경향이 있다",
        "확신을 가지고 선택하는 것이 어렵다"
    ],
    "내적갈등": [
        "흥미와 적성이 서로 다른 것 같아 고민이다",
        "하고 싶은 일과 할 수 있는 일 사이에서 갈등한다",
        "여러 진로 중 무엇을 선택해야 할지 혼란스럽다",
        "이상과 현실 사이에서 갈등한다",
        "관심 분야가 너무 많아 선택하기 어렵다"
    ],
    "외적장애": [
        "경제적 여건 때문에 진로 선택이 제한적이다",
        "주변 사람들의 반대나 기대가 부담스럽다",
        "사회적 편견이나 차별이 걱정된다",
        "취업 시장의 불확실성이 두렵다",
        "진로 실현을 위한 자원이나 기회가 부족하다"
    ],
    "결정의필요성부족": [
        "당장 진로를 결정할 필요를 느끼지 못한다",
        "진로 문제에 대해 깊이 생각해본 적이 없다",
        "진로 결정을 서두를 필요가 없다고 생각한다",
        "진로에 대해 고민하는 것이 시간 낭비 같다",
        "나중에 생각해도 늦지 않다고 생각한다"
    ]
}

# 요인별 해결 방법 및 추천 검사
SOLUTION_GUIDE = {
    "자기명확성부족": {
        "description": "자신의 흥미, 적성, 가치관, 성격 등을 명확히 이해하지 못하여 진로 결정에 어려움을 겪고 있습니다.",
        "solutions": [
            "자기 탐색 활동을 통해 나의 흥미, 적성, 가치관을 파악하세요",
            "과거 경험을 되돌아보며 성취감을 느꼈던 순간들을 분석하세요",
            "다양한 활동을 시도하며 자신의 강점과 약점을 발견하세요",
            "진로 상담을 받아 전문가의 도움을 받으세요"
        ],
        "tests": [
            "🎯 Holland 직업흥미검사 (RIASEC) - 6가지 직업적 흥미 유형 파악",
            "🧩 다중지능검사 - 8가지 지능 영역의 강점 발견",
            "💎 직업가치관검사 - 직업 선택 시 중요하게 생각하는 가치 확인",
            "🎭 MBTI 성격유형검사 - 성격 특성과 맞는 직업 탐색"
        ]
    },
    "진로관련정보부족": {
        "description": "직업 세계, 교육 기회, 노동시장 등에 대한 정보가 부족하여 진로 결정이 어렵습니다.",
        "solutions": [
            "커리어넷, 워크넷 등 진로정보 사이트를 적극 활용하세요",
            "관심 직업의 종사자를 만나 직접 이야기를 들어보세요",
            "직업 체험 프로그램이나 인턴십에 참여하세요",
            "학과/전공 정보를 충분히 조사하고 비교하세요"
        ],
        "tests": [
            "📚 직업정보탐색검사 - 체계적인 직업 정보 수집 방법 학습",
            "🏢 직업카드분류검사 - 다양한 직업 탐색 및 선호도 파악",
            "🎓 학과 적합도 검사 - 관심 학과와 나의 적합도 확인",
            "💼 직무적성검사 - 특정 직무에 대한 적합도 평가"
        ]
    },
    "결단성부족": {
        "description": "우유부단하거나 결정에 대한 두려움이 있어 선택을 미루고 있습니다.",
        "solutions": [
            "작은 결정부터 스스로 내리는 연습을 시작하세요",
            "완벽한 선택은 없다는 것을 인정하세요",
            "결정의 장단점을 객관적으로 분석하는 습관을 기르세요",
            "결정 후 실행에 옮기는 연습을 하세요"
        ],
        "tests": [
            "🧠 의사결정유형검사 - 자신의 의사결정 패턴 이해",
            "💪 자기효능감검사 - 자신감 수준 파악 및 향상 방법 모색",
            "🎯 진로성숙도검사 - 진로 발달 수준 확인",
            "🔍 진로준비행동검사 - 구체적인 진로 준비 정도 평가"
        ]
    },
    "내적갈등": {
        "description": "흥미와 능력, 이상과 현실 사이의 불일치로 내적 갈등을 겪고 있습니다.",
        "solutions": [
            "갈등의 원인을 명확히 파악하고 우선순위를 정하세요",
            "장기 목표와 단기 목표를 구분하여 단계적으로 접근하세요",
            "양쪽을 모두 충족시킬 수 있는 대안을 창의적으로 찾아보세요",
            "전문 상담사와 함께 갈등을 해결하는 과정을 거치세요"
        ],
        "tests": [
            "⚖️ 진로갈등검사 - 갈등의 유형과 정도 파악",
            "🎯 직업흥미-능력 통합검사 - 흥미와 능력의 일치도 확인",
            "💭 진로사고검사 - 비합리적인 진로 사고 패턴 발견",
            "🌟 생애역할검사 - 삶의 다양한 역할 간 균형 탐색"
        ]
    },
    "외적장애": {
        "description": "경제적, 사회적, 환경적 제약으로 인해 진로 선택에 어려움을 겪고 있습니다.",
        "solutions": [
            "장애 요인을 명확히 파악하고 해결 가능한 것부터 시작하세요",
            "장학금, 학자금 대출 등 경제적 지원 제도를 알아보세요",
            "주변의 지지 체계를 확보하고 도움을 요청하세요",
            "현실적인 대안을 찾고 단계적인 목표를 설정하세요"
        ],
        "tests": [
            "🛡️ 진로장벽검사 - 구체적인 장애 요인 파악",
            "💪 진로탄력성검사 - 어려움 극복 능력 확인",
            "🤝 사회적지지검사 - 주변 지원 체계 평가",
            "📋 진로자원검사 - 활용 가능한 자원 파악"
        ]
    },
    "결정의필요성부족": {
        "description": "진로 결정의 중요성이나 시급성을 느끼지 못하여 진로 준비가 지연되고 있습니다.",
        "solutions": [
            "진로 결정이 나의 미래에 미치는 영향을 인식하세요",
            "또래 집단의 진로 준비 상황을 파악하고 비교해보세요",
            "구체적인 진로 목표와 실천 계획을 세우세요",
            "진로 결정을 미룰 때의 손실을 구체적으로 생각해보세요"
        ],
        "tests": [
            "📊 진로성숙도검사 - 진로 발달 단계 확인",
            "⏰ 진로계획성검사 - 진로 계획 수준 평가",
            "🎯 진로동기검사 - 진로 탐색 동기 수준 파악",
            "🚀 진로준비도검사 - 현재 진로 준비 상태 점검"
        ]
    }
}


# ============================================================
# 유틸리티 함수
# ============================================================

def initialize_session_state():
    """세션 스테이트 초기화"""
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'
    if 'test_phase' not in st.session_state:
        st.session_state.test_phase = 'decision_level'
    if 'answers' not in st.session_state:
        st.session_state.answers = {
            'decision_level': {},
            'subfactors': {}
        }
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0


def calculate_decision_level_score(answers):
    """진로결정 수준 점수 계산 (0-100점)"""
    total = 0
    for idx, answer in answers.items():
        question = DECISION_LEVEL_QUESTIONS[idx]
        if question['reverse']:
            total += (6 - answer)
        else:
            total += answer
    
    max_score = len(DECISION_LEVEL_QUESTIONS) * 5
    percentage = (total / max_score) * 100
    return round(percentage)


def get_decision_level_result(score):
    """진로결정 수준 결과 판정"""
    if 0 <= score <= 30:
        return "결정 X 편안", "#4CAF50"
    elif 31 <= score <= 50:
        return "결정 X 불편안", "#FF9800"
    elif 51 <= score <= 80:
        return "미결정 X 불편안", "#F44336"
    else:
        return "미결정 X 편안", "#2196F3"


def calculate_subfactor_scores(answers):
    """하위요인 점수 계산"""
    scores = {}
    for factor, questions in SUBFACTOR_QUESTIONS.items():
        total = sum(answers.get(f"{factor}_{i}", 0) for i in range(len(questions)))
        max_score = len(questions) * 5
        percentage = round((total / max_score) * 100)
        scores[factor] = percentage
    return scores


def categorize_subfactor_score(score):
    """하위요인 점수 구분"""
    if score >= 61:
        return "높음"
    elif score >= 40:
        return "보통"
    else:
        return "낮음"


def calculate_decision_type_scores(answers):
    """진로의사결정 유형 점수 계산 (사용 안 함)"""
    return {}


def create_decision_level_gauge(score):
    """진로결정 수준 게이지 차트"""
    level, color = get_decision_level_result(score)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "진로결정 수준"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "#E8F5E9"},
                {'range': [31, 50], 'color': "#FFF3E0"},
                {'range': [51, 80], 'color': "#FFEBEE"},
                {'range': [81, 100], 'color': "#E3F2FD"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig


def create_subfactor_chart(scores):
    """하위요인 막대 차트"""
    factors = list(scores.keys())
    values = list(scores.values())
    colors = ['#4CAF50' if v >= 61 else '#FFC107' if v >= 40 else '#F44336' for v in values]
    
    fig = go.Figure(data=[
        go.Bar(
            y=factors,
            x=values,
            orientation='h',
            marker=dict(color=colors),
            text=values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="하위요인 검사 결과",
        xaxis_title="점수",
        xaxis=dict(range=[0, 100]),
        height=400,
        showlegend=False
    )
    
    return fig


def create_decision_type_chart(scores):
    """의사결정 유형 차트"""
    types = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=types,
        y=values,
        marker_color=['#2196F3', '#FF5722', '#4CAF50'],
        text=values,
        textposition='outside'
    ))
    
    fig.update_layout(
        title="진로의사결정 유형",
        xaxis_title="유형",
        yaxis_title="점수",
        height=350,
        showlegend=False
    )
    
    return fig


# ============================================================
# 페이지 함수
# ============================================================

def show_intro_page():
    """소개 페이지"""
    st.title("🎯 진로의사결정 검사")
    
    st.markdown("""
    ### 환영합니다! 👋
    
    이 검사는 당신의 **진로결정 수준**과 **의사결정 유형**을 파악하여
    진로 발달을 위한 맞춤형 조언을 제공합니다.
    
    #### 📋 검사 구성
    
    1. **진로결정 수준 검사** (10문항)
       - 진로 방향 설정 정도와 심리적 안정감 평가
    
    2. **의사결정 방해요인 검사** (30문항)
       - 자기명확성 부족
       - 진로관련 정보부족
       - 결단성 부족
       - 내적갈등
       - 외적장애
       - 결정의 필요성 부족
    
    #### ⏱️ 소요 시간
    약 8-10분
    
    #### 📊 응답 방식
    4점 척도 (매우 아니다, 아니다, 그렇다, 매우 그렇다)
    """)
    
    st.info("💡 **Tip**: 정답은 없습니다. 평소 자신의 모습을 솔직하게 답해주세요!")
    
    st.markdown("---")
    
    if st.button("검사 시작하기 🚀", type="primary", use_container_width=True):
        st.session_state.page = 'test'
        st.session_state.test_phase = 'decision_level'
        st.session_state.current_question = 0
        st.rerun()


def show_test_page():
    """검사 페이지"""
    phase = st.session_state.test_phase
    current_q = st.session_state.current_question
    
    # 현재 단계에 따른 문항 설정
    if phase == 'decision_level':
        questions = DECISION_LEVEL_QUESTIONS
        total = len(questions)
        phase_name = "1단계: 진로결정 수준"
        answer_key = 'decision_level'
    else:  # subfactors
        all_questions = []
        for factor, qs in SUBFACTOR_QUESTIONS.items():
            for q in qs:
                all_questions.append((factor, q))
        questions = all_questions
        total = len(questions)
        phase_name = "2단계: 의사결정 방해요인"
        answer_key = 'subfactors'
    
    # 진행률
    progress = current_q / total
    st.progress(progress)
    st.caption(f"{phase_name} - {current_q}/{total} ({int(progress * 100)}%)")
    
    # 문항 표시
    st.markdown(f"### 문항 {current_q + 1}")
    
    if phase == 'decision_level':
        question_text = questions[current_q]['text']
        st.markdown(f"#### {question_text}")
    else:
        factor, question_text = questions[current_q]
        st.markdown(f"**[{factor}]**")
        st.markdown(f"#### {question_text}")
    
    # 응답 선택 - 이전에 답한 값이 있는지 확인
    if phase == 'decision_level':
        previous_answer = st.session_state.answers[answer_key].get(current_q)
    else:
        factor = questions[current_q][0]
        key = f"{factor}_{sum(1 for f, _ in questions[:current_q] if f == factor)}"
        previous_answer = st.session_state.answers[answer_key].get(key)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        answer = st.radio(
            "응답을 선택해주세요",
            options=[1, 2, 4, 5],
            format_func=lambda x: {1: "매우 아니다", 2: "아니다", 4: "그렇다", 5: "매우 그렇다"}[x],
            index=[1, 2, 4, 5].index(previous_answer) if previous_answer in [1, 2, 4, 5] else None,
            key=f"q_{phase}_{current_q}",
            horizontal=False
        )
        
        st.markdown("---")
        
        col_prev, col_next = st.columns(2)
        
        with col_prev:
            if current_q > 0:
                if st.button("⬅️ 이전", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col_next:
            is_last_question = current_q == total - 1
            is_last_phase = phase == 'subfactors'
            
            button_text = "결과 보기 ✅" if (is_last_question and is_last_phase) else "다음 ➡️"
            
            if st.button(button_text, type="primary", use_container_width=True):
                # 답변이 선택되었는지 확인
                if answer is None:
                    st.error("응답을 선택해주세요!")
                    st.stop()
                
                # 답변 저장
                if phase == 'decision_level':
                    st.session_state.answers['decision_level'][current_q] = answer
                else:  # subfactors
                    factor, _ = questions[current_q]
                    key = f"{factor}_{sum(1 for f, _ in questions[:current_q] if f == factor)}"
                    st.session_state.answers['subfactors'][key] = answer
                
                if is_last_question:
                    if phase == 'decision_level':
                        st.session_state.test_phase = 'subfactors'
                        st.session_state.current_question = 0
                    else:
                        st.session_state.page = 'result'
                else:
                    st.session_state.current_question += 1
                
                st.rerun()


def show_result_page():
    """결과 페이지"""
    st.title("🎉 검사 결과")
    
    # 1. 진로결정 수준
    st.markdown("## 1️⃣ 진로결정 수준")
    decision_score = calculate_decision_level_score(st.session_state.answers['decision_level'])
    level, color = get_decision_level_result(decision_score)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = create_decision_level_gauge(decision_score)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 검사 결과")
        st.metric("점수", f"{decision_score}점")
        st.markdown(f"**판정**: {level}")
        
        if level == "미결정 X 불편안":
            interpretation = "미래의 진로에 대해 현실적, 구체적인 방향성이 결정되어 있지 않고 진로 방향성의 견고한 정도가 낮습니다."
        elif level == "결정 X 불편안":
            interpretation = "또래 평균과 비교하여, 진로의사결정 수준은 평균 수준으로 결정하고 있습니다. 현재도 어느 정도 진로의사결정을 하고 있으나, 아래 능력 향상을 위한 노력이 조금 더 요구됩니다."
        elif level == "결정 X 편안":
            interpretation = "미래 진로에 대해 현실적, 구체적인 방향성이 결정되어 있습니다."
        else:
            interpretation = "미래 진로에 대해 현실적, 구체적인 방향성이 아직 결정되지 않았음을 의미합니다. 다양한 진로 관련 경험을 통해 자신에게 적절한 진로를 결정해나가는 과정이 필요합니다."
        
        st.info(interpretation)
    
    # 2. 하위요인 검사
    st.markdown("---")
    st.markdown("## 2️⃣ 의사결정 방해요인 분석")
    
    subfactor_scores = calculate_subfactor_scores(st.session_state.answers['subfactors'])
    
    fig = create_subfactor_chart(subfactor_scores)
    st.plotly_chart(fig, use_container_width=True)
    
    # 하위요인 상세 결과
    st.markdown("### 요인별 상세 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📌 정보 및 자기이해")
        for factor in ["자기명확성부족", "진로관련정보부족", "결단성부족"]:
            score = subfactor_scores[factor]
            category = categorize_subfactor_score(score)
            st.metric(factor, f"{score}점", delta=category)
    
    with col2:
        st.markdown("#### ⚡ 갈등 및 동기")
        for factor in ["내적갈등", "외적장애", "결정의필요성부족"]:
            score = subfactor_scores[factor]
            category = categorize_subfactor_score(score)
            st.metric(factor, f"{score}점", delta=category)
    
    # 3. 요인별 해결 방법 및 추천 검사
    st.markdown("---")
    st.markdown("## 3️⃣ 맞춤형 해결 방안")
    
    # 높은 점수(문제가 되는) 요인 찾기
    problem_factors = [(f, s) for f, s in subfactor_scores.items() if s >= 50]
    problem_factors.sort(key=lambda x: x[1], reverse=True)
    
    if problem_factors:
        st.info(f"💡 당신이 주로 겪고 있는 어려움은 **{len(problem_factors)}가지** 영역입니다. 각 영역별 해결 방법을 확인해보세요.")
        
        for factor, score in problem_factors:
            with st.expander(f"🔍 **{factor}** ({score}점) - 해결 방법 보기", expanded=(score == problem_factors[0][1])):
                guide = SOLUTION_GUIDE[factor]
                
                st.markdown(f"**📋 현재 상태**")
                st.write(guide['description'])
                
                st.markdown(f"**💡 해결 방법**")
                for idx, solution in enumerate(guide['solutions'], 1):
                    st.markdown(f"{idx}. {solution}")
                
                st.markdown(f"**🎯 추천 진로심리검사**")
                for test in guide['tests']:
                    st.success(test)
    else:
        st.success("🎉 모든 요인에서 양호한 수준을 보이고 있습니다! 지속적인 진로 탐색과 준비를 이어가세요.")
        
        # 점수가 낮은 요인도 안내
        st.markdown("### 💪 더 강화하면 좋은 영역")
        for factor, score in sorted(subfactor_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            with st.expander(f"**{factor}** ({score}점)"):
                guide = SOLUTION_GUIDE[factor]
                st.write(guide['description'])
                st.markdown("**추천 검사:**")
                for test in guide['tests'][:2]:
                    st.info(test)
    
    # 종합 의견
    st.markdown("---")
    st.markdown("## 💡 종합 의견 및 실천 계획")
    
    with st.expander("📝 검사 결과 해석 및 제언", expanded=True):
        st.markdown(f"""
        #### 진로결정 수준: {level} ({decision_score}점)
        
        당신의 진로결정 수준은 **{level}** 상태입니다. 
        
        #### 주요 발견사항
        
        **개선이 시급한 영역:**
        """)
        
        # 높은 점수 요인 (문제 영역)
        high_factors = [f for f, s in subfactor_scores.items() if s >= 61]
        if high_factors:
            for factor in high_factors:
                st.markdown(f"- ⚠️ {factor}: {subfactor_scores[factor]}점 - 우선적으로 해결 필요")
        
        st.markdown("""
        **보통 수준 영역:**
        """)
        
        # 보통 점수 요인
        medium_factors = [f for f, s in subfactor_scores.items() if 40 <= s < 61]
        if medium_factors:
            for factor in medium_factors:
                st.markdown(f"- ⚡ {factor}: {subfactor_scores[factor]}점 - 지속적인 관심 필요")
        
        st.markdown("""
        **양호한 영역:**
        """)
        
        # 낮은 점수 요인 (양호한 영역)
        low_factors = [f for f, s in subfactor_scores.items() if s < 40]
        if low_factors:
            for factor in low_factors:
                st.markdown(f"- ✅ {factor}: {subfactor_scores[factor]}점 - 이 부분은 잘 하고 있습니다")
        else:
            st.markdown("- 모든 영역에서 개선이 필요합니다. 하나씩 차근차근 해결해나가세요.")
        
        st.markdown(f"""
        
        #### 실천 계획 제안
        
        1. **단기 목표 (1개월)**
           - 가장 점수가 높은 요인부터 해결 시작
           - 추천 검사 중 1-2가지 실시
           - 진로 상담 예약하기
        
        2. **중기 목표 (3개월)**
           - 진로 정보 수집 및 직업 체험 활동
           - 자기 이해를 위한 지속적인 탐색
           - 진로 목표 구체화하기
        
        3. **장기 목표 (6개월)**
           - 진로 실행 계획 수립
           - 필요한 자격이나 역량 준비
           - 정기적인 진로 점검 및 조정
        """)
    
    # 추가 자원
    st.markdown("---")
    st.markdown("## 📚 유용한 진로 정보 사이트")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **커리어넷**
        www.career.go.kr
        - 직업·학과 정보
        - 진로심리검사
        - 진로상담
        """)
    
    with col2:
        st.info("""
        **워크넷**
        www.work.go.kr
        - 직업정보
        - 구인구직
        - 직업훈련정보
        """)
    
    with col3:
        st.info("""
        **중앙청년지원센터**
        www.nysc.or.kr
        - 청년 정책
        - 취업 지원
        - 교육 프로그램
        """)
    
    # 다시하기 버튼
    st.markdown("---")
    if st.button("🔄 검사 다시하기", use_container_width=True):
        st.session_state.page = 'intro'
        st.session_state.test_phase = 'decision_level'
        st.session_state.answers = {
            'decision_level': {},
            'subfactors': {},
            'decision_type': {}
        }
        st.session_state.current_question = 0
        st.rerun()


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