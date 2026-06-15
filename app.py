import streamlit as st
from supabase import create_client

st.title("WaraWave")

try:
  
    url = st.secrets["connections"]["supabase"]["url"]
    key = st.secrets["connections"]["supabase"]["key"]
 
    supabase = create_client(url, key)

    respuesta = supabase.table("usuarios").select("*").execute()
    
    st.success("Conexión exitosa con Supabase")
    st.write(respuesta.data)
    
except Exception as e:
    st.error(f"Error: {e}")
