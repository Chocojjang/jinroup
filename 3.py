import streamlit as st
import folium
# from folium.plugins import MarkerCluster # (참고) 클러스터 기능은 현재 제거된 상태입니다.
from streamlit_folium import st_folium
import pandas as pd
import webbrowser # (참고) 서버 환경에서는 직접 사용되지 않습니다.

# --- 1. 데이터 로드 (캐시 사용으로 성능 향상) ---
@st.cache_data
def load_data(file_path):
    try:
        # 엑셀 파일 로드 시 dtype을 string으로 지정하여 URL 등이 숫자로 변환되는 것을 방지
        # (주의) '홈페이지주소 ' 컬럼명에 공백이 포함된 것을 확인하고 dtype에 반영
        return pd.read_excel(file_path, dtype={'홈페이지주소 ': str, '대학 및 입시정보': str})
    except FileNotFoundError:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 엑셀 파일이 코드와 같은 폴더에 있는지 확인하세요.")
        return None
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# (중요) 사용자가 업로드한 파일명 '대학원본.xlsx'로 수정
sb = load_data('대학원본.xlsx')

if sb is None:
    st.stop()

# --- 2. 초기값 및 세션 상태 설정 ---
DEFAULT_CENTER = [37.5665, 126.9780] # 서울 시청 중심
DEFAULT_ZOOM = 11

if 'selected_name' not in st.session_state:
    st.session_state.selected_name = None

# --- 3. 검색 기능 (지도보다 위로 이동) ---
st.divider() 
st.header("대학교 검색")

search_term = st.text_input(
    "대학명을 2글자 이상 입력하세요:",
    placeholder="예: 서울, 경북, 한양"
)

selected_name = None  

if len(search_term) >= 2:
    mask = sb['대학명'].str.contains(search_term, case=False, na=False)
    filtered_df = sb[mask]

    if not filtered_df.empty:
        university_names = filtered_df['대학명'].unique().tolist()
        
        st.write(f"'{search_term}' 검색 결과 (총 {len(university_names)}개):")
        
        col1, col2 = st.columns([3, 1]) 

        with col1:
            default_index = None
            if st.session_state.selected_name in university_names:
                default_index = university_names.index(st.session_state.selected_name)

            selected_name = st.selectbox(
                "selectbox_label", 
                options=university_names,
                index=default_index, 
                placeholder="목록에서 학교를 선택하세요.",
                label_visibility="collapsed" 
            )

        # --- [수정된 부분: 버튼 로직 변경 (Fallback 기능 추가)] ---
        with col2:
            current_selection = st.session_state.selected_name
            
            if current_selection:
                try:
                    school_data = sb[sb['대학명'] == current_selection].iloc[0]
                    url_info = school_data['대학 및 입시정보']
                    url_home = school_data['홈페이지주소 '] # (주의) 컬럼명에 공백 포함
                    
                    final_url = None
                    button_label = "정보 없음"
                    is_disabled = True
                    help_text = "선택된 학교의 정보 URL이 없습니다."

                    # 1. '대학 및 입시정보' URL 확인 (http로 시작하는지)
                    if not pd.isna(url_info) and str(url_info).strip().startswith('http'):
                        # 입시 정보 URL이 있음
                        final_url = str(url_info).strip()
                        button_label = "대학 및 입시정보"
                        is_disabled = False
                        help_text = f"{current_selection} 입시 정보로 이동합니다."
                    
                    # 2. (Fallback) '홈페이지주소 ' URL 확인 (단순히 비어있지 않은지)
                    elif not pd.isna(url_home) and str(url_home).strip(): # Check if not NaN and not an empty string
                        # 홈페이지 URL만 있음
                        home_url_stripped = str(url_home).strip()
                        
                        # http(s)://가 없으면 붙여줌
                        if not home_url_stripped.startswith('http'):
                            final_url = f"https://{home_url_stripped}"
                        else:
                            final_url = home_url_stripped
                            
                        button_label = "홈페이지" # 버튼 레이블 변경
                        is_disabled = False
                        help_text = f"{current_selection} 홈페이지로 이동합니다."
                    
                    # 3. 둘 다 유효한 URL이 없는 경우 (위의 if/elif를 통과 못함)
                    # final_url = None, button_label = "정보 없음" 등이 유지됨


                    # 4. 최종 URL 상태에 따라 버튼 표시
                    if final_url and not is_disabled:
                        st.link_button(
                            button_label, 
                            final_url,
                            use_container_width=True
                        )
                    else:
                        st.button(
                            button_label, 
                            use_container_width=True, 
                            disabled=True, 
                            help=help_text
                        )
                        
                except Exception as e:
                    st.button("정보 오류", use_container_width=True, disabled=True, help=f"정보 조회 오류: {e}")
            else:
                st.button(
                    "대학 및 입시정보", 
                    use_container_width=True, 
                    disabled=True,
                    help="먼저 검색 목록에서 학교를 선택하세요."
                )
        # --- [수정된 부분 끝] ---

        if selected_name != st.session_state.selected_name:
            st.session_state.selected_name = selected_name
            st.rerun() 
            
    else:
        st.warning("검색 결과가 없습니다.")
        if st.session_state.selected_name is not None:
            st.session_state.selected_name = None
            st.rerun()

elif len(search_term) == 1:
    st.info("검색어를 2글자 이상 입력해 주세요.(00대학교면 00을 입력)")
else:
    st.info("지도에서 학교명을 클릭하거나 검색창에 대학교 이름을 입력해 주세요.")
    if st.session_state.selected_name is not None:
        st.session_state.selected_name = None
        st.rerun()

# --- 4. 지도 표시 (검색 기능 아래로 이동) ---

if st.session_state.selected_name:
    school_data = sb[sb['대학명'] == st.session_state.selected_name].iloc[0]
    map_center = [school_data['위도'], school_data['경도']]
    map_zoom = 15 
else:
    map_center = DEFAULT_CENTER
    map_zoom = DEFAULT_ZOOM

m = folium.Map(location=map_center, zoom_start=map_zoom)

# 4-3. 마커 추가 (팝업 기능 추가)
for i in sb.index:
    name = sb.loc[i, '대학명']
    lat = sb.loc[i, '위도']
    lon = sb.loc[i, '경도']
    
    # --- [수정된 부분: 마커 클릭 시 URL 팝업 (Fallback 기능 추가)] ---
    # 1. 해당 학교의 URL 가져오기
    url_info = sb.loc[i, '대학 및 입시정보']
    url_home = sb.loc[i, '홈페이지주소 '] # (주의) 컬럼명에 공백 포함
    
    final_url = None
    link_text = "정보 링크 없음"
    
    # 2. URL 우선순위 결정
    # 2-1. '대학 및 입시정보' URL 확인 (http로 시작하는지)
    if not pd.isna(url_info) and str(url_info).strip().startswith('http'):
        final_url = str(url_info).strip()
        link_text = "대학 및 입시정보 열기"
    
    # 2-2. (Fallback) '홈페이지주소 ' URL 확인 (단순히 비어있지 않은지)
    elif not pd.isna(url_home) and str(url_home).strip():
        home_url_stripped = str(url_home).strip()
        
        # http(s)://가 없으면 붙여줌
        if not home_url_stripped.startswith('http'):
            final_url = f"https://{home_url_stripped}"
        else:
            final_url = home_url_stripped
            
        link_text = "홈페이지 열기" # 링크 텍스트 변경
    
    # 2-3. 둘 다 없으면 final_url = None, link_text = "정보 링크 없음" 유지

    # 3. 팝업창에 표시할 HTML 내용 생성
    popup_html = f"<b>{name}</b><br><hr>"
    if final_url:
        popup_html += f'<a href="{final_url}" target="_blank">{link_text}</a>'
    else:
        popup_html += link_text # "정보 링크 없음"
    
    # 4. Folium 팝업 객체 생성
    popup = folium.Popup(popup_html, max_width=300)
    # --- [수정된 부분 끝] ---

    is_selected = (name == st.session_state.selected_name)
    
    folium.Marker(
        [lat, lon],
        tooltip=name,
        popup=popup, 
        icon=folium.Icon(
            color='red' if is_selected else 'green', 
            icon='star'
        )
    ).add_to(m) 

# 4-4. 지도 표시
st_folium(m, width=1000, height=600, key="main_map")