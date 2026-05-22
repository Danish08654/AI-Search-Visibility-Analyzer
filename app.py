import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="AI Visibility Analyzer",
    page_icon="🚀",
    layout="wide"
)

# HEADER
st.markdown(
    """
    <div style="text-align:center;">
        <h1> AI Search Visibility Analyzer</h1>
        <p style="color:gray;">Analyze how AI models rank and mention your brands</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


query = st.sidebar.text_input(
    "Search Query",
    placeholder="Best AI image generation tools"
)

brands = st.sidebar.text_input(
    "Brands (comma separated)",
    placeholder="OpenAI, Midjourney, Stability AI"
)

analyze_btn = st.sidebar.button(" Run Analysis")

# MAIN LOGIC

if analyze_btn:

    if not query.strip() or not brands.strip():
        st.warning("⚠️ Please fill all fields in sidebar")
        st.stop()

    brand_list = [b.strip() for b in brands.split(",")]

    with st.spinner("🤖 Analyzing AI responses..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={
                    "query": query,
                    "brands": brand_list
                }
            )

            data = response.json()

        except Exception as e:
            st.error(f"Backend Error: {e}")
            st.stop()

    # TOP METRICS
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Query Length", len(query.split()))
    col2.metric("Brands Tracked", len(brand_list))
    col3.metric("AI Sources", len(data["responses"]))

    st.divider()

    # QUERY DISPLAY CARD
    
    st.markdown(
        f"""
        <div style="padding:15px; border-radius:12px; background:#0f172a; color:white;">
            <h4>📌 Query</h4>
            <p>{data["query"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # -------------------------
    # AI RESPONSES
    # -------------------------
    st.subheader("🤖 AI Model Responses")

    for platform, text in data["responses"].items():
        with st.expander(f"🔹 {platform} Response"):
            st.write(text)

    st.divider()

    # -------------------------
    # SENTIMENT
    # -------------------------
    st.subheader("😊 Sentiment Analysis")

    st.info(f"Overall Sentiment: {data['sentiment']}")

    # -------------------------
    # RANKINGS
    # -------------------------
    st.subheader("🏆 Brand Rankings")

    st.json(data["rankings"])

    # -------------------------
    # SHARE OF VOICE CHART
    # -------------------------
    st.subheader("📊 Share of Voice")

    sov_data = pd.DataFrame({
        "Brand": list(data["share_of_voice"].keys()),
        "Share": list(data["share_of_voice"].values())
    })

    fig = px.pie(
        sov_data,
        names="Brand",
        values="Share",
        hole=0.4
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        legend_title="Brands"
    )

    st.plotly_chart(fig, use_container_width=True)
