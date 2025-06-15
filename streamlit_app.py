import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="진주시 CCTV & 가로등 시각화", layout="wide")
st.title("🎈 진주시 CCTV 및 가로등 설치 현황 시각화")
st.markdown("### 📊 읍면동/법정동 기준 CCTV 설치대수와 가로등 총등수를 비교합니다.")

# =====================
# 📁 데이터 불러오기
# =====================
df_cctv = pd.read_csv("jinju_cctv.csv", encoding='euc-kr')
df_street = pd.read_csv("jinju_street.csv", encoding='euc-kr')

# =====================
# 📊 CCTV 데이터 처리
# =====================
df_cctv = df_cctv[['읍면동', '설치대수']].copy()
df_cctv['읍면동'] = df_cctv['읍면동'].str.strip()
cctv_grouped = df_cctv.groupby('읍면동', as_index=False).sum()
cctv_grouped = cctv_grouped.sort_values(by='읍면동')

# =====================
# 💡 가로등 데이터 처리
# =====================
df_street = df_street[['법정동', '총등수']].copy()
df_street['법정동'] = df_street['법정동'].str.strip()
street_grouped = df_street.groupby('법정동', as_index=False).sum()
street_grouped = street_grouped.sort_values(by='법정동')

# =====================
# 📍 CCTV 단독 그래프
# =====================
st.subheader("📍 읍면동별 CCTV 설치 대수")
fig_cctv = px.bar(
    cctv_grouped,
    x='읍면동',
    y='설치대수',
    title='📍 진주시 읍면동별 CCTV 설치대수',
    labels={'설치대수': '설치 대수', '읍면동': '읍면동'},
    text='설치대수',
    height=500
)
fig_cctv.update_traces(textposition='outside')
fig_cctv.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_cctv, use_container_width=True)

# =====================
# 💡 가로등 단독 그래프
# =====================
st.subheader("📍 법정동별 가로등 총등수")
fig_street = px.bar(
    street_grouped,
    x='법정동',
    y='총등수',
    title='💡 진주시 법정동별 가로등 총등수',
    labels={'총등수': '총 등수', '법정동': '법정동'},
    text='총등수',
    height=500
)
fig_street.update_traces(textposition='outside')
fig_street.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_street, use_container_width=True)

# =====================
# ⚖️ CCTV & 가로등 비교 (이중 Y축, 꺾은선)
# =====================
st.subheader("📊 CCTV vs 가로등 설치 비교 (막대+꺾은선 이중 Y축)")

# 공통 동 이름 기준 병합
merged = pd.merge(
    cctv_grouped.rename(columns={'읍면동': '동이름'}),
    street_grouped.rename(columns={'법정동': '동이름'}),
    on='동이름',
    how='inner'
)
merged = merged.sort_values(by='동이름')

# 이중 y축 그래프 (CCTV: 막대, 가로등: 꺾은선)
fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

# CCTV: 막대 그래프
fig_dual.add_trace(
    go.Bar(
        x=merged['동이름'],
        y=merged['설치대수'],
        name="CCTV 설치대수",
        marker_color='steelblue'
    ),
    secondary_y=False
)

# 가로등: 꺾은선 그래프
fig_dual.add_trace(
    go.Scatter(
        x=merged['동이름'],
        y=merged['총등수'],
        name="가로등 총등수",
        mode='lines+markers',
        line=dict(color='orange', width=2),
        marker=dict(size=6)
    ),
    secondary_y=True
)

# 레이아웃
fig_dual.update_layout(
    title="📊 진주시 동별 CCTV 설치대수 vs 가로등 총등수 (이중 Y축)",
    height=600,
    xaxis_tickangle=-45,
    legend=dict(x=0.01, y=0.99),
    margin=dict(t=50, b=50)
)

fig_dual.update_yaxes(title_text="설치대수 (CCTV)", secondary_y=False)
fig_dual.update_yaxes(title_text="총등수 (가로등)", secondary_y=True)

# 출력
st.plotly_chart(fig_dual, use_container_width=True)