import time
from datetime import datetime

import streamlit as st

from configuracion import supabase, CATEGORIAS, PLAYAS


def pagina_crear():
    if not st.session_state.get("logged_in"):
        st.warning(
            "Debes iniciar sesión para crear un reporte."
        )

        if st.button("Ir a iniciar sesión"):
            st.session_state["pagina"] = "login"
            st.rerun()

        return

    st.markdown(
        '<div class="page-title">'
        'CREAR REPORTE'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-subtitle">
            Proporciona los detalles de la problemática
            para que las autoridades y la comunidad
            puedan actuar.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    titulo = st.text_input(
        "Título del reporte",
        placeholder="Ej. Basura en la orilla",
    )

    col1, col2 = st.columns(2)

    with col1:
        categoria = st.selectbox(
            "Categoría",
            CATEGORIAS,
        )

    with col2:
        ubicacion = st.selectbox(
            "Playa / Ubicación",
            PLAYAS,
        )

    descripcion = st.text_area(
        "Descripción del problema",
        placeholder=(
            "Describe detalladamente "
            "lo que observaste"
        ),
        height=120,
    )

    archivo = st.file_uploader(
        "Evidencia visual — PNG, JPG, MP4",
        type=[
            "png",
            "jpg",
            "jpeg",
            "gif",
            "mp4",
            "webm",
            "mov",
        ],
    )

    col_cancelar, col_enviar = st.columns(2)

    with col_cancelar:
        if st.button(
            "Cancelar",
            use_container_width=True,
        ):
            st.session_state["pagina"] = "tablon"
            st.rerun()

    with col_enviar:
        if st.button(
            "Enviar reporte",
            use_container_width=True,
            type="primary",
        ):
            if not titulo or not descripcion:
                st.error(
                    "Título y descripción son obligatorios."
                )
                return

            imagen_url = None
            video_url = None

            if archivo:
                try:
                    archivo_bytes = archivo.getvalue()

                    extension = (
                        archivo.name
                        .split(".")[-1]
                        .lower()
                    )

                    nombre_archivo = (
                        f"reporte_"
                        f"{st.session_state['usuario_id']}_"
                        f"{int(datetime.now().timestamp())}."
                        f"{extension}"
                    )

                    bucket = supabase.storage.from_(
                        "reportes-imagenes"
                    )

                    bucket.upload(
                        nombre_archivo,
                        archivo_bytes,
                        file_options={
                            "content-type": archivo.type,
                            "upsert": "true",
                        },
                    )

                    url_publica = bucket.get_public_url(
                        nombre_archivo
                    )

                    if extension in [
                        "mp4",
                        "webm",
                        "mov",
                    ]:
                        video_url = url_publica

                    else:
                        imagen_url = url_publica

                except Exception as e:
                    st.error(
                        "No se pudo subir la "
                        f"evidencia visual: {e}"
                    )

                    st.stop()

            (
                supabase.table("reportes")
                .insert(
                    {
                        "usuario_id":
                            st.session_state["usuario_id"],

                        "titulo":
                            titulo,

                        "ubicacion":
                            ubicacion,

                        "categoria":
                            categoria,

                        "descripcion":
                            descripcion,

                        "imagen_url":
                            imagen_url,

                        "video_url":
                            video_url,

                        "me_sirve":
                            0,

                        "no_me_sirve":
                            0,
                    }
                )
                .execute()
            )

            st.success(
                "Reporte enviado exitosamente."
            )

            time.sleep(1.2)

            st.session_state["pagina"] = "tablon"

            st.rerun()