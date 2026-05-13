%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SNS Marketing Analytics", page_icon="📱", layout="wide")

st.title("📱 SNS Marketing Analytics Dashboard")
st.markdown("Track your campaign ROI and engagement metrics")

if "campaigns" not in st.session_state:
    st.session_state.campaigns = pd.DataFrame({
        "Campaign Name": ["Summer Festival", "Winter Wonderland", "Spring Bloom"],
        "Platform": ["Instagram", "TikTok", "YouTube"],
        "Budget (USD)": [20000, 15000, 30000],
        "Revenue (USD)": [65000, 45000, 90000],
        "Followers": [15000, 28000, 45000],
        "Likes": [4520, 8900, 12300],
        "Shares": [890, 2100, 3400],
        "Comments": [234, 567, 890]
    })

def calculate_metrics(df):
    df = df.copy()
    df["ROI"] = (df["Revenue (USD)"] / df["Budget (USD)"]).round(2)
    df["Engagement Rate (%)"] = ((df["Likes"] + df["Shares"] + df["Comments"]) / df["Followers"] * 100).round(1)
    return df

with st.sidebar:
    st.header("➕ Add New Campaign")
    new_name = st.text_input("Campaign Name")
    new_platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube", "Facebook", "Twitter"])
    new_budget = st.number_input("Budget (USD)", min_value=0, step=1000, value=10000)
    new_revenue = st.number_input("Revenue (USD)", min_value=0, step=1000, value=20000)
    new_followers = st.number_input("Followers", min_value=0, step=100, value=10000)
    new_likes = st.number_input("Likes", min_value=0, step=10, value=1000)
    new_shares = st.number_input("Shares", min_value=0, step=10, value=200)
    new_comments = st.number_input("Comments", min_value=0, step=10, value=100)
    if st.button("Add Campaign"):
        new_row = pd.DataFrame({
            "Campaign Name": [new_name],
            "Platform": [new_platform],
            "Budget (USD)": [new_budget],
            "Revenue (USD)": [new_revenue],
            "Followers": [new_followers],
            "Likes": [new_likes],
            "Shares": [new_shares],
            "Comments": [new_comments]
        })
        st.session_state.campaigns = pd.concat([st.session_state.campaigns, new_row], ignore_index=True)
        st.success(f"✅ {new_name} added successfully!")

st.subheader("📈 Campaign Data")
df_with_metrics = calculate_metrics(st.session_state.campaigns)
st.dataframe(df_with_metrics, use_container_width=True)

st.subheader("🎯 Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Budget", f"${df_with_metrics['Budget (USD)'].sum():,.0f}")
col2.metric("Total Revenue", f"${df_with_metrics['Revenue (USD)'].sum():,.0f}")
col3.metric("Average ROI", f"{df_with_metrics['ROI'].mean():.1f}x")
col4.metric("Avg Engagement Rate", f"{df_with_metrics['Engagement Rate (%)'].mean():.1f}%")

def color_roi(val):
    color = 'green' if val >= 2 else 'red'
    return f'color: {color}'
st.subheader("🎨 ROI Performance")
st.dataframe(df_with_metrics[["Campaign Name", "ROI"]].style.applymap(color_roi, subset=["ROI"]))

st.subheader("📊 Budget vs Revenue by Campaign")
fig_bar = px.bar(df_with_metrics, x="Campaign Name", y=["Budget (USD)", "Revenue (USD)"],
                 barmode="group", title="Budget vs Revenue")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 Weekly Engagement Trends (Demo)")
weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
weekly_data = pd.DataFrame({
    "Week": weeks,
    "Likes": [1200, 2100, 1800, 3000],
    "Shares": [300, 450, 400, 600],
    "Comments": [150, 220, 190, 310]
})
fig_line = px.line(weekly_data, x="Week", y=["Likes", "Shares", "Comments"],
                   title="Weekly Engagement", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.caption("📱 SNS Marketing Analytics Dashboard - Powered by Streamlit")