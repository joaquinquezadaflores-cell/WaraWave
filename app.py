import streamlit as st

from estilos import inject_css
from navegacion import render_navbar
from vistas.administracion import pagina_admin
from vistas.autenticacion import pagina_login, pagina_registro
from vistas.bienvenida import pagina_bienvenida
from vistas.crear_reporte import pagina_crear
from vistas.historial import pagina_historial
from vistas.oleaje import pagina_oleaje
from vistas.tablon import pagina_tablon


def main():
    st.set_page_config(
        page_title="Wara Wave",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_css()

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "bienvenida"

    render_navbar()
    pagina = st.session_state["pagina"]

    paginas = {
        "bienvenida": pagina_bienvenida,
        "login": pagina_login,
        "registro": pagina_registro,
        "tablon": pagina_tablon,
        "historial": pagina_historial,
        "oleaje": pagina_oleaje,
        "crear": pagina_crear,
        "admin": pagina_admin,
    }

    vista = paginas.get(pagina, pagina_bienvenida)
    vista()


if __name__ == "__main__":
    main()
