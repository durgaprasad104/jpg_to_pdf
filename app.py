import streamlit as st
from PIL import Image
import io

st.title("JPG to PDF Converter")

uploaded_files = st.file_uploader(
    "Upload JPG images", type=["jpg", "jpeg"], accept_multiple_files=True
)

if st.button("Start New Conversion"):
    st.session_state.cropped_images = []
    st.session_state.added_files = set()
    st.info("Cleared previous data. Please upload new images.")

# Initialize session state to store uploaded images
if "cropped_images" not in st.session_state:
    st.session_state.cropped_images = []
if "added_files" not in st.session_state:
    st.session_state.added_files = set()

if uploaded_files:
    uploaded_names = set([f.name for f in uploaded_files])
    # Reset session state if the uploaded files differ from the previous set
    if uploaded_names != st.session_state.added_files:
        st.session_state.cropped_images = []
        st.session_state.added_files = set()

    for file in uploaded_files:
        if file.name not in st.session_state.added_files:
            image = Image.open(file).convert("RGB")
            st.session_state.cropped_images.append(image)
            st.session_state.added_files.add(file.name)
            st.success(f"Added {file.name}")

    if st.session_state.cropped_images:
        st.write("### Images to be included in PDF:")
        for i, img in enumerate(st.session_state.cropped_images, 1):
            st.image(img, caption=f"Image {i}", width=150)

        if st.button("Generate and Download PDF"):
            pdf_buffer = io.BytesIO()
            imgs = st.session_state.cropped_images
            if len(imgs) == 1:
                imgs[0].save(pdf_buffer, format='PDF')
            else:
                imgs[0].save(pdf_buffer, format='PDF', save_all=True, append_images=imgs[1:])
            pdf_buffer.seek(0)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="Document.pdf",
                mime="application/pdf"
            )
else:
    st.info("Upload one or more JPG images to start.")
