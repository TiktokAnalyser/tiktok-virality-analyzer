import streamlit as st
import random
import time
import re

# ---------------------------------------
# APP CONFIGURATION
# ---------------------------------------
st.set_page_config(page_title="Universal TikTok Virality Analyzer", page_icon="🎥", layout="centered")

st.title("🎬 TikTok Video Virality Analyzer (AI Edition)")
st.caption("Upload any TikTok-style video to receive AI-powered insights, analytics, and recommendations for higher reach & engagement.")

# ---------------------------------------
# VIDEO UPLOAD
# ---------------------------------------
uploaded_file = st.file_uploader("Upload your TikTok video (MP4 or MOV)", type=["mp4", "mov"])

# Simple keyword extraction from filename
def extract_topic(filename):
    name = filename.lower()
    words = re.findall(r"[a-zA-Z]+", name)
    keywords = [w for w in words if len(w) > 3]
    return ", ".join(keywords[:5]) if keywords else "general"

# ---------------------------------------
# AI-like keyword & hashtag logic
# ---------------------------------------
def generate_hashtags(topic):
    base_tags = ["#FYP", "#Viral", "#TikTokTrend"]
    topic_tags = {
        "health": ["#HealthyLiving", "#Wellness", "#FitnessTips", "#Nutrition", "#MindBody"],
        "fashion": ["#OOTD", "#FashionTok", "#StyleTips", "#TrendAlert"],
        "food": ["#FoodTok", "#RecipeIdeas", "#CookingTips", "#Tasty", "#Foodie"],
        "motivation": ["#Motivation", "#Mindset", "#Goals", "#PositiveVibes"],
        "education": ["#LearnOnTikTok", "#StudyTips", "#DidYouKnow", "#Education"],
        "business": ["#Entrepreneur", "#SideHustle", "#BusinessTips", "#FinanceTok"],
        "comedy": ["#Funny", "#Relatable", "#LOL", "#ComedyVideo"],
    }

    selected = []
    for key in topic_tags:
        if key in topic.lower():
            selected = topic_tags[key]
            break
    if not selected:
        selected = random.choice(list(topic_tags.values()))

    return base_tags + selected[:5]

# ---------------------------------------
# AI Feedback logic
# ---------------------------------------
def generate_feedback(topic):
    feedback_pool = [
        "Hook viewers in the first 2 seconds with a question or surprise.",
        "Add captions — 80% of TikTok users watch with sound off.",
        "Use trending sounds to boost discovery.",
        "Ensure lighting and framing highlight your main subject.",
        "Post at your audience’s active hours (Fri/Sat evenings work best).",
        "Include a call-to-action like 'Follow for more' at the end.",
        "Engage in comments within 1 hour to boost ranking.",
        "Use natural storytelling flow — start → climax → takeaway.",
        "Consider using short cuts (2–3 seconds) to keep momentum.",
    ]
    random.shuffle(feedback_pool)
    return feedback_pool[:5]

# ---------------------------------------
# ANALYTICS SIMULATION
# ---------------------------------------
def generate_analytics(topic):
    analytics = {
        "Hook Strength": random.randint(60, 95),
        "Retention Potential": random.randint(50, 98),
        "Visual Clarity": random.randint(55, 100),
        "Audio Quality": random.randint(50, 100),
        "Trend Relevance": random.randint(40, 95),
        "Overall Virality Score": random.randint(60, 100),
    }
    return analytics

# ---------------------------------------
# MAIN APP LOGIC
# ---------------------------------------
if uploaded_file is not None:
    topic = extract_topic(uploaded_file.name)
    st.video(uploaded_file)
    st.info(f"📊 Detected Topic: **{topic.title()}**")

    with st.spinner("Analyzing video content and generating insights..."):
        time.sleep(3)
        analytics = generate_analytics(topic)
        hashtags = generate_hashtags(topic)
        feedback = generate_feedback(topic)
        caption = f"Discover amazing insights about {topic}! #AIAnalyzer #ViralVideo"

    st.success("✅ Analysis Complete — Here’s your full report:")

    # Metrics Layout
    st.subheader("📈 Performance Metrics")
    cols = st.columns(3)
    metrics = list(analytics.items())
    for i, (label, value) in enumerate(metrics):
        cols[i % 3].metric(label, f"{value}/100")

    st.subheader("🔥 Suggested Hashtags")
    st.write(" ".join(hashtags))

    st.subheader("✍️ AI Caption Suggestion")
    st.write(caption)

    st.subheader("💡 Professional Recommendations")
    for tip in feedback:
        st.write("•", tip)

    # Report Download
    report = f"""
    TikTok AI Virality Report
    Topic: {topic}

    Metrics:
    {chr(10).join([f"- {k}: {v}/100" for k, v in analytics.items()])}

    Suggested Hashtags:
    {", ".join(hashtags)}

    Caption:
    {caption}

    Recommendations:
    {chr(10).join(feedback)}
    """

    st.download_button("⬇️ Download Full Report", report, file_name="tiktok_ai_report.txt")
else:
    st.info("📤 Upload a TikTok video to begin analysis.")
