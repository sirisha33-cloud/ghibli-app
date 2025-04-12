import streamlit as st
import streamlit_authenticator as stauth
from diffusers import StableDiffusionPipeline
import torch
import bcrypt
from io import BytesIO

# ===== Login Setup =====
names = ['Siri', 'Guest']
usernames = ['siri123', 'guest_user']

# Replace with hashed passwords generated using bcrypt
hashed_pw
    'sirish97@3 => $2b$12$Cut8lVQeKRbuA826F1odzu0BAwfcRTLoYNr3pUsBSgAhlV.O0Yguu', # for 'siri33'
sirisH3@97 => $2b$12$5wNTCvCRLD/GXvIlGcAMo.JwOnsBZqhpqnPqipygeqtjatdwZsG4e',  # for 'guest44'
credentials = {
    "usernames": {
        "siri123": {"name": "Siri", "password": hashed_pw[0]},
        "guest_user": {"name": "Guest", "password": hashed_pw[1]},
    }
}

authenticator = stauth.Authenticate(
    credentials, 'ghibli_login', 'cookie_key', cookie_expiry_days=1
)

# Login UI
name, auth_status, username = authenticator.login('Login', 'main')

if auth_status == False:
    st.error("❌ Incorrect username or password")
elif auth_status == None:
    st.warning("👋 Please enter your credentials")
elif auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name} 👋")

    # ==== Ghibli App ====
    st.set_page_config(page_title="Ghibli Image Generator", layout="centered")
    st.title("✨ Studio Ghibli-Style Image Generator")
    st.markdown("Generate magical images in the soft, whimsical style of Studio Ghibli!")

    user_prompt = st.text_input("Enter your prompt:", "a magical forest with a cozy house, Studio Ghibli style")

    @st.cache_resource(show_spinner=True)
    def load_model():
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32
        ).to("cpu")
        return pipe

    pipe = load_model()

    if st.button("Generate Image"):
        with st.spinner("Creating your Ghibli world... 🎨"):
            image = pipe(user_prompt).images[0]
            st.image(image, caption="Your Ghibli-style masterpiece", use_column_width=True)

            # Save to buffer
            buf = BytesIO()
            image.save(buf, format="PNG")
            byte_im = buf.getvalue()

            # Download button
            st.download_button(
                label="📥 Download Image",
                data=byte_im,
                file_name="ghibli_style.png",
                mime="image/png"
            )
            st.success("Done! You can download or try another prompt.")

