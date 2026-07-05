import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["connections"]["supabase"]["url"]
SUPABASE_KEY = st.secrets["connections"]["supabase"]["key"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


CATEGORIAS = [
    "Contaminación",
    "Fauna",
    "Infraestructura",
    "Seguridad",
    "Otro",
]


PLAYAS = [
    "Playa Laucho",
    "Playa Lisera",
    "Playa Chinchorro",
    "Playa Las Machas",
    "Otra",
]