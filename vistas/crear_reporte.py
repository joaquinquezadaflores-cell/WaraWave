from pathlib import Path
from uuid import uuid4

import streamlit as st

from configuracion import CATEGORIAS, PLAYAS, obtener_supabase

try:
    from streamlit_geolocation import streamlit_geolocation
except ImportError:  
    streamlit_geolocation = None

MAX_IMAGEN_MB = 8
MAX_VIDEO_MB = 20
EXTENSIONES_VIDEO = {"mp4", "webm", "mov"}
EXTENSIONES_IMAGEN = {"png", "jpg", "jpeg", "gif"}


def _guardar_ubicacion_gps() -> None:
    if streamlit_geolocation is None:
        st.error(
            "Falta instalar streamlit-geolocation. Ejecuta "
            "pip install -r requirements.txt."
        )
        return

    st.markdown("#### Ubicación geográfica")
    st.caption(
        "Presiona el botón de ubicación y autoriza al navegador. "
        "La geolocalización funciona en localhost o mediante HTTPS."
    )

    resultado = streamlit_geolocation()
    if resultado and resultado.get("latitude") is not None:
        st.session_state["gps_reporte"] = {
            "latitud": float(resultado["latitude"]),
            "longitud": float(resultado["longitude"]),
            "precision": resultado.get("accuracy"),
        }

    gps = st.session_state.get("gps_reporte")
    if gps:
        precision = gps.get("precision")
        detalle = (
            f" · precisión aproximada: {precision:.0f} m"
            if isinstance(precision, (int, float))
            else ""
        )
        st.success(
            f"Ubicación registrada: {gps['latitud']:.6f}, "
            f"{gps['longitud']:.6f}{detalle}"
        )
        st.map(
            [{"lat": gps["latitud"], "lon": gps["longitud"]}],
            zoom=14,
            use_container_width=True,
        )


def _subir_evidencia(cliente, archivo, usuario_id):
    if not archivo:
        return None, None

    extension = Path(archivo.name).suffix.lower().lstrip(".")
    if extension not in EXTENSIONES_IMAGEN | EXTENSIONES_VIDEO:
        raise ValueError("Formato de archivo no permitido.")

    tamano_mb = archivo.size / (1024 * 1024)
    limite = MAX_VIDEO_MB if extension in EXTENSIONES_VIDEO else MAX_IMAGEN_MB
    if tamano_mb > limite:
        raise ValueError(
            f"El archivo supera el máximo permitido de {limite} MB."
        )

    nombre_archivo = f"{usuario_id}/{uuid4().hex}.{extension}"
    bucket = cliente.storage.from_("reportes-imagenes")
    bucket.upload(
        nombre_archivo,
        archivo.getvalue(),
        file_options={
            "content-type": archivo.type,
            "upsert": "false",
        },
    )
    url_publica = bucket.get_public_url(nombre_archivo)

    if extension in EXTENSIONES_VIDEO:
        return None, url_publica
    return url_publica, None


def pagina_crear():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para crear un reporte.")
        if st.button("Ir a iniciar sesión"):
            st.session_state["pagina"] = "login"
            st.rerun()
        return

    st.markdown(
        '<div class="page-title">CREAR REPORTE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="page-subtitle">
            Describe el problema, registra el punto exacto y agrega evidencia.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    titulo = st.text_input(
        "Título del reporte",
        placeholder="Ej. Basura acumulada en la orilla",
        max_chars=120,
    )

    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Categoría", CATEGORIAS)
    with col2:
        ubicacion = st.selectbox("Playa / Ubicación", PLAYAS)

    ubicacion_detalle = ""
    if ubicacion == "Otra":
        ubicacion_detalle = st.text_input(
            "Especifica el lugar",
            placeholder="Ej. sector norte de la desembocadura",
            max_chars=160,
        )

    descripcion = st.text_area(
        "Descripción del problema",
        placeholder="Describe detalladamente lo que observaste",
        height=140,
        max_chars=1200,
    )

    archivo = st.file_uploader(
        "Evidencia visual — imagen o video corto",
        type=sorted(EXTENSIONES_IMAGEN | EXTENSIONES_VIDEO),
        help=(
            f"Imágenes: máximo {MAX_IMAGEN_MB} MB. "
            f"Videos: máximo {MAX_VIDEO_MB} MB."
        ),
    )

    _guardar_ubicacion_gps()
    gps = st.session_state.get("gps_reporte")

    col_cancelar, col_enviar = st.columns(2)
    with col_cancelar:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.pop("gps_reporte", None)
            st.session_state["pagina"] = "tablon"
            st.rerun()

    with col_enviar:
        if st.button(
            "Enviar reporte",
            use_container_width=True,
            type="primary",
        ):
            if not titulo.strip() or not descripcion.strip():
                st.error("Título y descripción son obligatorios.")
                return
            if ubicacion == "Otra" and not ubicacion_detalle.strip():
                st.error("Especifica el lugar del reporte.")
                return
            if not gps:
                st.error(
                    "Debes registrar la ubicación geográfica antes de enviar."
                )
                return

            try:
                cliente = obtener_supabase()
                imagen_url, video_url = _subir_evidencia(
                    cliente,
                    archivo,
                    st.session_state["usuario_id"],
                )

                cliente.table("reportes").insert(
                    {
                        "usuario_id": st.session_state["usuario_id"],
                        "titulo": titulo.strip(),
                        "ubicacion": ubicacion,
                        "ubicacion_detalle": ubicacion_detalle.strip() or None,
                        "categoria": categoria,
                        "descripcion": descripcion.strip(),
                        "imagen_url": imagen_url,
                        "video_url": video_url,
                        "latitud": gps["latitud"],
                        "longitud": gps["longitud"],
                        "precision_ubicacion": gps.get("precision"),
                        "me_sirve": 0,
                        "no_me_sirve": 0,
                        "activo": True,
                    }
                ).execute()

                st.session_state.pop("gps_reporte", None)
                st.session_state["reporte_creado"] = True
                st.session_state["pagina"] = "tablon"
                st.rerun()
            except Exception as error:
                st.error(f"No se pudo guardar el reporte: {error}")
