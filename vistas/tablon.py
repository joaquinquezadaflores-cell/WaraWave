import streamlit as st

from configuracion import CATEGORIAS, PLAYAS, obtener_supabase
from vistas.componentes_reportes import encabezado_reporte, mostrar_detalle_reporte


def _confirmaciones_usuario(cliente, usuario_id) -> set:
    respuesta = (
        cliente.table("confirmaciones")
        .select("reporte_id")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    return {fila["reporte_id"] for fila in (respuesta.data or [])}


def pagina_tablon():
    if not st.session_state.get("logged_in"):
        st.session_state["pagina"] = "login"
        st.rerun()

    st.markdown(
        '<div class="page-title">TABLÓN DE REPORTES</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Reportes visibles de toda la comunidad, ordenados desde el más reciente.</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.pop("reporte_creado", False):
        st.success("Reporte enviado exitosamente.")

    try:
        cliente = obtener_supabase()

        respuesta_categorias = (
            cliente.table("reportes")
            .select("categoria")
            .eq("activo", True)
            .execute()
        )

        categorias_reportadas = sorted(
            {
                reporte["categoria"].strip()
                for reporte in (respuesta_categorias.data or [])
                if reporte.get("categoria")
            }
        )

        categorias_base = [
            categoria
            for categoria in CATEGORIAS
            if categoria != "Otro"
        ]

        opciones_categorias = list(
            dict.fromkeys(categorias_base + categorias_reportadas)
        )

    except Exception as error:
        st.error(f"No fue posible cargar las categorías: {error}")
        return

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        filtro_playa = st.selectbox(
            "Playa",
            ["Todas"] + PLAYAS,
        )

    with col2:
        filtro_categoria = st.selectbox(
            "Categoría",
            ["Todas"] + opciones_categorias,
        )



    try:
        query = (
            cliente.table("reportes")
            .select("*")
            .eq("activo", True)
            .order("fecha", desc=True)
        )

        if filtro_playa != "Todas":
            query = query.eq("ubicacion", filtro_playa)
        if filtro_categoria != "Todas":
            query = query.eq("categoria", filtro_categoria)

        reportes = query.execute().data or []
        confirmados = _confirmaciones_usuario(
            cliente,
            st.session_state["usuario_id"],
        )
    except Exception as error:
        st.error(f"No fue posible cargar el tablón: {error}")
        return

    if not reportes:
        st.info("No hay reportes visibles para los filtros seleccionados.")
        return

    usuario_id = st.session_state["usuario_id"]
    for reporte in reportes:
        reporte_id = reporte["id"]
        es_propio = reporte.get("usuario_id") == usuario_id
        ya_confirmado = reporte_id in confirmados
        key_expander = f"exp_{reporte_id}"

        if key_expander not in st.session_state:
            st.session_state[key_expander] = False

        with st.container(border=True):
            encabezado_reporte(reporte)
            st.markdown("<br>", unsafe_allow_html=True)

            col_ver, col_confirmar = st.columns([3, 2])
            with col_ver:
                texto_boton = (
                    "Ocultar detalles"
                    if st.session_state[key_expander]
                    else "Ver detalles"
                )
                if st.button(texto_boton, key=f"toggle_{reporte_id}"):
                    st.session_state[key_expander] = not st.session_state[key_expander]
                    st.rerun()

            with col_confirmar:
                cantidad = int(reporte.get("me_sirve") or 0)
                if es_propio:
                    st.button(
                        f"Tu reporte · {cantidad} confirmaciones",
                        key=f"propio_{reporte_id}",
                        disabled=True,
                        use_container_width=True,
                    )
                elif ya_confirmado:
                    st.button(
                        f"Confirmado · {cantidad}",
                        key=f"confirmado_{reporte_id}",
                        disabled=True,
                        use_container_width=True,
                    )
                elif st.button(
                    f"Confirmar reporte · {cantidad}",
                    key=f"confirmar_{reporte_id}",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        cliente.table("confirmaciones").insert(
                            {
                                "reporte_id": reporte_id,
                                "usuario_id": usuario_id,
                            }
                        ).execute()
                        st.rerun()
                    except Exception:
                        st.warning(
                            "Este reporte ya fue confirmado o no puede "
                            "ser confirmado por su autor."
                        )

            if st.session_state[key_expander]:
                mostrar_detalle_reporte(reporte)

        st.markdown("<br>", unsafe_allow_html=True)
