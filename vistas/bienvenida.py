import streamlit as st


def pagina_bienvenida():
    st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="welcome-title">WARA WAVE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="welcome-sub">Por playas más seguras</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "Iniciar sesión",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["pagina"] = "login"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Registrarse", use_container_width=True):
            st.session_state["pagina"] = "registro"
            st.rerun()