import streamlit as st
import pandas as pd
import simulation
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Election Dashboard", layout="wide")

# Title
st.title("🗳️ Tamil Nadu Election Prediction Dashboard")

# Load data
df = pd.read_csv("tn_full_synthetic_dataset.csv")

# Sidebar controls
st.sidebar.header("⚙️ Controls")

tvk_share = st.sidebar.slider("TVK Vote Share (%)", 0, 20, 10)

# Apply simulation
df = simulation.simulate_tvk(df, tvk_share=tvk_share/100)

# Select constituency
constituencies = sorted(df["Constituency"].unique())
selected_const = st.sidebar.selectbox("Select Constituency", constituencies)

# Filter data
subset = df[df["Constituency"] == selected_const].copy()

# Sort by vote share
subset = subset.sort_values(by="VoteShare_%", ascending=False)

# Top party
winner = subset.iloc[0]["Party"]
winner_vote = subset.iloc[0]["VoteShare_%"]
runner_up_vote = subset.iloc[1]["VoteShare_%"]
margin = winner_vote - runner_up_vote

# 🔥 KPI SECTION
col1, col2, col3 = st.columns(3)

col1.metric("🏆 Leading Party", winner)
col2.metric("📊 Vote Share", f"{winner_vote:.2f}%")
col3.metric("⚖️ Margin", f"{margin:.2f}%")

st.markdown("---")

# 📊 CHART SECTION
col1, col2 = st.columns(2)

# Pie Chart
with col1:
    st.subheader("🥧 Vote Share Distribution")
    fig1, ax1 = plt.subplots()
    ax1.pie(
        subset["VoteShare_%"],
        labels=subset["Party"],
        autopct='%1.1f%%',
        startangle=140
    )
    ax1.axis('equal')
    st.pyplot(fig1)

# Bar Chart
with col2:
    st.subheader("📊 Vote Share Comparison")
    st.bar_chart(subset.set_index("Party")["VoteShare_%"])

st.markdown("---")

# 📋 Data Table
st.subheader("📋 Detailed Data")
st.dataframe(subset[["Party", "VoteShare_%"]])

# Footer
st.markdown("### 🔍 Insights")
st.write(f"In **{selected_const}**, **{winner}** is leading with a margin of **{margin:.2f}%**.")
