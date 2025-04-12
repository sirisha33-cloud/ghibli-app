import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

st.set_page_config(page_title="Ghibli Image Generator 🎨", layout="centered")
st.title("✨ Studio Ghibli-Style Image Generator")
st.markdown("Generate magical images in the soft, whimsical style of Studio Ghibli!")

user_prompt = st.text_input("Enter your prompt:", "a magical forest with a cozy house, Studio Ghibli style")

def load_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float32
    ).to("cpu")
    return pipe

pipe = load_model()

if st.button("Generate Image"):
    with st.spinner("Creating magic... 🧚‍♀️"):
        image = pipe(user_prompt).images[0]
        st.image(image, caption="Your Ghibli-style masterpiece", use_column_width=True)
        image.save("generated_ghibli.png")
        st.success("Done! You can download or regenerate.")
