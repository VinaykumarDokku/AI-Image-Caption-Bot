import streamlit as st
from PIL import Image
from transformers import pipeline

st.set_page_config(
    page_title="AI Image Caption Bot",
    page_icon="📸",
    layout="centered"
)

@st.cache_resource
def load_model():
    return pipeline(
        "image-to-text",
        model="Salesforce/blip-image-captioning-base"
    )

st.title("📸 AI Image Caption Bot")
st.write("Generate natural-language captions for your images using AI.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("Generate Caption", type="primary"):
        try:
            with st.spinner("Analyzing image..."):
                captioner = load_model()
                result = captioner(image)
                caption = result[0]["generated_text"]

            st.success("Caption generated successfully!")
            st.write("**AI-Generated Caption:**")
            st.info(caption)

        except Exception as error:
            st.error(f"Caption generation failed: {error}")

st.divider()
st.caption("AI Image Caption Bot | Python • Streamlit • Transformers")
