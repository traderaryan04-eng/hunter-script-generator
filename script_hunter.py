import streamlit as st
from groq import Groq

# 1. UI Configuration (Phone par bhi mast dikhega)
st.set_page_config(page_title="Hunter Script Generator", layout="centered")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🎬 AI VIRAL SCRIPT HUNTER v1.0")
st.caption("Commerce to Tech Guy | Viral Reels & Shorts Engine")

# --- 2. SECRETS & AI SETUP ---
try:
    # Nayi app mein bhi 'GROQ_API_KEY' secrets mein dalni hogi
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Bhai, Streamlit Secrets mein 'GROQ_API_KEY' daalo!")
    GROQ_KEY = None

def get_viral_script(topic, platform, tone):
    prompt = f"""
    Topic: {topic}
    Platform: {platform}
    Tone: {tone} (Desi Hinglish style)
    
    Tasks:
    1. Give 3 Viral Hooks (Starting lines to grab attention).
    2. Write a full script (Intro, 3 main points, Outro).
    3. Give 5 Viral Hashtags.
    Character: A student (Commerce to Tech journey). Style: Begusarai Hunter style.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Sabse stable model [web:85]
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- 3. INPUT SECTION ---
with st.container():
    topic = st.text_area("Bhai, topic kya hai? (e.g. Maine AI tool kaise banaya...)", value="", placeholder="Yahan apna idea likho...")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["Instagram Reel", "YouTube Short", "YouTube Long Video"])
    with col2:
        tone = st.selectbox("Tone", ["Desi/Funny", "Serious/Educational", "Hustler/Motivational"])

# --- 4. EXECUTION ---
if st.button("🚀 GENERATE VIRAL SCRIPT"):
    if topic and GROQ_KEY:
        with st.spinner("Hunter AI script likh raha hai..."):
            res = get_viral_script(topic, platform, tone)
            st.markdown("---")
            st.subheader("📝 Your Viral Script")
            st.write(res)
    else:
        st.warning("Bhai, topic dalo aur check karo API key connected hai ya nahi!")

st.info("Hunter Tip: Pehla hook sabse powerful hona chahiye taaki audience scroll na kare! 📸")
