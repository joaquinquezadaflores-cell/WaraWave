import streamlit as st
from supabase import create_client
import cv2
from PIL import Image
import requests
import numpy as np

st.title("WaraWave")

try:
  
    url = st.secrets["connections"]["supabase"]["url"]
    key = st.secrets["connections"]["supabase"]["key"]
 
    supabase = create_client(url, key)

    respuesta = supabase.table("usuarios").select("*").execute()
    
    st.success("Conexión exitosa con Supabase")
    st.write(respuesta.data)

    st.write("ingrese la imagen de su reporte")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
    else:
        image = Image.open(requests.get("https://picsum.photos/200/120", stream=True).raw)

    edges = cv2.Canny(np.array(image), 100, 200)
    tab = st.tabs(["Imagen"])
    tab.image(image, use_column_width=True)
    
except Exception as e:
    st.error(f"Error: {e}")
