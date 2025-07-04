import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from files import Files


@st.cache_resource
def load_model():
    """
    Load the YOLO model.
    """
    model = YOLO(Files.RUNS_WEIGHTS_BEST_PT)
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

        # Get the predicted class
        if results[0].probs is not None:
            predicted_index = np.argmax(results[0].probs.data).item()
            print(f"Predicted Index: {predicted_index}")
            predicted_class = model.names[predicted_index]
            st.write(f"Predicted Class: {predicted_class}")
        else:
            st.write("No predictions were made.")

if __name__ == "__main__":
    main()