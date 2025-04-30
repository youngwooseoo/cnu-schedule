
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(layout="wide")
st.title("📘 충남대 시간표 추천 앱")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.sidebar.header("🛠️ 조건 설정")
    major = st.sidebar.selectbox("전공 선택", sorted(df["운영학과"].dropna().unique()))
    preferred_days_off = st.sidebar.multiselect("공강 원하는 요일", ["월", "화", "수", "목", "금"])
    preferred_mode = st.sidebar.radio("수업 형태", ["전체", "대면강의", "원격강의"])
    grading_type = st.sidebar.radio("평가 방식", ["전체", "상대평가", "절대평가"])

    # 필터링
    filtered = df[df["운영학과"] == major]
    if preferred_mode != "전체":
        filtered = filtered[filtered["수업형태"].astype(str).str.contains(preferred_mode)]
    if grading_type != "전체":
        filtered = filtered[filtered["성적평가방식"] == grading_type]
    if preferred_days_off:
        pattern = "|".join(preferred_days_off)
        filtered = filtered[~filtered["강의시간"].astype(str).str.contains(pattern)]

    st.success(f"🔍 총 {len(filtered)}개의 강의가 조건에 맞습니다.")
    st.dataframe(filtered)

    # 시간표 시각화 (간단 버전)
    st.subheader("🗓️ 시간표 시각화")
    fig, ax = plt.subplots(figsize=(10, 6))
    days = ["월", "화", "수", "목", "금"]
    ax.set_xlim(0, 5)
    ax.set_ylim(8, 20)
    ax.set_xticks(range(5))
    ax.set_xticklabels(days)
    ax.set_yticks(range(8, 21))
    ax.set_yticklabels([f"{h}:00" for h in range(8, 21)])
    ax.grid(True)

    for _, row in filtered.iterrows():
        if pd.isna(row["강의시간"]):
            continue
        entries = str(row["강의시간"]).split(",")
        for entry in entries:
            if len(entry) < 3:
                continue
            day = entry[0]
            try:
                time_range = entry[1:]
                start, end = time_range.split("~")
                start_h = int(start.split(":")[0])
                end_h = int(end.split(":")[0])
                x = days.index(day)
                ax.add_patch(patches.Rectangle((x, start_h), 0.95, end_h - start_h, color="skyblue", alpha=0.6))
                ax.text(x + 0.5, start_h + 0.5, row["과목명"], ha="center", va="center", fontsize=8)
            except:
                continue

    st.pyplot(fig)
else:
    st.info("⬅️ 왼쪽에서 CSV 파일을 업로드해주세요.")
