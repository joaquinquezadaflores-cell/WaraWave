import streamlit as st

st.title("Sistema de Gestión - Playa Segura 🏖️")

# Crear una barra lateral para el menú
opcion = st.sidebar.selectbox("Menú", ["Ver Reportes", "Crear Reporte"])

if opcion == "Crear Reporte":
    st.subheader("Registrar nuevas condiciones de la playa")
    playa = st.text_input("Nombre de la playa")
    estado = st.selectbox("Estado", ["Limpia", "Contaminada", "Flujo Alto"])
    
    if st.button("Enviar Reporte"):
        st.success(f"Reporte de {playa} guardado con éxito.")