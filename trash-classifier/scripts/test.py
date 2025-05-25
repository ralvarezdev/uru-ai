import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

from scripts import RUNS_WEIGHTS_BEST_PT


@st.cache_resource
def load_model():
    """
    Load the YOLO model.
    """
    model = YOLO(RUNS_WEIGHTS_BEST_PT)
    return model

def main():
    st.title("YOLO Inference with Streamlit")
    st.write("Upload an image to perform object detection using YOLO.")

    # Load the YOLO model
    model = load_model()

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Read the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to numpy array
        image_np = np.array(image)

        # Perform inference
        results = model(image_np)

        # Display the classification results
        st.write("Detection Results: " + results)

if __name__ == "__main__":
    main()