import streamlit as st
from groq import Groq
from fpdf import FPDF

# 1. UI Configuration
st.set_page_config(page_title="Hunter Script Generator", layout="centered")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🎬 AI VIRAL SCRIPT HUNTER v2.0")
st.caption("PDF Export | Smart Hooks | Viral Engine")

# --- 2. SECRETS SETUP ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Bhai, Secrets mein 'GROQ_API_KEY' check karo!")
    GROQ_KEY = None

# --- 3. PDF GENERATION FUNCTION ---
def create_pdf(script_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Viral Script - Hunter AI", ln=True, align='C')
    pdf.ln(10)
    
    # Content (Encoding fix for Hinglish)
    pdf.set_font("Arial", size=12)
    # Replace unsupported characters if any
    safe_text = script_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, safe_text)
    
    return pdf.output(dest="S").encode("latin-1")

def get_viral_script(topic, platform, tone):
    prompt = f"""
    Topic: {topic}
    Platform: {platform}
    Tone: {tone} (Desi Hinglish, Short & Punchy)
    
    Structure:
    1. 3 Viral Hooks (Stop scrolling immediately).
    2. The Problem (Relatable pain point).
    3. The Solution (Step-by-step).
    4. Call to Action (CTA).
    
    Format: Use bullet points. Keep sentences short.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"

# --- 4. INPUT SECTION ---
with st.container():
    topic = st.text_area("Topic (e.g. 5 Habits for Lazy Students)", placeholder="Type here...")
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["Instagram Reel", "YouTube Short"])
    with col2:
        tone = st.selectbox("Tone", ["Desi/Funny", "Serious/Educational", "Hustler"])

# --- 5. GENERATE & DOWNLOAD ---
if st.button("🚀 GENERATE SCRIPT"):
    if topic and GROQ_KEY:
        with st.spinner("Writing viral script..."):
            script = get_viral_script(topic, platform, tone)
            
            # Display Script
            st.markdown("---")
            st.subheader("📝 Generated Script")
            st.write(script)
            
            # PDF Download Button
            pdf_bytes = create_pdf(script)
            st.download_button(
                label="📄 Download Script as PDF",
                data=pdf_bytes,
                file_name="viral_script.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Topic daalo bhai!")
