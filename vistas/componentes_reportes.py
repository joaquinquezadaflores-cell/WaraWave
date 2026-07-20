import streamlit as st

from utilidades import format_fecha, texto_seguro


def nombre_ubicacion(reporte: dict) -> str:
    ubicacion = str(reporte.get("ubicacion") or "Sin ubicación")
    detalle = str(reporte.get("ubicacion_detalle") or "").strip()
    return f"{ubicacion} — {detalle}" if detalle else ubicacion


def mostrar_detalle_reporte(reporte: dict) -> None:
    st.markdown("#### Descripción")
    st.write(reporte.get("descripcion", ""))

    latitud = reporte.get("latitud")
    longitud = reporte.get("longitud")
    if latitud is not None and longitud is not None:
        st.markdown("#### Ubicación registrada")
        st.map(
            [{"lat": float(latitud), "lon": float(longitud)}],
            zoom=14,
            use_container_width=True,
        )
        st.caption(f"Coordenadas: {float(latitud):.6f}, {float(longitud):.6f}")

    imagen_url = reporte.get("imagen_url")
    video_url = reporte.get("video_url")
    if imagen_url and str(imagen_url).strip():
        st.markdown("#### Evidencia visual")
        st.image(imagen_url, use_container_width=True)
    elif video_url and str(video_url).strip():
        st.markdown("#### Evidencia visual")
        st.video(video_url)
    else:
        st.caption("Este reporte no tiene evidencia visual adjunta.")


def encabezado_reporte(reporte: dict, estado: str | None = None) -> None:
    titulo = texto_seguro(reporte.get("titulo", "Sin título"))
    categoria = texto_seguro(reporte.get("categoria", ""))
    ubicacion = texto_seguro(nombre_ubicacion(reporte))
    fecha = texto_seguro(format_fecha(reporte.get("fecha", "")))
    estado_html = (
        f'<span class="rbadge status-badge">{texto_seguro(estado)}</span>'
        if estado
        else ""
    )

    st.markdown(
        f"""
        <div class="rtitle">{titulo}</div>
        <div class="rmeta">{fecha} &nbsp;|&nbsp; {ubicacion}</div>
        <span class="rbadge">{categoria}</span>
        {estado_html}
        """,
        unsafe_allow_html=True,
    )
