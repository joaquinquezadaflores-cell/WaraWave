import streamlit as st

from configuracion import supabase
from utilidades import format_fecha


def pagina_admin():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para acceder.")
        return

    st.markdown(
        '<div class="page-title">ADMINISTRACIÓN</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Gestiona, ordena y modera los reportes ciudadanos.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    col_espacio, col_orden = st.columns([3, 1])

    with col_orden:
        orden = st.selectbox(
            "Ordenar por votos",
            [
                "Mayor a menor",
                "Menor a mayor",
            ],
        )

    ascendente = orden == "Menor a mayor"

    reportes = (
        supabase.table("reportes")
        .select("*")
        .order(
            "me_sirve",
            desc=not ascendente,
        )
        .execute()
        .data
        or []
    )

    if not reportes:
        st.info("No hay reportes.")
        return

    st.markdown(
        "<br>",
        unsafe_allow_html=True,
    )

    col_reporte, col_votos, col_fecha, col_acciones = st.columns(
        [4, 2, 2, 1]
    )

    with col_reporte:
        st.markdown("**Reporte**")

    with col_votos:
        st.markdown("**Votos**")

    with col_fecha:
        st.markdown("**Fecha**")

    with col_acciones:
        st.markdown("**Acciones**")

    st.divider()

    for reporte in reportes:
        reporte_id = reporte["id"]

        categoria = reporte.get(
            "categoria",
            "",
        ) or ""

        fecha = format_fecha(
            reporte.get(
                "fecha",
                "",
            )
        )

        me_sirve = reporte.get(
            "me_sirve",
            0,
        )

        no_me_sirve = reporte.get(
            "no_me_sirve",
            0,
        )

        with st.container(border=True):
            col_a, col_b, col_c, col_d = st.columns(
                [4, 2, 2, 1]
            )

            with col_a:
                st.markdown(
                    f"""
                    <div class="admin-title">
                        {reporte.get("titulo", "")}
                    </div>

                    <div class="admin-small">
                        {reporte.get("ubicacion", "")}
                    </div>

                    <br>

                    <span class="rbadge">
                        {categoria}
                    </span>
                    """,
                    unsafe_allow_html=True,
                )

            with col_b:
                st.markdown(
                    f"""
                    <div style="font-size:.9rem; line-height:1.7;">
                        Me sirve: <b>{me_sirve}</b><br>
                        No me sirve: <b>{no_me_sirve}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_c:
                st.markdown(
                    f"""
                    <div style="font-size:.9rem;">
                        {fecha}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_d:
                if st.button(
                    "Eliminar",
                    key=f"delete_{reporte_id}",
                ):
                    (
                        supabase.table("reportes")
                        .delete()
                        .eq("id", reporte_id)
                        .execute()
                    )

                    st.rerun()