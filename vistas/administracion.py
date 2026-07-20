from datetime import date, timedelta

import streamlit as st

from configuracion import (
    CATEGORIAS,
    PLAYAS,
    ROL_ADMINISTRADOR,
    ROL_AUTORIDAD,
    ROL_CIUDADANO,
    ROLES_CON_ACCESO_ADMIN,
    ROLES_VALIDOS,
    obtener_supabase,
)
from utilidades import format_fecha, rango_fechas_iso, texto_seguro
from vistas.componentes_reportes import mostrar_detalle_reporte, nombre_ubicacion

CATEGORIAS_PRIORITARIAS = {"Contaminación", "Infraestructura", "Seguridad"}


def pagina_admin():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para acceder.")
        return

    rol = st.session_state.get("usuario_rol", ROL_CIUDADANO)
    if rol not in ROLES_CON_ACCESO_ADMIN:
        st.markdown(
            '<div class="page-title">ACCESO RESTRINGIDO</div>',
            unsafe_allow_html=True,
        )
        st.error("Esta sección es exclusiva para administradores y autoridades.")
        return

    if rol == ROL_ADMINISTRADOR:
        _panel_administrador()
    elif rol == ROL_AUTORIDAD:
        _panel_autoridad()


def _filtros_reportes(prefijo: str):
    col1, col2, col3 = st.columns(3)
    with col1:
        playa = st.selectbox(
            "Zona / Playa",
            ["Todas"] + PLAYAS,
            key=f"{prefijo}_playa",
        )
    with col2:
        categoria = st.selectbox(
            "Categoría",
            ["Todas"] + CATEGORIAS,
            key=f"{prefijo}_categoria",
        )
    with col3:
        estado = st.selectbox(
            "Estado",
            ["Todos", "Visibles", "Retirados"],
            key=f"{prefijo}_estado",
        )

    hoy = date.today()
    col4, col5 = st.columns(2)
    with col4:
        inicio = st.date_input(
            "Desde",
            value=hoy - timedelta(days=30),
            key=f"{prefijo}_inicio",
        )
    with col5:
        fin = st.date_input(
            "Hasta",
            value=hoy,
            key=f"{prefijo}_fin",
        )

    return playa, categoria, estado, inicio, fin


def _consultar_reportes(cliente, filtros):
    playa, categoria, estado, inicio, fin = filtros
    inicio_iso, fin_iso = rango_fechas_iso(inicio, fin)

    query = (
        cliente.table("reportes")
        .select("*")
        .gte("fecha", inicio_iso)
        .lte("fecha", fin_iso)
        .order("fecha", desc=True)
    )

    if playa != "Todas":
        query = query.eq("ubicacion", playa)
    if categoria != "Todas":
        query = query.eq("categoria", categoria)
    if estado == "Visibles":
        query = query.eq("activo", True)
    elif estado == "Retirados":
        query = query.eq("activo", False)

    return query.execute().data or []


def _panel_administrador():
    st.markdown(
        '<div class="page-title">ADMINISTRACIÓN</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Modera reportes y gestiona las cuentas de la plataforma.</div>',
        unsafe_allow_html=True,
    )

    tab_reportes, tab_usuarios = st.tabs(
        ["Moderar reportes", "Gestionar usuarios"]
    )
    cliente = obtener_supabase()

    with tab_reportes:
        _moderacion_reportes(cliente)
    with tab_usuarios:
        _gestion_usuarios(cliente)


def _moderacion_reportes(cliente):
    filtros = _filtros_reportes("admin")
    if filtros[3] > filtros[4]:
        st.error("La fecha inicial no puede ser posterior a la fecha final.")
        return

    try:
        reportes = _consultar_reportes(cliente, filtros)
    except Exception as error:
        st.error(f"No se pudieron cargar los reportes: {error}")
        return

    st.caption(f"Resultados: {len(reportes)}")
    if not reportes:
        st.info("No hay reportes para los filtros seleccionados.")
        return

    for reporte in reportes:
        reporte_id = reporte["id"]
        activo = bool(reporte.get("activo", True))
        estado = "VISIBLE" if activo else "RETIRADO"

        with st.container(border=True):
            col_info, col_accion = st.columns([5, 2])
            with col_info:
                st.markdown(
                    f"""
                    <div class="admin-title">{texto_seguro(reporte.get('titulo'))}</div>
                    <div class="admin-small">
                        {texto_seguro(nombre_ubicacion(reporte))} ·
                        {texto_seguro(format_fecha(reporte.get('fecha')))}
                    </div>
                    <br>
                    <span class="rbadge">{texto_seguro(reporte.get('categoria'))}</span>
                    <span class="rbadge status-badge">{estado}</span>
                    """,
                    unsafe_allow_html=True,
                )
            with col_accion:
                etiqueta = "Retirar del tablón" if activo else "Restaurar"
                if st.button(
                    etiqueta,
                    key=f"moderar_{reporte_id}",
                    type="primary" if not activo else "secondary",
                    use_container_width=True,
                ):
                    try:
                        cliente.table("reportes").update(
                            {
                                "activo": not activo,
                                "moderado_por": st.session_state[
                                    "usuario_auth_id"
                                ],
                            }
                        ).eq("id", reporte_id).execute()
                        st.rerun()
                    except Exception as error:
                        st.error(f"No se pudo moderar el reporte: {error}")

            with st.expander("Revisar contenido"):
                mostrar_detalle_reporte(reporte)


def _gestion_usuarios(cliente):
    st.markdown("#### Usuarios registrados")
    st.caption(
        "Un administrador puede activar, desactivar o cambiar el rol de "
        "otras cuentas. No puede desactivar su propia cuenta desde aquí."
    )

    try:
        usuarios = (
            cliente.table("usuarios")
            .select("id, auth_id, nombre, correo, rol, activo, fecha_creacion")
            .order("nombre")
            .execute()
            .data
            or []
        )
    except Exception as error:
        st.error(f"No se pudieron cargar los usuarios: {error}")
        return

    if not usuarios:
        st.info("No hay usuarios registrados.")
        return

    for usuario in usuarios:
        usuario_id = usuario["id"]
        es_propio = str(usuario.get("auth_id")) == st.session_state.get(
            "usuario_auth_id"
        )
        rol_actual = usuario.get("rol") or ROL_CIUDADANO
        activo = bool(usuario.get("activo", True))

        with st.container(border=True):
            col_info, col_rol, col_estado = st.columns([4, 2, 2])
            with col_info:
                st.markdown(
                    f"**{texto_seguro(usuario.get('nombre'))}**  \n"
                    f"{texto_seguro(usuario.get('correo'))}"
                )
                st.caption("Tu cuenta" if es_propio else f"ID interno: {usuario_id}")

            with col_rol:
                nuevo_rol = st.selectbox(
                    "Rol",
                    ROLES_VALIDOS,
                    index=ROLES_VALIDOS.index(rol_actual)
                    if rol_actual in ROLES_VALIDOS
                    else 0,
                    key=f"rol_usuario_{usuario_id}",
                    disabled=es_propio,
                )
                if not es_propio and nuevo_rol != rol_actual:
                    if st.button(
                        "Guardar rol",
                        key=f"guardar_rol_{usuario_id}",
                        use_container_width=True,
                    ):
                        try:
                            cliente.table("usuarios").update(
                                {"rol": nuevo_rol}
                            ).eq("id", usuario_id).execute()
                            st.rerun()
                        except Exception as error:
                            st.error(f"No se pudo cambiar el rol: {error}")

            with col_estado:
                st.write("Estado")
                st.success("Activo") if activo else st.error("Desactivado")
                if not es_propio:
                    etiqueta = "Desactivar" if activo else "Activar"
                    if st.button(
                        etiqueta,
                        key=f"estado_usuario_{usuario_id}",
                        use_container_width=True,
                    ):
                        try:
                            cliente.table("usuarios").update(
                                {"activo": not activo}
                            ).eq("id", usuario_id).execute()
                            st.rerun()
                        except Exception as error:
                            st.error(f"No se pudo cambiar el estado: {error}")


def _panel_autoridad():
    st.markdown(
        '<div class="page-title">PANEL DE AUDITORÍA</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="page-subtitle">
            Resúmenes por zona y fecha para priorizar inspecciones sanitarias y ambientales.
        </div>
        """,
        unsafe_allow_html=True,
    )

    filtros = _filtros_reportes("autoridad")
    if filtros[3] > filtros[4]:
        st.error("La fecha inicial no puede ser posterior a la fecha final.")
        return

    try:
        reportes = _consultar_reportes(obtener_supabase(), filtros)
    except Exception as error:
        st.error(f"No se pudo generar el resumen: {error}")
        return

    if not reportes:
        st.info("No hay reportes para los filtros seleccionados.")
        return

    por_zona = {}
    por_categoria = {}
    prioritarios = 0
    confirmaciones = 0

    for reporte in reportes:
        zona = nombre_ubicacion(reporte)
        categoria = reporte.get("categoria") or "Sin categoría"
        por_zona[zona] = por_zona.get(zona, 0) + 1
        por_categoria[categoria] = por_categoria.get(categoria, 0) + 1
        confirmaciones += int(reporte.get("me_sirve") or 0)
        if categoria in CATEGORIAS_PRIORITARIAS:
            prioritarios += 1

    col_total, col_prior, col_zonas, col_conf = st.columns(4)
    col_total.metric("Reportes", len(reportes))
    col_prior.metric("Prioritarios", prioritarios)
    col_zonas.metric("Zonas afectadas", len(por_zona))
    col_conf.metric("Confirmaciones", confirmaciones)

    col_resumen1, col_resumen2 = st.columns(2)
    with col_resumen1:
        st.markdown("#### Reportes por zona")
        st.dataframe(
            [
                {"Zona": zona, "Cantidad": cantidad}
                for zona, cantidad in sorted(
                    por_zona.items(), key=lambda elemento: -elemento[1]
                )
            ],
            use_container_width=True,
            hide_index=True,
        )
    with col_resumen2:
        st.markdown("#### Reportes por categoría")
        st.dataframe(
            [
                {"Categoría": categoria, "Cantidad": cantidad}
                for categoria, cantidad in sorted(
                    por_categoria.items(), key=lambda elemento: -elemento[1]
                )
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.markdown("#### Detalle para inspección")
    for reporte in reportes:
        categoria = reporte.get("categoria") or ""
        prioridad = "PRIORITARIO" if categoria in CATEGORIAS_PRIORITARIAS else "NORMAL"
        with st.expander(
            f"{reporte.get('titulo', 'Sin título')} · {nombre_ubicacion(reporte)}"
        ):
            st.write(reporte.get("descripcion", ""))
            st.caption(
                f"{format_fecha(reporte.get('fecha'))} · {categoria} · "
                f"{prioridad} · {int(reporte.get('me_sirve') or 0)} confirmaciones"
            )
            latitud = reporte.get("latitud")
            longitud = reporte.get("longitud")
            if latitud is not None and longitud is not None:
                st.map(
                    [{"lat": float(latitud), "lon": float(longitud)}],
                    zoom=14,
                    use_container_width=True,
                )
