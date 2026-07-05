import time

import streamlit as st

from configuracion import supabase
from utilidades import hash_password


def pagina_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Iniciar sesión")
    st.markdown(
        '<div class="auth-sub">Ingresa tus credenciales para continuar</div>',
        unsafe_allow_html=True,
    )

    correo = st.text_input(
        "Correo electrónico",
        placeholder="usuario@gmail.com",
    )

    password = st.text_input(
        "Contraseña",
        type="password",
    )

    if st.button(
        "Entrar",
        use_container_width=True,
        type="primary",
    ):
        if not correo or not password:
            st.error("Completa todos los campos.")

        else:
            res = (
                supabase.table("usuarios")
                .select("id, nombre")
                .eq("correo", correo.strip().lower())
                .eq("password", hash_password(password))
                .execute()
            )

            if res.data:
                usuario = res.data[0]

                st.session_state["logged_in"] = True
                st.session_state["usuario_id"] = usuario["id"]
                st.session_state["usuario_nombre"] = usuario["nombre"]
                st.session_state["pagina"] = "tablon"

                st.rerun()

            else:
                st.error(
                    "No se pudo iniciar sesión: "
                    "credenciales incorrectas."
                )

    st.markdown("---")

    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def pagina_registro():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Registrarse")
    st.markdown(
        '<div class="auth-sub">'
        "Crea tu cuenta para reportar incidentes"
        "</div>",
        unsafe_allow_html=True,
    )

    nombre = st.text_input("Nombre completo")

    correo = st.text_input(
        "Correo electrónico",
        placeholder="usuario@gmail.com",
    )

    password = st.text_input(
        "Contraseña",
        type="password",
    )

    password2 = st.text_input(
        "Confirmar contraseña",
        type="password",
    )

    if st.button(
        "Crear cuenta",
        use_container_width=True,
        type="primary",
    ):
        if not nombre or not correo or not password or not password2:
            st.error("Completa todos los campos.")

        elif password != password2:
            st.error("Las contraseñas no coinciden.")

        elif len(password) < 6:
            st.error(
                "La contraseña debe tener al menos "
                "6 caracteres :)"
            )

        else:
            existe = (
                supabase.table("usuarios")
                .select("id")
                .eq("correo", correo.strip().lower())
                .execute()
            )

            if existe.data:
                st.error("Este correo ya está registrado. :)")

            else:
                supabase.table("usuarios").insert(
                    {
                        "nombre": nombre,
                        "correo": correo.strip().lower(),
                        "password": hash_password(password),
                    }
                ).execute()

                st.success(
                    "Cuenta creada. Ahora inicia sesión :)"
                )

                time.sleep(1.3)

                st.session_state["pagina"] = "login"

                st.rerun()

    st.markdown("---")

    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)