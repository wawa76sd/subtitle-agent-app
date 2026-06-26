# -*- coding: utf-8 -*-
"""
사용자님이 가장 좋아하시던 3분할 에이전트 UI를 완벽하게 구동하고,
내부 구문 오류(SyntaxError)를 완벽하게 해결한 메인 구동 파일
"""
import streamlit as st
import subtitle_engine as engine

st.set_page_config(page_title="자막 3분할 실시간 교차 검수 리포트", layout="wide")

st.title("🎬 자막 3분할 실시간 교차 검수 리포트")
st.caption("문장 단위 자동 병합 및 포괄적 실시간 무료 AI 문맥 번역 시스템")

st.sidebar.markdown("### 📁 검수용 데이터 소스 업로드")
srt_file = st.sidebar.file_uploader("1. SRT 자막 파일 (.srt)", type=["srt"])
script_file = st.sidebar.file_uploader("2. 원고 대본 파일 (.txt) [선택]", type=["txt"])

srt_content = ""
script_content = ""

if srt_file:
    srt_content = srt_file.read().decode("utf-8", errors="ignore")
if script_file:
    script_content = script_file.read().decode("utf-8", errors="ignore")

if st.sidebar.button("🚀 포괄적 교차 분석 시작", type="primary"):
    if not srt_content:
        st.sidebar.error("SRT 자막 파일을 반드시 먼저 업로드해 주세요!")
    else:
        with st.spinner("AI 분산 가속 번역 인프라 구동 중..."):
            result = engine.process_subtitles(srt_content, script_content)
            
            if result.merged_count == 0:
                st.error("자막 구조를 해석하지 못했습니다. SRT 규격을 확인해 주세요.")
            else:
                st.balloons()
                # 💡 3개 화면 에이전트 레이아웃이 포함된 결과창을 안전하게 렌더링합니다.
                st.components.html(result.review_html, height=850, scrolling=True)
                
                st.sidebar.markdown("---")
                st.sidebar.markdown("### 📥 마감 파일 다운로드")
                st.sidebar.download_button(
                    label="🇺🇸 영문 자막 (.srt) 받기",
                    data=result.translated_en_srt,
                    file_name="translated_english.srt",
                    mime="text/srt"
                )
                st.sidebar.download_button(
                    label="🇰🇷 한국어 병합본 (.srt) 받기",
                    data=result.merged_ko_srt,
                    file_name="merged_korean.srt",
                    mime="text/srt"
                )
