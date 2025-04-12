import streamlit_authenticator as stauth
import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# ===== LOGIN SETUP =====
names = ['Siri', 'Demo User']
usernames = ['siri123', 'demo']
passwords = ['abc123', 'demo123']

hashed_pw = stauth.Hasher(passwords).generate()

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
    st.title("✨ Studio Ghibli-Style Image Generator")
    st.markdown("Generate magical images in the soft, whimsical style of Studio Ghibli!")

    user_prompt = st.text_input("Enter your prompt:",
        "a magical forest with a cozy house, Studio Ghibli style")

    # == FREE LIMIT CHECK ==
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0

    # Simulate: only 'siri123' is a paying user
    is_paid_user = username == "siri123"

    if not is_paid_user and st.session_state.gen_count >= 3:
        st.warning("🚫 You've reached your free limit.")
        st.markdown("[🔓 Buy Unlimited Access](https://buy.stripe.com/test_6oE6rb83p3lv8Oc3cc)")
        st.stop()

    # == MODEL LOADER ==
    def load_model():
        pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float32
        ).to("cpu")
        return pipe

    pipe = load_model()

    # == GENERATE IMAGE ==
    if st.button("Generate Image"):
        with st.spinner("Creating magic... 🧚‍♀️"):
            image = pipe(user_prompt).images[0]
            st.image(image, caption="Your Ghibli-style masterpiece", use_column_width=True)

            # Save for download
            image.save("generated_ghibli.png")
            with open("generated_ghibli.png", "rb") as f:
                st.download_button(
                    label="📥 Download Image",
                    data=f,
                    file_name="ghibli_image.png",
                    mime="image/png"
                )

            # Track usage for free users
            if not is_paid_user:
                st.session_state.gen_count += 1

            st.success("Done! You can download or regenerate.")


