import streamlit as st

from configuracion import supabase, CATEGORIAS, PLAYAS
from utilidades import format_fecha


def pagina_tablon():
    if not st.session_state.get("logged_in"):
        st.session_state["pagina"] = "login"
        st.rerun()

    st.markdown(
        '<div class="page-title">TABLÓN DE REPORTES</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Reportes ciudadanos en tiempo real'
        '</div>',
        unsafe_allow_html=True,
    )

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
            ["Todas"] + CATEGORIAS,
        )

    query = (
        supabase.table("reportes")
        .select("*")
        .order("fecha", desc=True)
    )

    if filtro_playa != "Todas":
        query = query.eq(
            "ubicacion",
            filtro_playa,
        )

    if filtro_categoria != "Todas":
        query = query.eq(
            "categoria",
            filtro_categoria,
        )

    reportes = query.execute().data or []

    if not reportes:
        st.info(
            "No hay reportes todavía. "
            "Sé la primera persona en reportar."
        )
        return

    for reporte in reportes:
        reporte_id = reporte["id"]

        me_sirve = reporte.get(
            "me_sirve",
            0,
        )

        no_me_sirve = reporte.get(
            "no_me_sirve",
            0,
        )

        key_expander = f"exp_{reporte_id}"

        if key_expander not in st.session_state:
            st.session_state[key_expander] = False

        categoria = reporte.get(
            "categoria",
            "",
        ) or ""

        imagen_url = reporte.get("imagen_url")
        video_url = reporte.get("video_url")

        with st.container(border=True):
            st.markdown(
                f"""
                <div class="rtitle">
                    {reporte.get("titulo", "Sin título")}
                </div>

                <div class="rmeta">
                    {format_fecha(reporte.get("fecha", ""))}
                    &nbsp;|&nbsp;
                    {reporte.get("ubicacion", "")}
                </div>

                <span class="rbadge">
                    {categoria}
                </span>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                "<br>",
                unsafe_allow_html=True,
            )

            col_ver, col_me, col_no = st.columns(
                [4, 1.2, 1.3]
            )

            with col_ver:
                texto_boton = (
                    "Ocultar"
                    if st.session_state[key_expander]
                    else "Ver más"
                )

                if st.button(
                    texto_boton,
                    key=f"toggle_{reporte_id}",
                ):
                    st.session_state[key_expander] = (
                        not st.session_state[key_expander]
                    )

                    st.rerun()

            with col_me:
                if st.button(
                    f"Me sirve {me_sirve}",
                    key=f"me_{reporte_id}",
                ):
                    (
                        supabase.table("reportes")
                        .update(
                            {
                                "me_sirve": me_sirve + 1
                            }
                        )
                        .eq("id", reporte_id)
                        .execute()
                    )

                    st.rerun()

            with col_no:
                if st.button(
                    f"No me sirve {no_me_sirve}",
                    key=f"no_{reporte_id}",
                ):
                    (
                        supabase.table("reportes")
                        .update(
                            {
                                "no_me_sirve":
                                no_me_sirve + 1
                            }
                        )
                        .eq("id", reporte_id)
                        .execute()
                    )

                    st.rerun()

            if st.session_state[key_expander]:
                st.markdown("#### Descripción")

                st.write(
                    reporte.get(
                        "descripcion",
                        "",
                    )
                )

                if imagen_url and str(imagen_url).strip():
                    st.markdown(
                        "#### Evidencia visual"
                    )

                    st.image(
                        imagen_url,
                        use_container_width=True,
                    )

                elif video_url and str(video_url).strip():
                    st.markdown(
                        "#### Evidencia visual"
                    )

                    st.video(video_url)

                else:
                    st.caption(
                        "Este reporte no tiene "
                        "evidencia visual adjunta."
                    )

        st.markdown(
            "<br>",
            unsafe_allow_html=True,
        )