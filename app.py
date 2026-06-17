import streamlit as st
from supabase import create_client

st.title("Sistema de Gestión - Playa Segura")

opcion = st.sidebar.selectbox("Menú", ["Ver Reportes", "Crear Reporte"])

if opcion == "Crear Reporte":
    st.subheader("Registrar nuevas condiciones de la playa")

    playa = st.selectbox("Nombre de la playa", ["El Laucho", "La Lisera", "Chinchorro", "Las Machas"])

    foto = st.file_uploader("Sube una foto", type=["jpg", "jpge", "png"])

    descripción = st.text_input("Describa la situación")

    if foto is not None:
        st.image(foto, caption="Vista previa", use_container_width=True)
    
    if st.button("Enviar Reporte"):
        try:
            url = st.secrets["connections"]["supabase"]["url"]
            key = st.secrets["connections"]["supabase"]["key"]

            supabase = create_client(url, key)

            respuesta = supabase.table("usuarios").select("*").execute()
            st.success("Conexión exitosa con Supabase")

        except Exception as e:
            st.error(f"hubo un error conectadose con la base de datos {e}")
            
        try:
            bytes_foto = foto.getvalue()
            nombre_foto = foto.name
            res = supabase.strorage.from_("imagenes_app").upload(
                path=nombre_foto,
                file=bytes_foto,
                file_options={"content-type": foto.type}    
            )
            st.success(f"Reporte de {playa} guardado con éxito.")

        except Exception as e:
            st.error(f"hubo un error al subir el reporte: {e}")
