# -*- coding: utf-8 -*-
"""
Streamlit 메인 UI 구동 파일
자막 파일(SRT)과 대본(TXT)을 업로드받아 최신 3분할 교차 검수 뷰어를 렌더링합니다.
"""
import streamlit as st
import subtitle_engine as engine

st.set_page_config(page_title="자막 3분할 교차 검수 시스템", layout="wide")

st.title("🎬 Hackers Campus 법정의무교육 자막 검수 시스템")
st.caption("문장 단위 자동 병합 및 영미권 표준 어휘/고유명사 실시간 매핑 검수 인프라")

# 사이드바 설정 영역
st.sidebar.header("📁 데이터 업로드")
srt_file = st.sidebar.file_uploader("1. SRT 자막 파일 업로드", type=["srt"])
script_file = st.sidebar.file_uploader("2. 원고 대본 파일 업로드 (선택)", type=["txt"])

srt_content = ""
script_content = ""

if srt_file:
    srt_content = srt_file.read().decode("utf-8", errors="ignore")
if script_file:
    script_content = script_file.read().decode("utf-8", errors="ignore")

if st.sidebar.button("🚀 분석 및 번역 시작", type="primary"):
    if not srt_content:
        st.error("먼저 SRT 자막 파일을 업로드해 주세요!")
    else:
        with st.spinner("AI 분산 가속 엔진이 문맥 번역 및 고유명사 교차 추출을 수행 중입니다..."):
            # 자막 처리 엔진 구동
            result = engine.process_subtitles(srt_content, script_content)
            
            if result.merged_count == 0:
                st.warning("자막을 파싱하지 못했습니다. 파일 구조를 확인해 주세요.")
            else:
                st.success(f"분석 완료! 원본 {result.original_count}개 블록을 문장형 {result.merged_count}개 블록으로 최적화했습니다.")
                
                # HTML 뷰어 렌더링 (보안 정책 우회형 통합 리포트 내장)
                st.components.html(result.review_html, height=800, scrolling=True)
                
                # 다운로드 버튼 제공
                st.sidebar.markdown("---")
                st.sidebar.header("📥 결과물 다운로드")
                st.sidebar.download_button(
                    label="🇺🇸 영문 번역 SRT 다운로드",
                    data=result.translated_en_srt,
                    file_name="translated_english.srt",
                    mime="text/srt"
                )
                st.sidebar.download_button(
                    label="🇰🇷 문장 병합본 SRT 다운로드",
                    data=result.merged_ko_srt,
                    file_name="merged_korean.srt",
                    mime="text/srt"
                )
else:
    st.info("← 왼쪽 사이드바에 자막과 원고를 넣고 [분석 및 번역 시작] 버튼을 눌러주세요.")
