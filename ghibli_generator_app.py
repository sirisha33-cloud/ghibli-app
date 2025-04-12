import streamlit as st
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
import io

st.set_page_config(page_title="Ghibli Image Generator 🎨", layout="centered")
st.title("✨ AI Art Generator — Ghibli & More")
st.markdown("Create magical artwork from a prompt or photo in styles like Ghibli, Pixar, Watercolor, and more!")

# 🎨 Style selector
style = st.selectbox("Choose a style:", [
    "Studio Ghibli",
    "Pixar",
    "Cyberpunk",
    "Watercolor",
    "Fantasy"
])

style_prompts = {
    "Studio Ghibli": "in the style of Studio Ghibli",
    "Pixar": "in the style of Pixar animation",
    "Cyberpunk": "in a futuristic neon cyberpunk city",
    "Watercolor": "in dreamy watercolor painting style",
    "Fantasy": "in epic high-fantasy concept art style"
}

# 🖊️ Prompt input
prompt_input = st.text_input("Describe your scene:",
    f"a cozy village in the mountains {style_prompts[style]}"
)

# 🖼️ Image upload (optional)
uploaded_img = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])

@st.cache_resource(show_spinner=True)
def load_model():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float32
    ).to("cpu")
    return pipe

pipe = load_model()

if st.button("🎨 Generate Image"):
    with st.spinner("Creating your artwork..."):
        init_image = None
        if uploaded_img:
            init_image = Image.open(uploaded_img).convert("RGB").resize((512, 512))
        else:
            # If no image, use blank image as base
            init_image = Image.new("RGB", (512, 512), (255, 255, 255))

        image = pipe(prompt=prompt_input, image=init_image, strength=0.75, guidance_scale=7.5).images[0]
        st.image(image, caption=f"{style} Style Result", use_column_width=True)

        # 💾 Download button
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        st.download_button("Download Image", data=buf.getvalue(), file_name="ai_art.png", mime="image/png")
