import streamlit as st

from configuracion import CATEGORIAS, PLAYAS, obtener_supabase
from vistas.componentes_reportes import encabezado_reporte, mostrar_detalle_reporte

MOTIVOS_DUDA = [
    "La información parece incorrecta",
    "La ubicación no coincide",
    "Es un reporte duplicado",
    "La evidencia no corresponde",
    "Otro motivo",
]

def _confirmaciones_usuario(cliente, usuario_id) -> set:
    respuesta = (
        cliente.table("confirmaciones")
        .select("reporte_id")
        .eq("usuario_id", usuario_id)
        .execute()
    )
    return {fila["reporte_id"] for fila in (respuesta.data or [])}

def _dudas_usuario(cliente, usuario_id) -> set:
    respuesta = (
        cliente.table("dudas_reportes")
        .select("reporte_id")
        .eq("usuario_id", usuario_id)
        .execute()
    )

    return {
        fila["reporte_id"]
        for fila in (respuesta.data or [])
    }

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

        dudosos = _dudas_usuario(
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
        ya_dudoso = reporte_id in dudosos

        key_expander = f"exp_{reporte_id}"
        key_duda = f"duda_{reporte_id}"

        if key_expander not in st.session_state:
            st.session_state[key_expander] = False
        if key_duda not in st.session_state:
            st.session_state[key_duda] = False

        with st.container(border=True):
            encabezado_reporte(reporte)
            st.markdown("<br>", unsafe_allow_html=True)

            col_ver, col_confirmar, col_duda = st.columns([3, 2, 2])

            with col_ver:
                texto_boton = (
                    "Ocultar detalles"
                    if st.session_state[key_expander]
                    else "Ver detalles"
                )

                if st.button(
                    texto_boton,
                    key=f"toggle_{reporte_id}",
                    use_container_width=True,
                ):
                    st.session_state[key_expander] = (
                        not st.session_state[key_expander]
                    )
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
                    f"✅ Confirmar · {cantidad}",
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


            with col_duda:
                if es_propio:
                    st.button(
                        "No puedes valorar tu reporte",
                        key=f"duda_propia_{reporte_id}",
                        disabled=True,
                        use_container_width=True,
                    )

                elif ya_dudoso:
                    st.button(
                        "⚠️ Duda registrada",
                        key=f"dudoso_{reporte_id}",
                        disabled=True,
                        use_container_width=True,
                    )

                elif st.button(
                    "⚠️ Tengo dudas",
                    key=f"mostrar_duda_{reporte_id}",
                    use_container_width=True,
                ):
                    st.session_state[key_duda] = (
                        not st.session_state[key_duda]
                    )
                    st.rerun()


            if (
                st.session_state[key_duda]
                and not es_propio
                and not ya_dudoso
            ):
                with st.form(f"form_duda_{reporte_id}"):
                    motivo_duda = st.selectbox(
                        "¿Por qué tienes dudas sobre este reporte?",
                        MOTIVOS_DUDA,
                        key=f"motivo_duda_{reporte_id}",
                    )

                    detalle_duda = ""

                    if motivo_duda == "Otro motivo":
                        detalle_duda = st.text_input(
                            "Escribe el motivo",
                            key=f"detalle_duda_{reporte_id}",
                    )

                    enviar_duda = st.form_submit_button(
                        "Enviar observación",
                        use_container_width=True,
                    )

                    if enviar_duda:
                        if (
                            motivo_duda == "Otro motivo"
                            and not detalle_duda.strip()
                        ):
                            st.error("Debes escribir el motivo de tu duda.")
                        else:
                            try:
                                cliente.table("dudas_reportes").insert(
                                    {
                                        "reporte_id": reporte_id,
                                        "usuario_id": usuario_id,
                                        "motivo": motivo_duda,
                                        "detalle": detalle_duda.strip() or None,
                                    }
                                ).execute()

                                st.session_state[key_duda] = False
                                st.success("Tu observación fue registrada.")
                                st.rerun()

                            except Exception:
                                st.warning(
                                    "La duda ya fue registrada o no puedes "
                                    "valorar tu propio reporte."
                                )
                

            if st.session_state[key_expander]:
                mostrar_detalle_reporte(reporte)

        st.markdown("<br>", unsafe_allow_html=True)
