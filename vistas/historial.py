import streamlit as st

from configuracion import obtener_supabase
from vistas.componentes_reportes import encabezado_reporte, mostrar_detalle_reporte


def pagina_historial():
    if not st.session_state.get("logged_in"):
        st.session_state["pagina"] = "login"
        st.rerun()

    st.markdown(
        '<div class="page-title">MIS REPORTES</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="page-subtitle">
            Historial completo de tus reportes, incluidos los retirados del tablón :)
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    try:
        cliente = obtener_supabase()
        reportes = (
            cliente.table("reportes")
            .select("*")
            .eq("usuario_id", st.session_state["usuario_id"])
            .order("fecha", desc=True)
            .execute()
            .data
            or []
        )
    except Exception as error:
        st.error(f"No fue posible cargar tu historial: {error}")
        return

    if not reportes:
        st.info("Todavía no has creado reportes.")
        return

    visibles = sum(bool(reporte.get("activo", True)) for reporte in reportes)
    col_total, col_visibles, col_retirados = st.columns(3)
    col_total.metric("Total", len(reportes))
    col_visibles.metric("Visibles", visibles)
    col_retirados.metric("Retirados", len(reportes) - visibles)
    st.divider()

    for reporte in reportes:
        activo = bool(reporte.get("activo", True))
        estado = "Visible en el tablón" if activo else "Retirado por moderación"

        with st.expander(
            f"{reporte.get('titulo', 'Sin título')} · {estado}",
            expanded=False,
        ):
            encabezado_reporte(reporte, estado=estado)
            st.caption(
                f"Confirmaciones recibidas: {int(reporte.get('me_sirve') or 0)}"
            )
            mostrar_detalle_reporte(reporte)
