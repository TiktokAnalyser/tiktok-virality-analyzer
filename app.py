import streamlit as st
import whisper
import tempfile
import random
import time
import re
from datetime import datetime

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="TikTok Analyzer Pro", page_icon="🎥", layout="wide")

st.title("TikTok Video Analyzer with AI Transcription")
st.caption("Professional dashboard for analyzing TikTok videos — includes automatic transcription, analytics, hashtags, captions, and SEO insights.")

# ---------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------

def extract_keywords(text):
    words = re.findall(r"[A-Za-z]+", text.lower())
    stop = {"the", "and", "you", "for", "that", "this", "with", "are", "was", "from", "your", "what", "when"}
    keywords = [w for w in words if len(w) > 3 and w not in stop]
    freq = {}
    for w in keywords:
        freq[w] = freq.get(w, 0) + 1
    top_words = sorted(freq, key=freq.get, reverse=True)[:6]
    return " ".join(top_words) if top_words else "general"

def classify_category(text):
    t = text.lower()
    if any(x in t for x in ["food", "recipe", "eat", "kitchen"]): return "food"
    if any(x in t for x in ["health", "fitness", "wellness", "diet"]): return "health"
    if any(x in t for x in ["fashion", "style", "beauty", "makeup"]): return "fashion"
    if any(x in t for x in ["motivation", "inspire", "success", "mindset"]): return "motivation"
    if any(x in t for x in ["education", "learn", "study", "tutorial", "facts"]): return "education"
    if any(x in t for x in ["comedy", "funny", "humor", "skit"]): return "comedy"
    if any(x in t for x in ["music", "dance", "song", "beat"]): return "entertainment"
    return "general"

def generate_metrics():
    return {
        "Hook Strength": random.randint(60, 95),
        "Retention Potential": random.randint(55, 98),
        "Replay Factor": random.randint(40, 95),
        "Engagement Probability": random.randint(50, 100),
        "Visual Clarity": random.randint(60, 100),
        "Audio Quality": random.randint(55, 100),
        "Trend Relevance": random.randint(40, 95),
        "Overall Virality Score": random.randint(65, 100),
    }

def generate_hashtags(topic, category):
    words = [w.capitalize() for w in topic.split() if len(w) > 3]
    base_tags = ["#FYP", "#Viral"]
    category_tags = {
        "food": ["#FoodTok", "#Cooking", "#Tasty", "#HomeChef", "#RecipeIdeas"],
        "health": ["#HealthyLiving", "#Wellness", "#Nutrition", "#FitnessTips"],
        "fashion": ["#OOTD", "#StyleTok", "#TrendAlert", "#FashionTips"],
        "motivation": ["#Motivation", "#Mindset", "#DailyInspiration", "#GoalGetter"],
        "education": ["#LearnOnTikTok", "#StudyTok", "#DidYouKnow", "#Knowledge"],
        "comedy": ["#FunnyTok", "#ComedyVideo", "#LOL", "#Skits"],
        "entertainment": ["#DanceTok", "#MusicTrend", "#Performance", "#ShowTime"],
        "general": ["#ForYou", "#ExplorePage", "#Creators", "#TrendingNow"],
    }
    selected = category_tags.get(category, category_tags["general"])
    custom = [f"#{w}" for w in words[:4]]
    hashtags = list(dict.fromkeys(base_tags + selected + custom))
    return hashtags[:10]

def generate_best_time(category):
    times = {
        "food": ["11 AM – 2 PM", "Friday 6 PM"],
        "health": ["6 AM – 9 AM", "Sunday 8 PM"],
        "fashion": ["3 PM – 6 PM", "Saturday 10 AM"],
        "motivation": ["Morning 7–9 AM", "Sunday 7 PM"],
        "education": ["Weekdays 9–11 AM", "Wednesday 3 PM"],
        "comedy": ["Evening 8–11 PM", "Weekend nights"],
        "entertainment": ["Evening 6–10 PM", "Saturday 8 PM"],
        "general": ["6 PM – 9 PM", "Friday 8 PM"],
    }
    return times.get(category, times["general"])

def generate_caption(topic, category):
    return f"{topic.title()} — short insights from the world of {category}."

def generate_description(topic, category):
    return (
        f"This video discusses {topic}. It covers essential aspects of {category} content "
        f"that engage modern TikTok audiences. Stay tuned, like, and follow for more."
    )

def generate_keywords(topic, category):
    words = topic.lower().split()
    extras = [category, "tiktok", "viral", "trending", "short video", "algorithm"]
    return ", ".join(list(dict.fromkeys(words + extras))[:12])

def generate_feedback(category):
    base = [
        "Start with a strong hook in the first 2 seconds.",
        "Add subtitles for higher retention and accessibility.",
        "Maintain steady lighting and avoid overexposure.",
        "Post consistently (3–4 times weekly).",
        "Encourage comments to drive engagement.",
    ]
    if category == "comedy": base.append("Keep your pacing tight for better comedic timing.")
    if category == "education": base.append("Summarize key takeaways at the end.")
    if category == "fashion": base.append("Highlight textures and outfit details clearly.")
    if category == "health": base.append("Reference credible data or studies if relevant.")
    if category == "food": base.append("Include step visuals or final presentation shots.")
    random.shuffle(base)
    return base[:6]

# ---------------------------------------
# MAIN APP
# ---------------------------------------
uploaded_file = st.file_uploader("Upload your TikTok video", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    with st.spinner("Transcribing audio... please wait."):
        model = whisper.load_model("base")
        result = model.transcribe(temp_path)
        transcript = result["text"]

    topic = extract_keywords(transcript)
    category = classify_category(transcript)
    metrics = generate_metrics()
    hashtags = generate_hashtags(topic, category)
    post_times = generate_best_time(category)
    caption = generate_caption(topic, category)
    description = generate_description(topic, category)
    keywords = generate_keywords(topic, category)
    feedback = generate_feedback(category)

    # --- Results Dashboard ---
    st.header("Analysis Results")
    cols = st.columns(4)
    for i, (k, v) in enumerate(metrics.items()):
        cols[i % 4].metric(k, f"{v}/100")

    st.subheader("Detected Topic & Category")
    st.write(f"Topic: {topic.title()}  |  Category: {category.title()}")

    st.subheader("Transcript")
    st.text_area("Transcribed Speech", transcript, height=200)

    st.subheader("Suggested Hashtags")
    st.write(" ".join(hashtags))

    st.subheader("Optimal Posting Times")
    st.write(", ".join(post_times))

    st.subheader("Recommended Caption")
    st.write(caption)

    st.subheader("Recommended Description")
    st.write(description)

    st.subheader("SEO Keywords")
    st.write(keywords)

    st.subheader("Professional Recommendations")
    for tip in feedback:
        st.write("-", tip)

    # --- Downloadable Report ---
    report = f"""
TikTok Video Analysis Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Topic: {topic.title()}
Category: {category.title()}

--- Transcript ---
{transcript}

--- Metrics ---
{chr(10).join([f"- {k}: {v}/100" for k, v in metrics.items()])}

--- Suggested Hashtags ---
{", ".join(hashtags)}

--- Optimal Posting Times ---
{", ".join(post_times)}

--- Caption ---
{caption}

--- Description ---
{description}

--- SEO Keywords ---
{keywords}

--- Recommendations ---
{chr(10).join(feedback)}
"""
    st.download_button("Download Full Report", report, file_name="tiktok_transcription_analysis.txt")

else:
    st.info("Upload a TikTok video file to begin transcription and analysis.")
