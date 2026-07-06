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
