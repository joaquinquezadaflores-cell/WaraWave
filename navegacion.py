import streamlit as st


def render_navbar():
    pagina = st.session_state.get("pagina", "bienvenida")
    usuario = st.session_state.get("usuario_nombre", "")

    st.markdown(
        f"""
        <div class="navbar">
            <div>
                <div class="brand">WARA WAVE</div>
                <div class="tagline">Por playas más seguras</div>
            </div>
            <div>
                <span class="nav-user">{usuario if usuario else ""}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if pagina in ("bienvenida", "login", "registro"):
        return

    st.markdown(
        '<div class="nav-button-area">',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    with cols[0]:
        if st.button("Tablón", use_container_width=True):
            st.session_state["pagina"] = "tablon"
            st.rerun()

    with cols[1]:
        if st.button("Crear", use_container_width=True):
            st.session_state["pagina"] = "crear"
            st.rerun()

    with cols[2]:
        if st.button("Admin", use_container_width=True):
            st.session_state["pagina"] = "admin"
            st.rerun()

    with cols[3]:
        if st.button("Salir", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)