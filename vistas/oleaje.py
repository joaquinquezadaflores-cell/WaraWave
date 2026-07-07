import streamlit as st

from configuracion import supabase
from oleaje import oleaje, riesgo, recomendacion


def pagina_oleaje():

    st.markdown(
        '<div class="page-title">ESTADO DEL OLEAJE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Condiciones actuales del mar en Arica</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    if oleaje is None:
        st.error(
            "No fue posible obtener la información del oleaje."
        )
        return

    cantidad_reportes = (
        supabase.table("reportes")
        .select(
            "id",
            count="exact",
        )
        .execute()
        .count
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🌊 Altura de ola",
            f'{oleaje["altura"]:.2f} m',
        )

    with col2:
        st.metric(
            "🧭 Dirección",
            f'{oleaje["direccion"]:.0f}°',
        )

    with col3:
        st.metric(
            "⏱️ Período",
            f'{oleaje["periodo"]:.1f} s',
        )

    st.divider()

    st.subheader("Nivel de riesgo")
    st.success(riesgo)

    st.subheader("Recomendación")
    st.warning(recomendacion)

    st.subheader("Reportes ciudadanos")
    st.info(
        f"Actualmente existen **{cantidad_reportes}** reportes registrados."
    )