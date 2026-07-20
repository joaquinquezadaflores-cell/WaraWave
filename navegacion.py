import streamlit as st

from configuracion import (
    ROL_ADMINISTRADOR,
    ROL_AUTORIDAD,
    ROL_CIUDADANO,
    ROLES_CON_ACCESO_ADMIN,
)
from utilidades import limpiar_sesion, texto_seguro

ETIQUETAS_ROL = {
    ROL_CIUDADANO: ("Ciudadano", "role-ciudadano"),
    ROL_ADMINISTRADOR: ("Administrador", "role-administrador"),
    ROL_AUTORIDAD: ("Autoridad", "role-autoridad"),
}


def _ir_a(pagina: str) -> None:
    st.session_state["pagina"] = pagina
    st.rerun()


def render_navbar():
    pagina = st.session_state.get("pagina", "bienvenida")
    usuario = texto_seguro(st.session_state.get("usuario_nombre", ""))
    rol = st.session_state.get("usuario_rol", ROL_CIUDADANO)
    etiqueta_rol, clase_rol = ETIQUETAS_ROL.get(
        rol,
        ETIQUETAS_ROL[ROL_CIUDADANO],
    )

    badge_html = (
        f'<span class="role-badge {clase_rol}">{etiqueta_rol}</span>'
        if usuario
        else ""
    )

    st.markdown(
        f"""
        <div class="navbar">
            <div>
                <div class="brand">WARA WAVE</div>
                <div class="tagline">Por playas más seguras</div>
            </div>
            <div>
                <span class="nav-user">{usuario}</span>
                {badge_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if pagina in ("bienvenida", "login", "registro"):
        return

    tiene_acceso_admin = rol in ROLES_CON_ACCESO_ADMIN
    cantidad = 6 if tiene_acceso_admin else 5
    columnas = st.columns(cantidad)

    botones = [
        ("Tablón", "tablon"),
        ("Historial", "historial"),
        ("Oleaje", "oleaje"),
        ("Crear", "crear"),
    ]

    for indice, (etiqueta, destino) in enumerate(botones):
        with columnas[indice]:
            if st.button(
                etiqueta,
                key=f"nav_{destino}",
                use_container_width=True,
                type="primary" if pagina == destino else "secondary",
            ):
                _ir_a(destino)

    siguiente = 4
    if tiene_acceso_admin:
        etiqueta = "Auditoría" if rol == ROL_AUTORIDAD else "Admin"
        with columnas[siguiente]:
            if st.button(
                etiqueta,
                key="nav_admin",
                use_container_width=True,
                type="primary" if pagina == "admin" else "secondary",
            ):
                _ir_a("admin")
        siguiente += 1

    with columnas[siguiente]:
        if st.button("Salir", use_container_width=True):
            limpiar_sesion()
            st.rerun()
