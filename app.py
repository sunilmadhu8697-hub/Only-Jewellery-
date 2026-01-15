import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Jewellery Prompt Generator",
    page_icon="💎",
    layout="centered"
)

# ---------------- GEMINI API ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- UI ----------------
st.title("💎 Jewellery Image → Luxury Prompt")
st.write("Upload a jewellery image and generate a premium image-generation prompt.")

uploaded_image = st.file_uploader(
    "Upload Jewellery Image",
    type=["jpg", "jpeg", "png"]
)

background = st.selectbox(
    "Background Style",
    ["Dark Matte Black", "Royal Navy Blue", "Champagne Beige", "Soft Gradient"]
)

lighting = st.selectbox(
    "Lighting Style",
    ["Soft Cinematic Studio Light", "Warm Luxury Lighting", "Editorial High-End Light"]
)

mood = st.selectbox(
    "Mood",
    ["Luxury", "Royal", "Minimal", "Premium Brand"]
)

generate_btn = st.button("Generate Prompt")

# ---------------- GEMINI LOGIC ----------------
if generate_btn:

    if uploaded_image is None:
        st.warning("Please upload a jewellery image.")
    else:
        image = Image.open(uploaded_image)

        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
You are a professional luxury jewelry photography prompt engineer.

Analyze the uploaded jewelry image and WRITE a single high-quality image-generation prompt.

Rules:
- Keep the jewelry design EXACTLY the same
- Do not change shape, stones, or structure

Photography Style:
Background: {background}
Lighting: {lighting}
Mood: {mood}

Quality:
Ultra sharp focus
Photorealistic
Luxury editorial jewelry photography
Clean background
High-end brand look

Output ONLY the final prompt text.
Do NOT include explanations.
"""

        response = model.generate_content(
            [prompt, image],
            generation_config={"temperature": 0.4}
        )

        st.success("Luxury prompt generated!")

        st.text_area(
            "Generated Prompt (Copy & Use)",
            response.text.strip(),
            height=260
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Powered by Google Gemini • Jewellery Prompt Generator")
