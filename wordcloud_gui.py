import streamlit as st
from wordcloud import WordCloud
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="WordCloud Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- HEADER ----
st.markdown(
    """
    <h1 style="text-align:center; color:#2E86C1; font-family:sans-serif;">
        WordCloud Visualizer
    </h1>
    """, unsafe_allow_html=True
)

# ---- SIDEBAR ----
st.sidebar.header("📥 Upload Files")

text_file = st.sidebar.file_uploader("Upload Text File (.txt)", type=["txt"])
mask_file = st.sidebar.file_uploader("Upload Mask Image (PNG/JPG)", type=["png","jpg","jpeg"])

generate = st.sidebar.button("Generate WordCloud")

# ---- DISPLAY PANELS ----
col1, col2 = st.columns(2)

# Show waiting message initially
if not generate:
    with col1:
        st.markdown(
            """
            <div style="text-align:center; padding:40px; background:#f8f9fa; border-radius:15px; border:2px dashed #ddd; margin:10px;">
                <p style="font-size:60px; margin:0;">☁️</p>
                <h3 style="color:#2E86C1; margin:15px 0 5px 0;">Normal WordCloud</h3>
                <p style="color:#888; font-size:14px; margin:0;">Waiting for input...</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="text-align:center; padding:40px; background:#f8f9fa; border-radius:15px; border:2px dashed #ddd; margin:10px;">
                <p style="font-size:60px; margin:0;">🎭</p>
                <h3 style="color:#2E86C1; margin:15px 0 5px 0;">Mask WordCloud</h3>
                <p style="color:#888; font-size:14px; margin:0;">Waiting for input...</p>
            </div>
            """, unsafe_allow_html=True
        )

# ---- GENERATION ----
if generate:
    if text_file is None:
        st.error("❗ Please upload a text file")
    else:
        text_data = str(text_file.read(), "utf-8")

        # normal wordcloud
        wc = WordCloud(
            background_color="white",
            width=600,
            height=400,
            colormap="viridis"
        ).generate(text_data)

        img_normal = wc.to_image()

        with col1:
            st.markdown(
                """
                <div style="text-align:center; background:#f8f9fa; border-radius:15px; border:2px solid #2E86C1; padding:15px; margin:10px;">
                    <h3 style="color:#2E86C1; margin:0 0 10px 0;">☁️ Normal WordCloud</h3>
                </div>
                """, unsafe_allow_html=True
            )
            st.image(img_normal, use_container_width=True)

        # mask wordcloud
        if mask_file is not None:
            mask = np.array(Image.open(mask_file))

            wc_mask = WordCloud(
                background_color="white",
                mask=mask,
                contour_width=2,
                contour_color="black",
                colormap="plasma"
            ).generate(text_data)

            img_mask = wc_mask.to_image()
            with col2:
                st.markdown(
                    """
                    <div style="text-align:center; background:#f8f9fa; border-radius:15px; border:2px solid #2E86C1; padding:15px; margin:10px;">
                        <h3 style="color:#2E86C1; margin:0 0 10px 0;">🎭 Mask WordCloud</h3>
                    </div>
                    """, unsafe_allow_html=True
                )
                st.image(img_mask, use_container_width=True)
        else:
            with col2:
                st.markdown(
                    """
                    <div style="text-align:center; padding:40px; background:#fff3cd; border-radius:15px; border:2px dashed #ffc107; margin:10px;">
                        <p style="font-size:50px; margin:0;">⚠️</p>
                        <h3 style="color:#856404; margin:15px 0 5px 0;">Mask WordCloud</h3>
                        <p style="color:#856404; font-size:14px; margin:0;">No mask image uploaded</p>
                    </div>
                    """, unsafe_allow_html=True
                )

