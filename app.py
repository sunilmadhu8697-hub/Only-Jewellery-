import streamlit as st
import google.generativeai as genai
import replicate
from PIL import Image
import os

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Jewellery Image to Image AI",
    page_icon="💎",
    layout="centered"
)

st.title("💎 Jewellery Image → Luxury Image")
st.write("Upload a jewellery image and generate a luxury studio-style photo.")

# ---------------- API KEYS ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")

# ---------------- IMAGE UPLOAD ----------------
uploaded_image = st.file_uploader(
    "Upload Jewellery Image",
    type=["jpg", "jpeg", "png"]
)

generate_btn = st.button("Generate Luxury Image")

# ---------------- MAIN LOGIC ----------------
if generate_btn:

    if uploaded_image is None:
        st.warning("Please upload a jewellery image.")
    else:
        # Load image
        image = Image.open(uploaded_image)

        # --------- STEP 1: GEMINI PROMPT ---------
        model = genai.GenerativeModel("gemini-1.5-pro")

        gemini_prompt = """
You are a professional luxury jewelry photography prompt engineer.

Analyze the uploaded jewelry image and write a SINGLE image-generation prompt.

Rules:
- Preserve the exact jewelry design
- Do not change stones, shape, or structure

Photography Style:
Luxury studio product photography
Clean background (black, navy, or champagne)
Soft cinematic lighting
Sharp focus
High-end brand look

Output ONLY the final prompt text.
"""

        gemini_response = model.generate_content(
            [gemini_prompt, image],
            generation_config={"temperature": 0.4}
        )

        final_prompt = gemini_response.text.strip()

        st.subheader("Generated Prompt")
        st.text_area("Prompt", final_prompt, height=180)

        # --------- STEP 2: IMAGE → IMAGE (SDXL) ---------
        with st.spinner("Generating luxury image..."):
            output = replicate.run(
                "stability-ai/sdxl",
                input={
                    "image": uploaded_image,
                    "prompt": final_prompt,
                    "strength": 0.3,
                    "num_inference_steps": 30,
                    "guidance_scale": 7
                }
            )

        st.success("Luxury image generated!")

        st.subheader("Generated Luxury Image")
        st.image(output[0], use_column_width=True)
