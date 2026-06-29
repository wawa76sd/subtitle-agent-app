# -*- coding: utf-8 -*-
import streamlit as st
import subtitle_engine as engine

# 1. 페이지 기본 설정 및 디자인 (최상단 배치)
st.set_page_config(
    page_title="인공지능 자막 번역 & 검수 매니저",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 타이틀 및 안내 멘트
st.title("🎬 스마트 자막 번역 및 실시간 교차 검수 시스템")
st.markdown("---")

# 3. 사이드바 - 파일 업로드 및 설정
st.sidebar.header("📁 데이터 업로드")
uploaded_srt = st.sidebar.file_uploader("1️⃣ 한글 오리지널 SRT 자막 파일 (.srt)", type=["srt"])
uploaded_script = st.sidebar.file_uploader("2️⃣ 강사 원고/대본 텍스트 파일 (.txt)", type=["txt"])

st.sidebar.markdown("---")
st.sidebar.markdown("💡 **Tip**: 두 파일을 모두 업로드한 뒤 아래 **[자막 처리 가동]** 버튼을 누르시면, 문장 단위로 싱크가 자동 병합되며 3분할 교차 검수 모니터가 우측에 나타납니다.")

# 4. 자막 처리 로직 가동 버튼
if uploaded_srt:
    st.success("✅ SRT 자막 파일이 성공적으로 로드되었습니다.")
    
    # 두 파일 내용 읽기
    srt_content = uploaded_srt.read().decode("utf-8", errors="ignore")
    script_content = ""
    if uploaded_script:
        script_content = uploaded_script.read().decode("utf-8", errors="ignore")
        st.success("✅ 원고 대본 파일이 연동되었습니다.")
    
    st.markdown("### ⚙️ 프로세싱 제어")
    if st.button("🚀 자막 처리 및 3대 에이전트 가동 (클릭)", type="primary"):
        with st.spinner("🤖 한글 싱크 병합, 영어 번역 및 역번역 복원을 정밀 수행 중입니다... (약 10~30초 소요)"):
            try:
                # 자막 엔진 호출
                result = engine.process_subtitles(srt_content, script_content)
                
                if result and result.segments:
                    st.balloons()
                    
                    # 통계 정보 출력
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("기존 개별 자막 줄 수", f"{result.original_count} 줄")
                    with col2:
                        st.metric("문장 단위 병합 자막 수", f"{result.merged_count} 문장")
                    
                    st.markdown("---")
                    
                    # 결과물 다운로드 섹션
                    st.markdown("### 💾 최종 결과물 다운로드")
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        st.download_button(
                            label="🇺🇸 최종 번역 영문 자막 다운로드 (.srt)",
                            data=result.translated_en_srt,
                            file_name="translated_english_final.srt",
                            mime="text/plain"
                        )
                    with d_col2:
                        st.download_button(
                            label="🇰🇷 싱크 병합 한글 자막 다운로드 (.srt)",
                            data=result.merged_ko_srt,
                            file_name="merged_korean_final.srt",
                            mime="text/plain"
                        )
                    
                    st.markdown("---")
                    
                    # 🖥️ 핵심: 3분할 교차 검수 모니터 화면 렌더링
                    st.markdown("### 🖥️ 실시간 교차 검수 모니터 모드")
                    st.components.v1.html(result.review_html, height=750, scrolling=True)
                else:
                    st.error("❌ 자막 파싱에 실패했거나 변환된 데이터가 없습니다. 파일 형식을 확인해 주세요.")
            except Exception as e:
                st.error(f"🚨 처리 중 예기치 못한 엔진 오류가 발생했습니다: {str(e)}")
else:
    st.info("👋 먼저 왼쪽 사이드바에서 검수할 한글 SRT 자막 파일을 업로드해 주세요.")
