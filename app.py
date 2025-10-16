import streamlit as st
import random
import time
import re
from datetime import datetime

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="TikTok Virality Analyzer Pro", page_icon="🎥", layout="wide")

st.title("🎬 TikTok Video Virality Analyzer PRO")
st.caption("Upload your video and let AI generate metrics, insights, and current TikTok trends for your niche.")

# ---------------------------
# DATA MOCKUPS (Simulated)
# ---------------------------
trending_data = {
    "health": {
        "hashtags": ["#EyeHealth", "#WellnessTips", "#HealthyEating", "#BloodTypeDiet", "#HolisticLiving"],
        "sounds": ["‘Positive Energy’ remix", "‘Calm Beats’ Lo-Fi", "‘Morning Reset’ instrumental"],
        "best_times": ["6 PM - 9 PM", "7 AM - 9 AM"],
    },
    "fashion": {
        "hashtags": ["#OOTD", "#StyleTok", "#FashionWeek", "#TrendAlert", "#OutfitIdeas"],
        "sounds": ["‘Runway Walk’ edit", "‘Pop Vogue’ beat", "‘Mirror Selfie’ trend sound"],
        "best_times": ["4 PM - 8 PM", "Saturday 10 AM"],
    },
    "food": {
        "hashtags": ["#FoodTok", "#HomeCooking", "#RecipeIdeas", "#WhatIEat", "#TastyFood"],
        "sounds": ["‘Cooking Groove’ theme", "‘Yummy Remix’", "‘Chef Vibes’"],
        "best_times": ["11 AM - 1 PM", "Friday 6 PM"],
    },
    "motivation": {
        "hashtags": ["#Motivation", "#GrindMode", "#DailyInspiration", "#SuccessMindset", "#GoalGetter"],
        "sounds": ["‘Rise & Grind’ speech mix", "‘Success’ cinematic track", "‘Hustle Energy’"],
        "best_times": ["Morning 6–9 AM", "Sunday evening"],
    },
    "comedy": {
        "hashtags": ["#FunnyTok", "#Relatable", "#LOL", "#Skits", "#ViralComedy"],
        "sounds": ["‘Laugh Track’ edit", "‘Meme Beat’", "‘Funny Audio Remix’"],
        "best_times": ["Night 8–11 PM", "Weekend afternoons"],
    },
    "education": {
        "hashtags": ["#LearnOnTikTok", "#DidYouKnow", "#StudyTok", "#Facts", "#BrainTips"],
        "sounds": ["‘Study Focus’ background", "‘Smart Facts’ loop", "‘Science Jam’ beat"],
        "best_times": ["Morning 9–11 AM", "Weekdays 3 PM"],
    },
    "general": {
        "hashtags": ["#ForYou", "#ViralNow", "#CreatorsOfTikTok", "#TrendAlert", "#FYP"],
        "sounds": ["‘Epic Beat’", "‘Viral Flow’", "‘For You Mix’"],
        "best_times": ["6 PM - 10 PM"],
    }
}

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------
def extract_topic(filename):
    name = filename.lower()
    words = re.findall(r"[a-zA-Z]+", name)
    if "food" in name: return "food"
    if "health" in name: return "health"
    if "fashion" in name or "style" in name: return "fashion"
    if "motivation" in name or "inspire" in name: return "motivation"
    if "funny" in name or "comedy" in name: return "comedy"
    if "learn" in name or "education" in name: return "education"
    return "general"

def generate_analytics():
    return {
        "Hook Strength": random.randint(60, 95),
        "Retention Potential": random.randint(55, 99),
        "Replay Factor": random.randint(40, 95),
        "Engagement Probability": random.randint(50, 100),
        "Visual Clarity": random.randint(60, 100),
        "Audio Quality": random.randint(50, 100),
        "Trend Relevance": random.randint(40, 95),
        "Overall Virality Score": random.randint(65, 100),
    }

def generate_feedback():
    feedback_pool = [
        "Start with a question or emotional hook in the first 2 seconds.",
        "Keep total length under 20 seconds for optimal retention.",
        "Use trending sounds within your niche for 15–20% extra visibility.",
        "Add closed captions — boosts accessibility & engagement.",
        "Include a call-to-action like ‘Follow for more tips!’",
        "Maintain consistent posting (3–4x weekly).",
        "Engage in comments early to trigger the algorithm.",
        "Use color contrast or text overlays for clarity.",
        "End with a punchline or unexpected twist to increase shares.",
    ]
    random.shuffle(feedback_pool)
    return feedback_pool[:5]

# ---------------------------
# APP INTERFACE
# ---------------------------
tab1, tab2, tab3 = st.tabs(["📈 Video Analysis", "🔥 Trend Finder Panel", "🧾 Report Summary"])

with tab1:
    uploaded_file = st.file_uploader("Upload your TikTok video", type=["mp4", "mov"])
    if uploaded_file:
        category = extract_topic(uploaded_file.name)
        st.video(uploaded_file)
        st.info(f"Detected category: **{category.title()}**")

        with st.spinner("Analyzing your video for viral potential..."):
            time.sleep(3)
            analytics = generate_analytics()
            feedback = generate_feedback()

        st.success("✅ Analysis Complete")

        st.subheader("📊 Key Metrics")
        cols = st.columns(4)
        for i, (k, v) in enumerate(analytics.items()):
            cols[i % 4].metric(k, f"{v}/100")

        st.subheader("💡 AI Recommendations")
        for tip in feedback:
            st.write("•", tip)

        st.session_state["category"] = category
        st.session_state["analytics"] = analytics
        st.session_state["feedback"] = feedback

with tab2:
    st.header("🔥 TikTok Trend Finder Panel")
    category = st.session_state.get("category", "general")
    trend = trending_data.get(category, trending_data["general"])

    st.write(f"### Trending in **{category.title()}** Category")

    col1, col2, col3 = st.columns(3)
    col1.metric("Trending Hashtags", len(trend["hashtags"]))
    col2.metric("Hot Sounds", len(trend["sounds"]))
    col3.metric("Best Times", len(trend["best_times"]))

    st.subheader("📌 Top Hashtags")
    st.write(" ".join(trend["hashtags"]))

    st.subheader("🎵 Hot Sounds / Music")
    for s in trend["sounds"]:
        st.write("🎶", s)

    st.subheader("🕓 Best Times to Post")
    for t in trend["best_times"]:
        st.write("🕒", t)

with tab3:
    if "analytics" in st.session_state:
        st.header("🧾 Full AI Report")
        analytics = st.session_state["analytics"]
        category = st.session_state["category"]
        feedback = st.session_state["feedback"]
        trend = trending_data.get(category, trending_data["general"])

        report = f"""
        TikTok Video Virality Report
        Category: {category}

        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}

        Metrics:
        {chr(10).join([f"- {k}: {v}/100" for k, v in analytics.items()])}

        Trending Hashtags:
        {', '.join(trend['hashtags'])}

        Recommended Sounds:
        {', '.join(trend['sounds'])}

        Best Posting Times:
        {', '.join(trend['best_times'])}

        Feedback:
        {chr(10).join(feedback)}
        """

        st.download_button("⬇️ Download Full Professional Report", report, file_name="tiktok_trend_report.txt")
    else:
        st.info("Upload and analyze a video first to generate your report.")
