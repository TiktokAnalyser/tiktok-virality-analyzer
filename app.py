import streamlit as st
import random
import time

# -------------------------------
# APP SETTINGS
# -------------------------------
st.set_page_config(page_title="TikTok Virality Analyzer", page_icon="🎥", layout="centered")

# Header
st.title("🎬 TikTok Video Virality Analyzer")
st.write("Upload your TikTok-style video and get AI-powered insights about its viral potential!")

# -------------------------------
# UPLOAD SECTION
# -------------------------------
uploaded_file = st.file_uploader("Upload your video (MP4, MOV)", type=["mp4", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)
    with st.spinner("Analyzing your video... ⏳"):
        time.sleep(3)  # Simulate analysis time

    # -------------------------------
    # MOCK AI LOGIC (Simulated)
    # -------------------------------
    virality_score = random.randint(60, 100)
    engagement_prediction = random.choice(["High", "Moderate", "Low"])
    best_post_time = random.choice(["Friday 7 PM", "Saturday 10 AM", "Sunday 8 PM"])
    hashtags = random.sample(
        ["#FYP", "#Viral", "#TrendingNow", "#TikTokChallenge", "#Lifestyle", "#Motivation", "#DanceTrend", "#ComedyVibes", "#MorningRoutine"],
        5
    )
    feedback = [
        "🎯 Strong start! Keep the first 2 seconds energetic.",
        "🧠 Add captions — videos with captions perform 25% better.",
        "🎵 Use trending sound effects or remixes.",
        "✨ Lighting looks great; maintain consistency across clips.",
        "📈 Add a call-to-action at the end (‘Follow for Part 2!’)."
    ]

    # -------------------------------
    # DISPLAY RESULTS
    # -------------------------------
    st.success("✅ Video Analysis Complete!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Virality Score", f"{virality_score}/100")
    col2.metric("Predicted Engagement", engagement_prediction)
    col3.metric("Best Time to Post", best_post_time)

    st.subheader("🔥 Suggested Hashtags")
    st.write(" ".join(hashtags))

    st.subheader("💡 AI Feedback & Recommendations")
    for tip in feedback:
        st.write(tip)

    # -------------------------------
    # EXTRA: Downloadable Report
    # -------------------------------
    report = f"""
    TikTok Video Virality Report

    - Virality Score: {virality_score}/100
    - Predicted Engagement: {engagement_prediction}
    - Best Time to Post: {best_post_time}
    - Suggested Hashtags: {', '.join(hashtags)}

    Feedback:
    {chr(10).join(feedback)}
    """

    st.download_button("⬇️ Download Analysis Report", report, file_name="tiktok_virality_report.txt")
else:
    st.info("📤 Please upload your TikTok video file to start the analysis.")
