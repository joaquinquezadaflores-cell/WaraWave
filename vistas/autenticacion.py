import streamlit as st

from configuracion import ROL_CIUDADANO, obtener_supabase
from utilidades import correo_valido, password_segura


def _cargar_perfil(cliente, auth_id: str):
    respuesta = (
        cliente.table("usuarios")
        .select("id, nombre, correo, rol, activo")
        .eq("auth_id", auth_id)
        .limit(1)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None


def pagina_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Iniciar sesión")
    st.markdown(
        '<div class="auth-sub">Ingresa tus credenciales para continuar</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.pop("registro_exitoso", False):
        st.success(
            "Cuenta creada. Revisa tu correo si Supabase solicita "
            "confirmación y luego inicia sesión."
        )

    correo = st.text_input(
        "Correo electrónico",
        placeholder="usuario@gmail.com",
    )
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar", use_container_width=True, type="primary"):
        if not correo or not password:
            st.error("Completa todos los campos.")
        else:
            try:
                cliente = obtener_supabase()
                respuesta = cliente.auth.sign_in_with_password(
                    {
                        "email": correo.strip().lower(),
                        "password": password,
                    }
                )

                if not respuesta.user or not respuesta.session:
                    st.error("No fue posible iniciar sesión.")
                    return

                perfil = _cargar_perfil(cliente, str(respuesta.user.id))
                if not perfil:
                    cliente.auth.sign_out()
                    st.error(
                        "La cuenta existe, pero falta su perfil en la tabla "
                        "usuarios. Ejecuta database_actualizacion.sql."
                    )
                    return

                if not perfil.get("activo", True):
                    cliente.auth.sign_out()
                    st.error(
                        "Esta cuenta fue desactivada por un administrador."
                    )
                    return

                st.session_state["logged_in"] = True
                st.session_state["usuario_id"] = perfil["id"]
                st.session_state["usuario_auth_id"] = str(respuesta.user.id)
                st.session_state["usuario_nombre"] = perfil["nombre"]
                st.session_state["usuario_correo"] = perfil.get("correo", correo)
                st.session_state["usuario_rol"] = (
                    perfil.get("rol") or ROL_CIUDADANO
                )
                st.session_state["pagina"] = "tablon"
                st.rerun()
            except Exception as error:
                mensaje = str(error).lower()
                if "email not confirmed" in mensaje:
                    st.error("Primero debes confirmar tu correo electrónico.")
                else:
                    st.error("Correo o contraseña incorrectos.")

    st.markdown("---")
    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def pagina_registro():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Registrarse")
    st.markdown(
        '<div class="auth-sub">Crea tu cuenta para reportar incidentes</div>',
        unsafe_allow_html=True,
    )

    nombre = st.text_input("Nombre completo")
    correo = st.text_input(
        "Correo electrónico",
        placeholder="usuario@gmail.com",
    )
    password = st.text_input("Contraseña", type="password")
    password2 = st.text_input("Confirmar contraseña", type="password")
    st.caption(
        "La contraseña debe tener 8 caracteres o más, una mayúscula, "
        "una minúscula y un número."
    )

    if st.button("Crear cuenta", use_container_width=True, type="primary"):
        correo_limpio = correo.strip().lower()
        nombre_limpio = nombre.strip()

        if not nombre_limpio or not correo_limpio or not password or not password2:
            st.error("Completa todos los campos.")
        elif not correo_valido(correo_limpio):
            st.error("Ingresa un correo electrónico válido.")
        elif password != password2:
            st.error("Las contraseñas no coinciden.")
        elif not password_segura(password):
            st.error(
                "Usa al menos 8 caracteres, una mayúscula, "
                "una minúscula y un número."
            )
        else:
            try:
                cliente = obtener_supabase()
                respuesta = cliente.auth.sign_up(
                    {
                        "email": correo_limpio,
                        "password": password,
                        "options": {
                            "data": {
                                "nombre": nombre_limpio,
                                "rol": ROL_CIUDADANO,
                            }
                        },
                    }
                )

                if not respuesta.user:
                    st.error("No se pudo crear la cuenta.")
                    return

                # El trigger SQL crea o enlaza la fila de public.usuarios.
                if respuesta.session:
                    cliente.auth.sign_out()

                st.session_state["registro_exitoso"] = True
                st.session_state["pagina"] = "login"
                st.rerun()
            except Exception as error:
                mensaje = str(error).lower()
                if "already" in mensaje or "registered" in mensaje:
                    st.error("Este correo ya está registrado.")
                else:
                    st.error(f"No se pudo crear la cuenta: {error}")

    st.markdown("---")
    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
