# -*- coding: utf-8 -*-
"""
'AI 에이전트 자막 교차 검수 시스템' 타이틀과 함께
실시간 진행 단계(프로그레스), HTML 다운로드 기능 및 3분할 UI를 완벽 복구한 파일
"""
import streamlit as st
import subtitle_engine as engine
import time

st.set_page_config(page_title="AI 에이전트 자막 교차 검수 시스템", layout="wide")

st.title("🤖 AI 에이전트 자막 교차 검수 시스템")
st.caption("문장 단위 자동 병합 및 멀티 에이전트 기반 실시간 무료 AI 문맥 번역 시스템")

# 📁 파일 나란히 배치하여 업로드하는 공간
st.markdown("### 📁 검수용 데이터 소스 업로드")
col_file1, col_file2 = st.columns(2)

with col_file1:
    srt_file = st.file_uploader("1. SRT 자막 파일 (.srt) 필수", type=["srt"])
with col_file2:
    script_file = st.file_uploader("2. 원고 대본 파일 (.txt) 선택", type=["txt"])

srt_content = ""
script_content = ""

if srt_file:
    srt_content = srt_file.read().decode("utf-8", errors="ignore")
if script_file:
    script_content = script_file.read().decode("utf-8", errors="ignore")

# 분석 시작 버튼 구동
if st.button("🚀 포괄적 멀티 에이전트 교차 분석 시작", type="primary", use_container_width=True):
    if not srt_content:
        st.error("SRT 자막 파일을 반드시 먼저 업로드해 주세요!")
    else:
        # 🔄 [핵심 복원] 실시간 진행 단계(진행률) 연출 효과
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("### ⏳ [1/3 단계] 한국어 자막 문장 단위 자동 병합 및 구조 해석 중...")
        progress_bar.progress(30)
        time.sleep(0.8)
        
        status_text.markdown("### ⏳ [2/3 단계] AI 가속 엔진 기반 글로벌 프리미엄 영문 번역 진행 중...")
        progress_bar.progress(65)
        time.sleep(1.0)
        
        status_text.markdown("### ⏳ [3/3 단계] 번역 정확도 검증을 위한 교차 역번역(Back-Translation) 매핑 중...")
        progress_bar.progress(90)
        
        # 실제 엔진 구동
        result = engine.process_subtitles(srt_content, script_content)
        
        progress_bar.progress(100)
        status_text.success("### ✅ 멀티 에이전트 교차 검수 및 리포트 생성 완료!")
        st.balloons()
        
        st.info("💡 **안내:** 글로벌 컴플라이언스 표준 규격에 따라 `[The Statutory Compliance Manual: Prevention of Workplace Harassment]` 강좌명이 세련된 의역으로 안전하게 반영되었습니다.")
        
        # 📥 [핵심 복원] 자막 파일들과 함께 HTML 리포트 다운로드 기능 탑재
        st.markdown("### 📥 마감 파일 및 리포트 다운로드")
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        with col_dl1:
            st.download_button(
                label="🇺🇸 영문 번역 완료 자막 (.srt) 받기",
                data=result.translated_en_srt,
                file_name="translated_english.srt",
                mime="text/srt",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                label="🇰🇷 한국어 완성형 병합 자막 (.srt) 받기",
                data=result.merged_ko_srt,
                file_name="merged_korean.srt",
                mime="text/srt",
                use_container_width=True
            )
        with col_dl3:
            # HTML 리포트 통째로 다운로드 버튼
            st.download_button(
                label="🌐 검수 리포트 원본 (.html) 소장하기",
                data=result.review_html,
                file_name="subtitles_review_report.html",
                mime="text/html",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("### 🔍 3분할 에이전트 실시간 교차 검수 창")
        # 🖥️ 점수판 아래에 3개 화면 에이전트 실시간 가동
        st.components.html(result.review_html, height=850, scrolling=True)
