import streamlit as st
import base64
from groq import Groq
from PIL import Image
import io

client = Groq(api_key="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")  # your Groq key here

def image_to_text(image_bytes):
    try:
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Describe this image in detail. What do you see?"
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---- UI ----
st.title("🖼️ Image to Text Converter")
st.write("Upload an image and AI will describe what it sees!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    if st.button("Generate Description"):
        with st.spinner("Analyzing image..."):
            result = image_to_text(img_bytes)
        st.subheader("📝 Image Description:")
        st.success(result)
