import streamlit as st
from groq import Groq
from fpdf import FPDF

# ---------- 1. BASIC SETUP ----------
st.set_page_config(page_title="Hunter Script Generator", layout="centered")
st.markdown(
    "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>",
    unsafe_allow_html=True,
)

st.title("🎬 AI VIRAL SCRIPT HUNTER v3.0")
st.caption("Reels + Shorts + Long Video | Sharp Hinglish | PDF Export")

# ---------- 2. GROQ CLIENT ----------
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_KEY)
except Exception:
    GROQ_KEY = None
    st.error("Bhai, Streamlit Secrets mein 'GROQ_API_KEY' daalna mat bhoolna!")

# ---------- 3. PDF CREATOR ----------
def create_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Hunter Viral Script", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", size=12)
    safe_text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 8, safe_text)

    return pdf.output(dest="S").encode("latin-1")

# ---------- 4. AI CALL ----------

def build_prompt(topic: str, platform: str, tone: str) -> str:
    base_header = """
You are an expert Indian content writer for YouTube & Instagram.
Write in clean Hinglish (English letters only, NO Hindi script).
Avoid spelling mistakes, no broken words, no overlong sentences.
Always format output exactly as requested.
"""

    if platform in ["Instagram Reel", "YouTube Short"]:
        mode_block = f"""
FORMAT: SHORT FORM SCRIPT (30–45 sec)

Topic: {topic}
Platform: {platform}
Tone: {tone}

Output format:

1) Hooks (3 lines):
- Hook 1: ...
- Hook 2: ...
- Hook 3: ...

2) Main Script (max 8 lines, bullet points):
- Line 1 ...
- Line 2 ...
- Line 3 ...
- Line 4 ...
- Line 5 ...
- Line 6 ...
- Line 7 ...
- Line 8 ...

3) Call To Action (1 line):
- CTA: ...

Rules:
- Lines should be punchy and direct, like you are talking to the camera.
- No extra explanation text outside this structure.
"""
    else:
        # YouTube Long Video
        mode_block = f"""
FORMAT: LONG FORM SCRIPT (8–10 minute talking video)

Topic: {topic}
Platform: {platform}
Tone: {tone}

Output format:

1) Title:
- One YouTube title idea (max 80 characters).

2) Hook (30–40 sec):
- 2–3 short sentences that create curiosity and pain.

3) Introduction:
- 3–4 bullets: who am I + why this topic matters for the viewer.

4) Main Sections (3–5 points):
For each section use this pattern:
- Section X: Name of the point
  - Story: 2–3 lines (relatable example).
  - Lesson: 1–2 lines (key idea).
  - Steps:
    - Step 1 ...
    - Step 2 ...
    - Step 3 ...

5) Mini Recap:
- 3–5 bullets summarising the main lessons.

6) Strong CTA:
- 1 line: ask to like/subscribe + tease next video.

Rules:
- Use bullet points exactly as shown.
- Keep sentences short and camera-friendly.
- No extra commentary outside this structure.
"""
    return base_header + mode_block

def get_script(topic: str, platform: str, tone: str) -> str:
    prompt = build_prompt(topic, platform, tone)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

# ---------- 5. UI INPUTS ----------

topic = st.text_area(
    "Topic (e.g. 5 Habits for Lazy Students)",
    placeholder="5 Habits to Fix Your Lazy Routine in 2025",
)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox(
        "Platform",
        ["Instagram Reel", "YouTube Short", "YouTube Long Video"],
    )
with col2:
    tone = st.selectbox(
        "Tone",
        ["Desi/Funny", "Serious/Educational", "Hustler/Motivational"],
    )

# ---------- 6. GENERATE + PDF ----------

if st.button("🚀 GENERATE VIRAL SCRIPT"):
    if not topic:
        st.warning("Bhai, topic toh daal pehle!")
    elif not GROQ_KEY:
        st.error("API key missing hai, Secrets check kar!")
    else:
        with st.spinner("Hunter AI script likh raha hai..."):
            script_text = get_script(topic, platform, tone)

        st.markdown("---")
        st.subheader("📝 Final Script")
        st.write(script_text)

        pdf_bytes = create_pdf(script_text)
        st.download_button(
            label="📄 Download Script as PDF",
            data=pdf_bytes,
            file_name="hunter_viral_script.pdf",
            mime="application/pdf",
        )

st.info(
    "Tip: Pehle Hooks ko alag se test karo (Reels / Shorts) – jo hook sabse zyada watch time de, uske around long video banao."
)
