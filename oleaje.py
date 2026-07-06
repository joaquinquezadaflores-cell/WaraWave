import requests

def obtener_oleaje(latitud, longitud):
    url = (
        f"https://marine-api.open-meteo.com/v1/marine?"
        f"latitude={latitud}"
        f"&longitude={longitud}"
        f"&hourly=wave_height,wave_direction,wave_period"
    )
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        return {
            "altura": datos["hourly"]["wave_height"][0],
            "direccion": datos["hourly"]["wave_direction"][0],
            "periodo": datos["hourly"]["wave_period"][0]
        }
    return None
