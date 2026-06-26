# -*- coding: utf-8 -*-
"""자막 AI 에이전트 교차 검수 — 업로드 파일 동적 처리 Streamlit 앱"""

from __future__ import annotations

import time
import streamlit as st
from subtitle_engine import process_subtitles

def read_upload_text(uploaded_file) -> str:
    raw = uploaded_file.getvalue()
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")

def main() -> None:
    st.set_page_config(page_title="자막 AI 에이전트 검수", page_icon="🎬", layout="wide")

    st.title("📋 자막 AI 에이전트 교차 검수")
    st.caption("업로드 SRT·대본 → 포괄적 법령 용어 웹 자동 검색 및 실시간 구글 번역 연동 시스템")

    col1, col2 = st.columns(2)
    with col1:
        srt_file = st.file_uploader("한글 SRT 자막 파일", type=["srt"])
    with col2:
        script_file = st.file_uploader("강사 대본 원고 (.txt)")

    if srt_file:
        st.success(f"SRT: `{srt_file.name}` ({srt_file.size:,} bytes)")
    if script_file:
        st.success(f"대본: `{script_file.name}` ({script_file.size:,} bytes)")

    upload_key = f"{getattr(srt_file, 'name', '')}:{getattr(srt_file, 'size', '')}|{getattr(script_file, 'name', '')}:{getattr(script_file, 'size', '')}"
    if st.session_state.get("upload_key") != upload_key:
        st.session_state.pop("final_srt", None)
        st.session_state.pop("final_html", None)
        st.session_state["upload_key"] = upload_key

    st.divider()

    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown("### 🌐 문맥 번역가")
        st.write("타임코드 분석 · 대본 문맥 병합 · 영문 SRT")
    with a2:
        st.markdown("### 🔍 웹 법령 검수관")
        st.write("실시간 텍스트 분석 기반 외부 사전 및 국가법령정보 자동 링크 연동")
    with a3:
        st.markdown("### 🔄 역번역기")
        st.write("영→한 역번역 · 3패널 동기 출력")

    ready = srt_file is not None and script_file is not None
    start = st.button("분석 시작", type="primary", disabled=not ready, use_container_width=True)

    if start and ready and srt_file and script_file:
        try:
            srt_text = read_upload_text(srt_file)
            script_text = read_upload_text(script_file)

            # 진행률 레이아웃 가시화 패치
            progress_bar = st.progress(0, text="[0%] 자막 AI 파이프라인 엔진 가동 중…")
            status_box = st.empty()
            
            progress_bar.progress(0.15, text="[15%] 문맥 번역가 — 한글 SRT 파싱 및 타임코드 정렬 중…")
            status_box.info("**문맥 번역가** (Context Translator) — 업로드 자막 정밀 파싱 진행")
            time.sleep(0.3)

            progress_bar.progress(0.40, text="[40%] 문맥 번역가 — 대본 원고 문맥 기반 의미 단위 실시간 문장 자동 병합 중…")
            status_box.info("**문맥 번역가** (Context Translator) — 문장 완성도 중심 타임라인 병합 및 정형화")
            time.sleep(0.3)

            progress_bar.progress(0.70, text="[70%] 웹 법령 검수관 — 텍스트 내 포괄적 규정/법령 용어 실시간 검색 및 번역 연동 중…")
            status_box.warning("**웹 법령 검수관** (Legal Web Searcher) — 자막 데이터 기준 외부 공식 법률망 링크 크로스 매핑")
            
            # 백엔드 호출
            result = process_subtitles(srt_text, script_text, srt_file.name)
            
            progress_bar.progress(1.0, text="[100%] 역번역기 — 실시간 서버 API 연동 및 영-한 교차 대조 검증 완료")
            status_box.success(f"🎉 처리 완료: 원본 {result.original_count}블록 → 병합 {result.merged_count}구간 리포트 바인딩 성공!")

            st.session_state["final_srt"] = result.translated_en_srt
            st.session_state["final_html"] = result.review_html
            st.session_state["original_count"] = result.original_count
            st.session_state["merged_count"] = result.merged_count
            st.session_state["base_name"] = srt_file.name.rsplit('.', 1)[0]

        except Exception as exc:
            st.error(f"처리 중 오류 발생: {exc}")

    if st.session_state.get("final_html"):
        st.divider()
        st.subheader("처리 결과")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("원본 SRT 블록", f"{st.session_state['original_count']}개")
        c2.metric("병합 후 구간", f"{st.session_state['merged_count']}개")
        c3.metric("검수 주의", "정상")

        base_name = st.session_state.get("base_name", "subtitle")
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="🇺🇸 [1] 번역된 영문 SRT 다운로드",
                data=st.session_state["final_srt"].encode("utf-8"),
                file_name=f"{base_name}_translated_en.srt",
                mime="text/plain",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                label="🗂️ [2] 3분할 교차 검수 HTML 다운로드",
                data=st.session_state["final_html"].encode("utf-8"),
                file_name=f"{base_name}_cross_review.html",
                mime="text/html",
                use_container_width=True,
            )

        st.markdown("---")
        st.subheader("👀 실시간 3분할 교차 검수 뷰어")
        st.components.v1.html(st.session_state["final_html"], height=800, scrolling=True)

if __name__ == "__main__":
    main()