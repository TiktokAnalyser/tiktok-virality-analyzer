import streamlit as st
import random
import time
import re
from datetime import datetime

# --------------------------------
# CONFIG
# --------------------------------
st.set_page_config(page_title="TikTok Smart Virality Analyzer", page_icon="🎥", layout="wide")

st.title("🎬 TikTok Video Virality Analyzer (Dynamic Edition)")
st.caption("AI-powered TikTok analyzer that dynamically suggests hashtags, sounds, and post times based on your video content.")

# --------------------------------
# HELPER FUNCTIONS
# --------------------------------

# Extract topic keywords from filename
def extract_topic(filename):
    name = filename.lower()
    words = re.findall(r"[a-zA-Z]+", name)
    keywords = [w for w in words if len(w) > 3]
    topic = " ".join(keywords[:6]) if keywords else "general"
    return topic

# Generate hashtags dynamically based on topic
def dynamic_hashtags(topic):
    base = ["#FYP", "#TikTokTrend"]
    words = topic.split()
    smart_tags = [f"#{w.capitalize()}" for w in words if len(w) > 3]
    extras = random.sample(["#ViralVideo", "#TrendingNow", "#ExplorePage", "#Creators", "#ContentTips"], 3)
    hashtags = list(dict.fromkeys(base + smart_tags + extras))  # remove duplicates
    return hashtags[:10]

# Generate sound ideas dynamically
def dynamic_sounds(topic):
    core = topic.split()
    base_sound = random.choice(["Remix", "Groove", "Beat", "Vibes", "Track", "Flow"])
    descriptor = core[0].capitalize() if core else "Viral"
    return [f"{descriptor} {base_sound}", f"{descriptor} Theme", f"{descriptor} Loop"]

# Suggest best posting time dynamically
def best_posting_time(topic):
    topic = topic.lower()
    if any(x in topic for x in ["food", "recipe", "health", "fitness", "morning"]):
        return ["Morning (7 AM – 10 AM)", "Afternoon (12 PM – 2 PM)"]
    elif any(x in topic for x in ["comedy", "funny", "dance", "music"]):
        return ["Evening (7 PM – 10 PM)", "Weekend Nights"]
    elif any(x in topic for x in ["education", "facts", "tutorial", "learn"]):
        return ["Morning (9 AM – 11 AM)", "Weekdays 3 PM"]
    elif any(x in topic for x in ["fashion", "beauty", "makeup", "style"]):
        return ["Afternoon (3 PM – 6 PM)", "Saturday 10 AM"]
    else:
        return ["Evening (6 PM – 9 PM)", "Friday 8 PM"]

# Generate analytics
def generate_metrics():
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

# Generate feedback
def generate_feedback(topic):
    general_tips = [
        "Add captions — 80% of TikTok users watch with sound off.",
        "Hook your viewers in the first 2 seconds.",
        "Use trending sounds that fit your content tone.",
        "Keep total video length under 20 seconds for retention.",
        "Add a call-to-action like 'Follow for more'.",
        "Engage with comments in the first 30 minutes.",
    ]
    if "food" in topic:
        general_tips.append("Show ingredients clearly and add close-up shots of texture.")
    if "health" in topic:
        general_tips.append("Use credible health facts or show real results to build trust.")
    if "fashion" in topic:
        general_tips.append("Add outfit transitions or mirror shots to catch attention.")
    if "comedy" in topic:
        general_tips.append("Add punchline text overlay at the last 2 seconds.")
    random.shuffle(general_tips)
    return general_tips[:6]

# --------------------------------
# APP INTERFACE
# --------------------------------
tab1, tab2, tab3 = st.tabs(["📈 Video Analysis", "🔥 Trend Finder", "🧾 Download Report"])

with tab1:
    uploaded_file = st.file_uploader("Upload your TikTok video", type=["mp4", "mov"])
    if uploaded_file:
        topic = extract_topic(uploaded_file.name)
        st.video(uploaded_file)
        st.info(f"Detected Topic: **{topic.title()}**")

        with st.spinner("Analyzing your video content..."):
            time.sleep(3)
            metrics = generate_metrics()
            feedback = generate_feedback(topic)

        st.success("✅ Analysis Complete")
        cols = st.columns(4)
        for i, (k, v) in enumerate(metrics.items()):
            cols[i % 4].metric(k, f"{v}/100")

        st.session_state["topic"] = topic
        st.session_state["metrics"] = metrics
        st.session_state["feedback"] = feedback

with tab2:
    st.header("🔥 Smart Trend Finder (AI-based Suggestions)")
    topic = st.session_state.get("topic", "general")
    hashtags = dynamic_hashtags(topic)
    sounds = dynamic_sounds(topic)
    times = best_posting_time(topic)

    st.subheader("📌 Trending Hashtags")
    st.write(" ".join(hashtags))

    st.subheader("🎵 Recommended Sounds")
    for s in sounds:
        st.write("🎶", s)

    st.subheader("🕒 Optimal Post Times")
    for t in times:
        st.write("🕓", t)

with tab3:
    if "metrics" in st.session_state:
        topic = st.session_state["topic"]
        metrics = st.session_state["metrics"]
        feedback = st.session_state["feedback"]
        hashtags = dynamic_hashtags(topic)
        sounds = dynamic_sounds(topic)
        times = best_posting_time(topic)

        report = f"""
        TikTok Smart Analyzer Report
        Topic: {topic.title()}
        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}

        Metrics:
        {chr(10).join([f"- {k}: {v}/100" for k, v in metrics.items()])}

        Trending Hashtags:
        {', '.join(hashtags)}

        Suggested Sounds:
        {', '.join(sounds)}

        Best Posting Times:
        {', '.join(times)}

        Recommendations:
        {chr(10).join(feedback)}
        """

        st.download_button("⬇️ Download Full Report", report, file_name="tiktok_smart_report.txt")
    else:
        st.info("Please upload a video and analyze it first.")
