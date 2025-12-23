import streamlit as st
from groq import Groq
from fpdf import FPDF

st.set_page_config(page_title="Hunter Script Generator", layout="centered")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🎬 AI VIRAL SCRIPT HUNTER v2.1")
st.caption("Reels & Shorts | Sharp Hinglish | PDF Export")

# --- SECRETS & CLIENT ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Bhai, Secrets mein 'GROQ_API_KEY' daalo!")
    GROQ_KEY = None

# --- PDF CREATOR ---
def create_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Hunter Viral Script", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", size=12)
    safe_text = script_text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 8, safe_text)
    return pdf.output(dest="S").encode("latin-1")

# --- AI CALL ---
def get_viral_script(topic, platform, tone):
    prompt = f"""
You are an expert Indian short-form content writer.
Write in clean Hinglish (English letters only, no mixed broken Hindi).
No spelling mistakes, no extra filler words.

Topic: {topic}
Platform: {platform}
Tone: {tone}

Output format (exactly follow):

1) Hooks:
- Hook 1: ...
- Hook 2: ...
- Hook 3: ...

2) Main Script (max 8 lines, bullet points):
- Line 1 ...
- Line 2 ...
...

3) Call To Action (1 line):
- CTA: ...

Keep lines short, punchy and camera-friendly.
"""
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

# --- UI INPUTS ---
topic = st.text_area(
    "Topic (e.g. 5 Habits for Lazy Students)",
    placeholder="5 Habits to Fix Your Lazy Routine in 2025",
)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Platform", ["Instagram Reel", "YouTube Short"])
with col2:
    tone = st.selectbox("Tone", ["Desi/Funny", "Serious/Educational", "Hustler"])

# --- GENERATE ---
if st.button("🚀 GENERATE SHARP SCRIPT"):
    if not topic:
        st.warning("Bhai, topic toh daal pehle!")
    elif not GROQ_KEY:
        st.error("API key missing hai!")
    else:
        with st.spinner("Hunter AI script polish kar raha hai..."):
            raw_script = get_viral_script(topic, platform, tone)

        st.markdown("---")
        st.subheader("📝 Final Script (Hooks + Bullet Points)")
        st.write(raw_script)

        # PDF Download
        pdf_bytes = create_pdf(raw_script)
        st.download_button(
            label="📄 Download Script as PDF",
            data=pdf_bytes,
            file_name="hunter_viral_script.pdf",
            mime="application/pdf",
        )

st.info("Tip: Pehle sirf Hooks test karo Reels me. Jo hook sabse zyada retention de, usko main script bana do.")
