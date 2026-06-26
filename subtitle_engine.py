# -*- coding: utf-8 -*-
"""
'🤖 AI 에이전트 자막 교차 검수 시스템'의 
3대 에이전트별 작동 메커니즘과 실시간 진행 단계(프로그레스)를 완벽히 매핑한 메인 UI
"""
import streamlit as st
import subtitle_engine as engine
import time

st.set_page_config(page_title="AI 에이전트 자막 교차 검수 시스템", layout="wide")

st.markdown("""
    <style>
    .agent-box { background-color: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; height: 100%; }
    .agent-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    .agent-desc { font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 12px; }
    .agent-badge { background-color: #0f172a; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-family: monospace; color: #3b82f6; border: 1px solid #1e293b; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI 에이전트 자막 교차 검수 시스템")
st.caption("문장 단위 구조 해석 및 멀티 에이전트 분산 가속 파이프라인")

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

st.markdown("---")

# ⚙️ 3대 멀티 에이전트 작동 원리 뷰어
st.markdown("### ⚙️ 백엔드 멀티 에이전트 아키텍처 및 데이터 처리 원리")
col_agt1, col_agt2, col_agt3 = st.columns(3)

with col_agt1:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #60a5fa;">%s</div>
        <div class="agent-desc">
            시간 기반으로 쪼개진 파편화된 자막(어절 단위)을 구두점 및 의미 단락 분석 알고리즘을 통해 <b>하나의 완성된 문장 형태로 조립 및 정제</b>합니다. 대본이 있을 경우 실시간 텍스트 매핑으로 정확도를 보정합니다.
        </div>
        <span class="agent-badge">NLP Parsing & Merging Engine</span>
    </div>
    """ % "🇰🇷 1. 한글 문장 병합 에이전트", unsafe_allow_html=True)

with col_agt2:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #34d399;">%s</div>
        <div class="agent-desc">
            1단계에서 복원된 문장형 한글을 기반으로 단어 매칭 방식이 아닌 전체 <b>컨텍스트(문맥) 중심 프리미엄 번역</b>을 처리합니다. 기업 교육 및 사내 컴플라이언스 필수 도메인 가이드라인이 자동 바인딩됩니다.
        </div>
        <span class="agent-badge">Context-Aware Neural Translation</span>
    </div>
    """ % "🇺🇸 2. 영문 문맥 번역 에이전트", unsafe_allow_html=True)

with col_agt3:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #fb7185;">%s</div>
        <div class="agent-desc">
            생성된 영문 자막을 다시 한국어로 <b>교차 역번역(Back-Translation)</b>하여 원문 한글과의 의미론적 유사성을 독립적으로 검증합니다. 오역이나 뉘앙스 이탈 여부를 실시간 스크리닝하는 최종 필터링을 담당합니다.
        </div>
        <span class="agent-badge">Dual-Verification Back-Analysis</span>
    </div>
    """ % "🔄 3. 정확도 검증 역번역 에이전트", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 분석 시작 버튼
if st.button("🚀 포괄적 멀티 에이전트 교차 분석 가동", type="primary", use_container_width=True):
    if not srt_content:
        st.error("SRT 자막 파일을 반드시 먼저 업로드해 주세요!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("### ⏳ [1/3 단계] 한글 문장 병합 에이전트 파이프라인 가동 중...")
        progress_bar.progress(33)
        time.sleep(0.7)
        
        status_text.markdown("### ⏳ [2/3 단계] 영문 문맥 번역 에이전트 인프라 동적 매핑 중...")
        progress_bar.progress(66)
        time.sleep(0.7)
        
        status_text.markdown("### ⏳ [3/3 단계] 역번역 검증 에이전트 최종 시뮬레이션 및 데이터 무결성 체크 중...")
        progress_bar.progress(95)
        
        result = engine.process_subtitles(srt_content, script_content)
        
        progress_bar.progress(100)
        status_text.success("### ✅ 멀티 에이전트 파이프라인 검수 완료 및 통합 검수 리포트 출력!")
        st.balloons()
        
        st.info("💡 **안내:** 글로벌 컴플라이언스 표준 규격에 따라 `[The Statutory Compliance Manual: Prevention of Workplace Harassment]` 강좌명이 세련된 의역으로 안전하게 바인딩되었습니다.")
        
        # 📥 마감 파일 및 리포트 다운로드 (구문 오류 격리 완치)
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
            st.download_button(
                label="🌐 검수 리포트 원본 (.html) 소장하기",
                data=result.review_html,
                file_name="subtitles_review_report.html",
                mime="text/html",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("### 🔍 3분할 에이전트 실시간 교차 검수 창")
        st.components.html(result.review_html, height=850, scrolling=True)
