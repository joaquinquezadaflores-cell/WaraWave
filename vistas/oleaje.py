import streamlit as st

from configuracion import PLAYAS_COORDENADAS, obtener_supabase
from oleaje import calcular_riesgo, direccion_cardinal, obtener_condiciones_mar
from utilidades import format_fecha


def _valor(valor, decimales=1, sufijo="") -> str:
    if valor is None:
        return "Sin datos"
    return f"{float(valor):.{decimales}f}{sufijo}"


def pagina_oleaje():
    if not st.session_state.get("logged_in"):
        st.session_state["pagina"] = "login"
        st.rerun()

    st.markdown(
        '<div class="page-title">ESTADO DEL MAR</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="page-subtitle">
            Oleaje, nivel del mar, temperatura y corriente para planificar actividades de forma segura.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_playa, col_refrescar = st.columns([4, 1])
    with col_playa:
        playa = st.selectbox(
            "Selecciona una playa",
            list(PLAYAS_COORDENADAS.keys()),
        )
    with col_refrescar:
        st.write("")
        st.write("")
        if st.button("Actualizar ahora", use_container_width=True):
            obtener_condiciones_mar.clear()
            st.rerun()

    latitud, longitud = PLAYAS_COORDENADAS[playa]

    try:
        with st.spinner("Consultando condiciones del mar..."):
            condiciones = obtener_condiciones_mar(latitud, longitud)
    except Exception as error:
        st.error(f"No fue posible obtener la información del mar: {error}")
        return

    riesgo = calcular_riesgo(
        condiciones.get("altura_ola"),
        condiciones.get("velocidad_corriente"),
    )

    st.markdown(
        f"""
        <div class="risk-card {riesgo['clase']}">
            <div class="risk-icon">{riesgo['icono']}</div>
            <div>
                <div class="risk-label">Nivel de riesgo: {riesgo['nivel']}</div>
                <div class="risk-text">{riesgo['recomendacion']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("🌊 Altura de ola", _valor(condiciones.get("altura_ola"), 2, " m"))
    col2.metric("⏱️ Período", _valor(condiciones.get("periodo_ola"), 1, " s"))
    col3.metric("🧭 Dirección de ola", direccion_cardinal(condiciones.get("direccion_ola")))

    col4, col5, col6 = st.columns(3)
    col4.metric("🌡️ Temperatura", _valor(condiciones.get("temperatura_mar"), 1, " °C"))
    col5.metric("↕️ Nivel del mar", _valor(condiciones.get("nivel_mar"), 2, " m"))
    col6.metric("➡️ Velocidad corriente", _valor(condiciones.get("velocidad_corriente"), 2, " km/h"))

    st.metric(
        "🧭 Dirección de la corriente",
        direccion_cardinal(condiciones.get("direccion_corriente")),
    )

    hora = condiciones.get("hora")
    st.info(
        f"Datos para **{playa}**. Hora del modelo: **{hora or 'sin datos'}**. "
        "La aplicación renueva la consulta automáticamente cada hora."
    )
    st.caption(
        "Fuente: Open-Meteo Marine API. Los modelos costeros son orientativos "
        "y no reemplazan avisos de la Armada, autoridades o salvavidas."
    )

    try:
        cliente = obtener_supabase()
        cantidad = (
            cliente.table("reportes")
            .select("id", count="exact")
            .eq("activo", True)
            .eq("ubicacion", playa)
            .execute()
            .count
        )
        st.caption(f"Reportes ciudadanos visibles en esta playa: {cantidad or 0}")
    except Exception:
        pass
