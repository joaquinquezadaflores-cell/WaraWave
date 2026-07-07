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

def obtener_recomendacion(nivel_riesgo):

    if nivel_riesgo == "🟢 Condiciones seguras":
        return (
            "El mar presenta condiciones favorables"
            "Puedes realizar actividades recreativas con normalidad,"
            "manteniendo siempre las medidas básicas de seguridad"
        )
    elif nivel_riesgo == "🟡 Riesgo moderado":
        return (
            "¡Se recomienda ingresar al mar con precaución!"
            "Evita alejarte de la orilla y sigue las indicaciones de los salvavidas"
        )
    elif nivel_riesgo == "🟠 Riesgo alto":
        return (
            "¡Se recomienda evitar actividades recreativas en el mar!"
            "Las condiciones del oleaje pueden representar un riesgo para bañistas"
        )
    elif nivel_riesgo == "🔴 Riesgo extremo":
        return (
            "¡No ingreses al mar!"
            "Existe un alto riesgo debido al fuerte oleaje"
        )
    else:
        return (
            "No existe información suficiente para generar una recomendación"
        )

def calcular_riesgo(altura_ola):

    if altura_ola >= 2.5:
        return "🔴 Riesgo extremo"
    elif altura_ola >= 1.5:
        return "🟠 Riesgo alto"
    elif altura_ola >= 1:
        return "🟡 Riesgo moderado"
    else:
        return "🟢 Condiciones seguras"

oleaje = obtener_oleaje(-18.470, -70.312)

if oleaje:
    riesgo = calcular_riesgo(oleaje["altura"])
    recomendacion = obtener_recomendacion(riesgo)
    