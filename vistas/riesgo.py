def calcular_riesgo(altura_ola, cantidad_reportes):

    if altura_ola >= 2.5:
        return "🔴 Riesgo extremo"
    elif altura_ola >= 1.5 and cantidad_reportes >= 5:
        return "🟠 Riesgo alto"
    elif altura_ola >= 1:
        return "🟡 Riesgo moderado"
    else:
        return "🟢 Condiciones seguras"
