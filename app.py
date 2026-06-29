# -*- coding: utf-8 -*-
"""
'🤖 AI 에이전트 자막 교차 검수 시스템'
기존 오리지널 UI 레이아웃을 100% 유지하면서,
다운로드 버튼 클릭 시 화면 리셋(Rerun) 버그만 세션 상태로 완벽 해결한 최종 마스터 UI
"""
import streamlit as st
import subtitle_engine as engine
import time

st.set_page_config(page_title="자막 교차 검수 시스템", layout="wide")

st.markdown("""
    <style>
    .agent-box { background-color: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; height: 100%; }
    .agent-title { font-size: 15px; font-weight: bold; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    .agent-desc { font-size: 12.5px; color: #94a3b8; line-height: 1.6; margin-bottom: 12px; word-break: keep-all; }
    .agent-badge { background-color: #0f172a; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-family: monospace; color: #3b82f6; border: 1px solid #1e293b; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI 자막 번역&교차 검수 시스템")
st.caption("이러닝 자막의 문장 구조 복원 및 다국어 번역 데이터 무결성 검수 가속화 도구")

st.markdown("### 📁 검수 대상 파일 업로드")
col_file1, col_file2 = st.columns(2)

with col_file1:
    srt_file = st.file_uploader("1. SRT 자막 파일 (.srt) [필수]", type=["srt"])
with col_file2:
    script_file = st.file_uploader("2. 원고 대본 파일 (.txt) [선택]", type=["txt"])

srt_content = ""
script_content = ""

if srt_file:
    srt_content = srt_file.read().decode("utf-8", errors="ignore")
if script_file:
    script_content = script_file.read().decode("utf-8", errors="ignore")

st.markdown("---")

st.markdown("### ⚙️ 자막 프로세싱 핵심 처리 단계")
col_agt1, col_agt2, col_agt3 = st.columns(3)

with col_agt1:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #60a5fa;">🇰🇷 1. 한글 문장 구조 복원</div>
        <div class="agent-desc">
            시간 단위로 짧게 쪼개진 자막 어절들을 구두점과 문맥 단락 기준으로 분석하여 <b>하나의 완결된 문장 형태로 자연스럽게 결합</b>합니다. 대본 매핑을 통해 싱크의 정확도를 보정합니다.
        </div>
        <span class="agent-badge">문장 단위 결합 알고리즘</span>
    </div>
    """, unsafe_allow_html=True)

with col_agt2:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #34d399;">🇺🇸 2. 영문 문맥 번역 및 의역</div>
        <div class="agent-desc">
            복원된 문장을 바탕으로 단어 기계 직역을 차단하고 전체 문맥을 파악해 번역합니다. <b>강좌명 및 강사 정보 등 주요 도메인 정보가 비즈니스 표준 표현으로 자동 치환</b>됩니다.
        </div>
        <span class="agent-badge">콘텐츠 맞춤형 번역</span>
    </div>
    """, unsafe_allow_html=True)

with col_agt3:
    st.markdown("""
    <div class="agent-box">
        <div class="agent-title" style="color: #fb7185;">🔄 3. 번역 무결성 역번역 검증</div>
        <div class="agent-desc">
            생성된 영문 자막을 다시 한국어로 역번역하여 원문 한글 자막과 대조합니다. <b>의미가 변질되거나 누락된 구간이 없는지 독립적으로 2차 필터링</b>을 수행하여 번역 무결성을 확보합니다.
        </div>
        <span class="agent-badge">양방향 의미론적 검증</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 💡 [버그 예방 방어막] 세션 상태 기저 저장소 선언
if 'analysis_result' not in st.session_state:
    st.session_state['analysis_result'] = None

if st.button("🚀 자막 분석 및 교차 검수", type="primary", use_container_width=True):
    if not srt_content:
        st.error("SRT 자막 파일을 먼저 업로드해 주세요!")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("### ⏳ [1/3] 한글 문장 병합 프로세스 분석 중...")
        progress_bar.progress(33)
        time.sleep(0.4)
        
        status_text.markdown("### ⏳ [2/3] 도메인 표준 가이드라인 기반 영문 번역 중...")
        progress_bar.progress(66)
        time.sleep(0.4)
        
        status_text.markdown("### ⏳ [3/3] 데이터 역번역 검증 및 HTML 리포트 빌드 중...")
        progress_bar.progress(95)
        
        # 분석 결과를 세션 상태 저장소에 영구 박제
        st.session_state['analysis_result'] = engine.process_subtitles(srt_content, script_content)
        
        progress_bar.progress(100)
        status_text.empty() # 로딩 텍스트 깔끔히 정리

# 💡 [리셋 방지 코어] 세션에 분석 완료 결과가 존재한다면 새로고침 후에도 UI 창 무조건 고정 출력
if st.session_state['analysis_result'] is not None:
    result = st.session_state['analysis_result']
    
    # 초록색 성공 배너와 알림 배너 복원
    st.success("📊 분석 완료! 통합 검수 리포트가 하단에 출력되었습니다.")
    st.info("💡 **안내:** 규격 가이드라인에 따라 강좌명이 `[The Statutory Compliance Manual: Prevention of Workplace Harassment]` 규격으로 안전하게 바인딩되었습니다.")
    
    st.markdown("### 📥 결과물 다운로드")
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        st.download_button(
            label="🇺🇸 영문 번역 완료 자막 (.srt) 다운로드",
            data=result.translated_en_srt,
            file_name="translated_english.srt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        st.download_button(
            label="🇰🇷 한국어 문장 병합 자막 (.srt) 다운로드",
            data=result.merged_ko_srt,
            file_name="merged_korean.srt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl3:
        st.download_button(
            label="🌐 HTML 통합 검수 리포트 저장",
            data=result.review_html,
            file_name="subtitles_review_report.html",
            mime="text/html",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### 🔍 자막 교차 검수 모니터")
    st.components.v1.html(result.review_html, height=850, scrolling=True)
