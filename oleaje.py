from datetime import datetime

import requests
import streamlit as st

VARIABLES_MAR = [
    "wave_height",
    "wave_direction",
    "wave_period",
    "sea_level_height_msl",
    "sea_surface_temperature",
    "ocean_current_velocity",
    "ocean_current_direction",
]


@st.cache_data(ttl=3600, show_spinner=False)
def obtener_condiciones_mar(latitud: float, longitud: float) -> dict:
    """Consulta Open-Meteo y conserva el resultado por una hora (HU-10)."""
    respuesta = requests.get(
        "https://marine-api.open-meteo.com/v1/marine",
        params={
            "latitude": latitud,
            "longitude": longitud,
            "current": ",".join(VARIABLES_MAR),
            "timezone": "America/Santiago",
            "cell_selection": "sea",
            "length_unit": "metric",
        },
        timeout=12,
    )
    respuesta.raise_for_status()
    datos = respuesta.json()
    actuales = datos.get("current") or {}
    unidades = datos.get("current_units") or {}

    if not actuales:
        raise ValueError("La API no devolvió condiciones actuales.")

    return {
        "hora": actuales.get("time"),
        "altura_ola": actuales.get("wave_height"),
        "direccion_ola": actuales.get("wave_direction"),
        "periodo_ola": actuales.get("wave_period"),
        "nivel_mar": actuales.get("sea_level_height_msl"),
        "temperatura_mar": actuales.get("sea_surface_temperature"),
        "velocidad_corriente": actuales.get("ocean_current_velocity"),
        "direccion_corriente": actuales.get("ocean_current_direction"),
        "unidades": unidades,
        "consultado_en": datetime.now().astimezone().isoformat(),
    }


def calcular_riesgo(altura_ola, velocidad_corriente) -> dict:
    altura = float(altura_ola or 0)
    corriente = float(velocidad_corriente or 0)

    if altura >= 2.5 or corriente >= 3.0:
        return {
            "nivel": "Peligroso",
            "icono": "🔴",
            "clase": "riesgo-peligroso",
            "recomendacion": "No ingreses al mar. Busca indicaciones oficiales y de salvavidas.",
        }
    if altura >= 1.5 or corriente >= 2.0:
        return {
            "nivel": "Fuerte",
            "icono": "🟠",
            "clase": "riesgo-fuerte",
            "recomendacion": "Evita actividades recreativas y mantente cerca de zonas vigiladas.",
        }
    if altura >= 0.8 or corriente >= 1.0:
        return {
            "nivel": "Moderado",
            "icono": "🟡",
            "clase": "riesgo-moderado",
            "recomendacion": "Ingresa solo con precaución y sigue las instrucciones de salvavidas.",
        }
    return {
        "nivel": "Tranquilo",
        "icono": "🟢",
        "clase": "riesgo-tranquilo",
        "recomendacion": "Condiciones favorables, manteniendo siempre las medidas básicas de seguridad.",
    }


def direccion_cardinal(grados) -> str:
    if grados is None:
        return "Sin datos"

    puntos = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    indice = round(float(grados) / 45) % 8
    return f"{puntos[indice]} ({float(grados):.0f}°)"
