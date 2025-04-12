import streamlit_authenticator as stauth
import streamlit as st
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch

# ===== LOGIN SETUP =====
names = ['Siri', 'Demo User']
usernames = ['siri123', 'demo']

# Hashed passwords for 'abc123' and 'demo123'
hashed_pw = [
    '$2b$12$KIXU2ZRzVj1PaZJ2Q0OE1ugNvwfvEkT5YQetbZq8zhNbyV7NHF8Xu',  # abc123
    '$2b$12$zXh7B7Xp5ak8nF5guE/JauWKHZwSVhh.zOKO.QnA9LQv6mvHjL0fy'   # demo123
]

authenticator = stauth.Authenticate(
    names, usernames, hashed_pw,
    'ghibli_login', 'abcdef', cookie_expiry_days=1
)

name, auth_status, username = authenticator.login('Login', 'main')

if auth_status == False:
    st.error("❌ Incorrect username or password")
    st.stop()
elif auth_status == None:
    st.warning("👋 Please enter your credentials")
    st.stop()
elif auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name} 👋")

    # ===== GHIBLI APP =====
    st.set_page_config(page_title="Ghibli Image Generator 🎨", layout="centered")
    st.title("✨ Ghibli-Style Image Generator (img2img)")
    st.markdown("Upload a photo or use a blank canvas and bring it to life — Ghibli style!")

    # ===== Free Usage Limit =====
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0

    is_paid_user = username == "siri123"  # ✅ this user has unlimited access

    if not is_paid_user and st.session_state.gen_count >= 3:
        st.warning("🚫 You've reached your free generation limit.")
        st.markdown("[🔓 Buy Unlimited Access](https://buy.stripe.com/test_6oE6rb83p3lv8Oc3cc)")
        st.stop()

    # ===== Prompt & Upload =====
    user_prompt = st.text_input("Enter your prompt:",
        "a magical forest with a cozy house, Studio Ghibli style")

    uploaded_image = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])

    # ===== Load Model =====
    def load_model():
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float32
        ).to("cpu")
        return pipe

    pipe = load_model()

    # ===== Generate Image =====
    if st.button("Generate Image"):
        with st.spinner("Creating your Ghibli-style image... ✨"):
            if uploaded_image:
                init_image = Image.open(uploaded_image).convert("RGB").resize((512, 512))
            else:
                init_image = Image.new("RGB", (512, 512), (255, 255, 255))  # blank canvas

            image = pipe(prompt=user_prompt, image=init_image, strength=0.75, guidance_scale=7.5).images[0]
            st.image(image, caption="Your Ghibli-style masterpiece", use_column_width=True)

            image.save("generated_ghibli.png")
            with open("generated_ghibli.png", "rb") as f:
                st.download_button(
                    label="📥 Download Image",
                    data=f,
                    file_name="ghibli_image.png",
                    mime="image/png"
                )

            if not is_paid_user:
                st.session_state.gen_count += 1

            st.success("Done! You can download or generate again.")
