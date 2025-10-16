import streamlit as st
import random
import time
import re
from datetime import datetime

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="TikTok Video Analyzer", page_icon="🎥", layout="wide")

st.title("TikTok Video Virality & Content Analyzer")
st.caption("Professional AI-style analysis dashboard for any TikTok video — metrics, hashtags, caption, description, and SEO insights.")

# ---------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------

def extract_topic(filename):
    """Extract keywords from video filename."""
    name = filename.lower()
    words = re.findall(r"[a-zA-Z]+", name)
    keywords = [w for w in words if len(w) > 3]
    topic = " ".join(keywords[:6]) if keywords else "general"
    return topic

def classify_category(topic):
    """Infer a general category from topic text."""
    t = topic.lower()
    if any(x in t for x in ["food", "recipe", "cook", "eat"]): return "food"
    if any(x in t for x in ["health", "fitness", "wellness", "diet"]): return "health"
    if any(x in t for x in ["fashion", "style", "beauty", "makeup"]): return "fashion"
    if any(x in t for x in ["motivation", "inspire", "success", "mindset"]): return "motivation"
    if any(x in t for x in ["education", "learn", "study", "tutorial", "facts"]): return "education"
    if any(x in t for x in ["comedy", "funny", "humor", "skit"]): return "comedy"
    if any(x in t for x in ["music", "dance", "song", "beat"]): return "entertainment"
    return "general"

def generate_metrics():
    """Simulate realistic content performance metrics."""
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
    """Generate topic-based hashtags."""
    words = [w.capitalize() for w in topic.split() if len(w) > 3]
    base_tags = ["#FYP", "#Viral", "#TikTokTrend"]
    category_tags = {
        "food": ["#FoodTok", "#CookingTips", "#Tasty", "#ChefMode", "#RecipeIdeas"],
        "health": ["#HealthyLiving", "#Wellness", "#FitnessTips", "#Nutrition", "#MindBody"],
        "fashion": ["#OOTD", "#StyleTok", "#TrendAlert", "#FashionTips", "#OutfitInspo"],
        "motivation": ["#Motivation", "#DailyInspiration", "#Mindset", "#GrindMode", "#GoalGetter"],
        "education": ["#LearnOnTikTok", "#StudyTok", "#DidYouKnow", "#QuickTips", "#Knowledge"],
        "comedy": ["#FunnyTok", "#LOL", "#ComedyVideo", "#Relatable", "#Skits"],
        "entertainment": ["#DanceTok", "#MusicTrend", "#BeatSync", "#Perform", "#ShowTime"],
        "general": ["#ForYou", "#ExplorePage", "#Creators", "#TrendingNow", "#ContentTips"],
    }
    selected = category_tags.get(category, category_tags["general"])
    custom_tags = [f"#{w}" for w in words[:4]]
    hashtags = base_tags + selected[:5] + custom_tags
    return list(dict.fromkeys(hashtags))[:10]

def generate_best_time(category):
    """Suggest optimal posting times based on category."""
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
    """Create professional short-form caption."""
    return f"{topic.title()} — a quick insight into the world of {category}. Keep watching for more valuable moments."

def generate_description(topic, category):
    """Create longer descriptive paragraph for TikTok or YouTube use."""
    return (
        f"This video dives into {topic}. Whether you're interested in {category} trends, insights, "
        f"or inspiration, this short clip highlights key ideas that resonate with today's TikTok audience. "
        "Watch till the end for the full experience and don’t forget to like, comment, and follow for more."
    )

def generate_keywords(topic, category):
    """Generate SEO keywords."""
    base = topic.lower().split()
    extras = [category, "TikTok", "viral", "trending", "short video", "algorithm"]
    keywords = list(dict.fromkeys(base + extras))
    return ", ".join(keywords[:12])

def generate_feedback(category):
    """Strategic improvement recommendations."""
    base = [
        "Keep the video length concise (under 20 seconds).",
        "Maintain clear visual focus — avoid cluttered backgrounds.",
        "Add clear subtitles for accessibility and engagement.",
        "Start with a strong hook within the first 2 seconds.",
        "Encourage comments or questions to drive interaction.",
        "Use consistent posting patterns to build audience habit.",
    ]
    if category == "comedy":
        base.append("Ensure your punchline lands at the end for maximum replays.")
    if category == "education":
        base.append("Simplify explanations with on-screen text or diagrams.")
    if category == "fashion":
        base.append("Use good lighting and stable framing for outfit clarity.")
    if category == "health":
        base.append("Base your claims on credible facts to build trust.")
    if category == "food":
        base.append("Include close-up shots and show preparation steps clearly.")
    random.shuffle(base)
    return base[:6]

# ---------------------------------------
# MAIN INTERFACE
# ---------------------------------------
uploaded_file = st.file_uploader("Upload your TikTok video", type=["mp4", "mov"])

if uploaded_file:
    topic = extract_topic(uploaded_file.name)
    category = classify_category(topic)
    st.video(uploaded_file)
    st.info(f"Detected topic: {topic.title()}  |  Category: {category.title()}")

    with st.spinner("Analyzing video content and generating insights..."):
        time.sleep(3)
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
    st.download_button("Download Full Report", report, file_name="tiktok_analysis_report.txt")

else:
    st.info("Upload a TikTok video file to begin the analysis.")
