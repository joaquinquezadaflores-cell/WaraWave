import streamlit as st
from supabase import Client, create_client

SUPABASE_URL = st.secrets["connections"]["supabase"]["url"]
SUPABASE_KEY = st.secrets["connections"]["supabase"]["key"]

CATEGORIAS = [
    "Contaminación",
    "Fauna",
    "Infraestructura",
    "Seguridad",
    "Otro",
]

PLAYAS_COORDENADAS = {
    "Playa Laucho": (-18.4913, -70.3226),
    "Playa Lisera": (-18.4852, -70.3266),
    "Playa Chinchorro": (-18.4585, -70.3128),
    "Playa Las Machas": (-18.4219, -70.3105),
}

PLAYAS = list(PLAYAS_COORDENADAS.keys()) + ["Otra"]

ROL_CIUDADANO = "ciudadano"
ROL_ADMINISTRADOR = "administrador"
ROL_AUTORIDAD = "autoridad"
ROLES_VALIDOS = (ROL_CIUDADANO, ROL_ADMINISTRADOR, ROL_AUTORIDAD)
ROLES_CON_ACCESO_ADMIN = (ROL_ADMINISTRADOR, ROL_AUTORIDAD)


def obtener_supabase() -> Client:
    """entrega un cliente independiente para cada sesion de Streamlit
    
    guardarlo en session_state evita compartir la sesion de Supabase Auth
    entre distintos usuarios conectados a la aplicacion
    """
    if "_supabase_cliente" not in st.session_state:
        st.session_state["_supabase_cliente"] = create_client(
            SUPABASE_URL,
            SUPABASE_KEY,
        )

    return st.session_state["_supabase_cliente"]
