#!/usr/bin/env python
# coding: utf-8

# Skapa en streamlit applikation.

# In[54]:


import streamlit as st
import cv2
import numpy as np
import joblib

# Styling
custom_css = """
<style>
h1 {
    color: darkblue;
}
button {
    background-color: darkblue !important;
    color: white !important;
    border-color: darkblue !important;
}
</style>
"""

# In[55]:

# Download the trained model
loaded_model = joblib.load('model_knn.joblib')

# In[56]:

# Image pre-processing
def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (28, 28), interpolation=cv2.INTER_AREA)
    lower_pixel = 140 
    upper_pixel = 160 
    for i in range(resized_image.shape[0]):
        for j in range(resized_image.shape[1]):
            if resized_image[i, j] <= lower_pixel:
                resized_image[i, j] = 0
            elif resized_image[i, j] > upper_pixel:
                resized_image[i, j] = 255
    resized_image = cv2.bitwise_not(resized_image)
    flattened_image = resized_image.flatten().reshape(1, -1)
    return resized_image, flattened_image

# In[57]:

#Application screen
def main():
    st.title("Streamlit application for determining numbers")
   
    st.markdown(custom_css, unsafe_allow_html=True)#apply my style

    # Upload picture or take picture from camera
    uploaded_file = st.file_uploader("Upload a picture", type=["jpg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
   
    else:
       
        video_capture = cv2.VideoCapture(0)
        _, frame = video_capture.read()
        image = frame[:, :, ::-1]

    # Preprocess the image if defined
    if 'image' in locals():
        preprocessed_image, flattened_image = preprocess_image(image)

        # Preprocessed image 
      
        st.image(preprocessed_image, use_column_width=True)

        # Make prediction with the model
        if st.button('Predict'):
            prediction = loaded_model.predict(flattened_image)
            st.write(f"Predicted digit: {prediction}")

if __name__ == "__main__":
    main()








