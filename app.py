import streamlit as st

from estilos import inject_css
from navegacion import render_navbar

from vistas.bienvenida import pagina_bienvenida
from vistas.autenticacion import pagina_login, pagina_registro
from vistas.tablon import pagina_tablon
from vistas.oleaje import pagina_oleaje
from vistas.crear_reporte import pagina_crear
from vistas.administracion import pagina_admin


def main():
    st.set_page_config(
        page_title="Wara Wave",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_css()

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "bienvenida"

    render_navbar()

    pagina = st.session_state["pagina"]

    if pagina == "bienvenida":
        pagina_bienvenida()

    elif pagina == "login":
        pagina_login()

    elif pagina == "registro":
        pagina_registro()

    elif pagina == "tablon":
        pagina_tablon()
    
    elif pagina == "oleaje":
        pagina_oleaje()

    elif pagina == "crear":
        pagina_crear()

    elif pagina == "admin":
        pagina_admin()


if __name__ == "__main__":
    main()