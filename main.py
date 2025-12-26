"""
진로탐색 통합 웹페이지
메인 페이지에서 각 기능으로 이동할 수 있습니다.
"""

import streamlit as st
import importlib.util
import sys
from pathlib import Path


# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="진로탐색 종합 플랫폼",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 스타일 설정
# ============================================================
st.markdown("""
<style>
    /* 상단 메뉴 스타일 */
    .main-menu {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    
    /* 홈 화면 스타일 */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
    }
    
    .hero-title {
        font-size: 3em;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-size: 1.5em;
        color: #666;
        margin-bottom: 40px;
    }
    
    /* 카드 스타일 */
    .card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
    
    .card-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .card-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    
    .card-description {
        color: #666;
        font-size: 1em;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 세션 스테이트 초기화
# ============================================================
def initialize_session_state():
    """세션 스테이트 초기화"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'


# ============================================================
# 외부 Python 파일 실행 함수
# ============================================================
def load_and_run_module(file_path, module_name):
    """
    외부 Python 파일을 동적으로 로드하고 실행
    
    Args:
        file_path (str): 실행할 Python 파일 경로
        module_name (str): 모듈 이름
    """
    try:
        # 파일 존재 확인
        if not Path(file_path).exists():
            st.error(f"⚠️ 파일을 찾을 수 없습니다: {file_path}")
            st.info("파일이 같은 폴더에 있는지 확인해주세요.")
            return
        
        # 모듈 로드
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
    except Exception as e:
        st.error(f"⚠️ 페이지 로드 중 오류가 발생했습니다: {str(e)}")
        st.info("파일 경로와 코드를 확인해주세요.")


# ============================================================
# 상단 메뉴
# ============================================================
def show_menu():
    """상단 메뉴 표시"""
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])
    
    with col1:
        if st.button("🏠 홈", use_container_width=True, type="primary" if st.session_state.current_page == 'home' else "secondary"):
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col2:
        if st.button("🎯 진로결정돕기", use_container_width=True, type="primary" if st.session_state.current_page == 'career_decision' else "secondary"):
            st.session_state.current_page = 'career_decision'
            st.rerun()
    
    with col3:
        if st.button("🎨 흥미와전공", use_container_width=True, type="primary" if st.session_state.current_page == 'riasec' else "secondary"):
            st.session_state.current_page = 'riasec'
            st.rerun()
    
    with col4:
        if st.button("📚 대학입시정보", use_container_width=True, type="primary" if st.session_state.current_page == 'university' else "secondary"):
            st.session_state.current_page = 'university'
            st.rerun()
    
    with col5:
        st.write("")
    
    st.markdown("---")


# ============================================================
# 홈 페이지
# ============================================================
def show_home_page():
    """홈 페이지"""
    # 히어로 섹션
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🎓 진로탐색 종합 플랫폼</div>
        <div class="hero-subtitle">당신의 꿈을 찾아가는 여정을 함께합니다</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 서비스 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🎯</div>
            <div class="card-title">진로결정돕기</div>
            <div class="card-description">
                진로 의사결정 수준을 파악하고<br>
                방해요인을 분석하여<br>
                맞춤형 해결책을 제시합니다
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("시작하기", key="btn1", use_container_width=True, type="primary"):
            st.session_state.current_page = 'career_decision'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🎨</div>
            <div class="card-title">흥미와전공</div>
            <div class="card-description">
                RIASEC 검사를 통해<br>
                당신의 직업적 흥미를 파악하고<br>
                관련 직업과 학과를 추천합니다
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("시작하기", key="btn2", use_container_width=True, type="primary"):
            st.session_state.current_page = 'riasec'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📚</div>
            <div class="card-title">대학입시정보</div>
            <div class="card-description">
                최신 대학 입시 정보와<br>
                전형 분석을 통해<br>
                합격 전략을 세워보세요
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("시작하기", key="btn3", use_container_width=True, type="primary"):
            st.session_state.current_page = 'university'
            st.rerun()
    
    # 추가 정보
    st.markdown("---")
    st.markdown("## 💡 이용 안내")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 진로결정돕기**
        - 소요시간: 약 8-10분
        - 문항수: 40문항
        - 결과: 의사결정 방해요인 분석 및 해결방안
        """)
        
        st.success("""
        **🎨 흥미와전공**
        - 소요시간: 약 10-15분
        - 문항수: 48문항
        - 결과: RIASEC 유형별 직업 및 학과 추천
        """)
    
    with col2:
        st.warning("""
        **📚 대학입시정보**
        - 최신 입시 정보 제공
        - 대학별 전형 분석
        - 합격 전략 수립
        """)
        
        st.info("""
        **📞 문의하기**
        - 이메일: career@example.com
        - 전화: 02-1234-5678
        - 운영시간: 평일 09:00-18:00
        """)


# ============================================================
# 메인 실행
# ============================================================
def main():
    """메인 함수"""
    initialize_session_state()
    
    # 상단 메뉴
    show_menu()
    
    # 페이지 라우팅
    if st.session_state.current_page == 'home':
        show_home_page()
    
    elif st.session_state.current_page == 'career_decision':
        st.title("🎯 진로결정돕기")
        st.markdown("---")
        
        # jinrotool2.py 실행
        load_and_run_module("jinrotool2.py", "jinrotool2")
    
    elif st.session_state.current_page == 'riasec':
        st.title("🎨 흥미와전공")
        st.markdown("---")
        
        # REASEC3.py 실행
        load_and_run_module("REASEC3.py", "riasec3")
    
    elif st.session_state.current_page == 'university':
        st.title("📚 대학입시정보")
        st.markdown("---")
        
        # 3.py 실행
        load_and_run_module("3.py", "university_info")


if __name__ == "__main__":
    main()