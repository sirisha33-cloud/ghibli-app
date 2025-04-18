import streamlit as st
import streamlit_authenticator as stauth
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
from io import BytesIO

# ==== Streamlit page config ====
st.set_page_config(page_title="Ghibli Image Generator 🎨", layout="centered")

# ==== Login Setup ====
names = ['Siri', 'Guest']
usernames = ['siri123', 'guest_user']

# Hashed passwords for: sirish97@3, sirisH3@97
hashed_pw = [
    '$2b$12$GHIjwfBiUGZjZ/Pz/SZYT.TMIqjD70AR82.HYTN.gM3e39wl5umUW',  # sirish97@3
    '$2b$12$BK155do45Lk7TDjII93imuxvDWfYj.pDhLwfpqRljub8vRAMDgoJa'   # sirisH3@97
]

credentials = {
    "usernames": {
        usernames[0]: {"name": names[0], "password": hashed_pw[0]},
        usernames[1]: {"name": names[1], "password": hashed_pw[1]},
    }
}

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="ghibli_login",
    key="abcdef",
    cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status == False:
    st.error("❌ Incorrect username or password")
    st.stop()
elif auth_status == None:
    st.warning("👋 Please enter your credentials")
    st.stop()
elif auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome, {name} 👋")

    # ==== UI ====
    st.title("✨ Ghibli-Style Image Generator (img2img)")
    st.markdown("Upload an image or use a blank canvas. Enter your prompt and create Ghibli-style art!")

    # ==== Prompt & Upload ====
    user_prompt = st.text_input("Enter your prompt:",
        "a magical forest with a cozy house, Studio Ghibli style")

    uploaded_image = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])

    # ==== Limit for guest users ====
    if "gen_count" not in st.session_state:
        st.session_state.gen_count = 0

    is_paid_user = username == "siri123"
    if not is_paid_user and st.session_state.gen_count >= 3:
        st.warning("🚫 You've used all 3 free generations.")
        st.markdown("[🔓 Buy Unlimited Access](https://buy.stripe.com/test_6oE6rb83p3lv8Oc3cc)")
        st.stop()

    # ==== Load model ====
    @st.cache_resource(show_spinner=True)
    def load_model():
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32
        ).to("cpu")  # ✅ Using CPU only
        return pipe

    pipe = load_model()

    # ==== Generate Image ====
    if st.button("Generate Image"):
        with st.spinner("Creating your Ghibli-style artwork... ✨"):
            if uploaded_image:
                init_image = Image.open(uploaded_image).convert("RGB").resize((512, 512))
            else:
                init_image = Image.new("RGB", (512, 512), (255, 255, 255))  # Blank canvas

            image = pipe(prompt=user_prompt, image=init_image, strength=0.75, guidance_scale=7.5).images[0]

            st.image(image, caption="Your Ghibli-style masterpiece", use_column_width=True)

            # Save image and offer download
            buf = BytesIO()
            image.save(buf, format="PNG")
            st.download_button(
                label="📥 Download Image",
                data=buf.getvalue(),
                file_name="ghibli_image.png",
                mime="image/png"
            )

            st.session_state.gen_count += 1


