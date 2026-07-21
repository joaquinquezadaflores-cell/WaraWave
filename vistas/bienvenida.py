import streamlit as st


def pagina_bienvenida():
    st.markdown(
        """
        <div class="welcome-box">
            <div class="welcome-icon">🌊</div>
            <div class="welcome-eyebrow">Comunidad costera informada</div>
            <div class="welcome-title">WARA WAVE</div>
            <div class="welcome-sub">Por playas más seguras</div>
            <div class="welcome-copy">
                Reporta incidentes, revisa información ciudadana y consulta
                las condiciones del mar desde una sola plataforma.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "Ingresar a mi cuenta",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "login"
            st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Crear una cuenta", use_container_width=True):
            st.session_state["pagina"] = "registro"
            st.rerun()