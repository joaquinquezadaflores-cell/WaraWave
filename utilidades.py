import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def format_fecha(fecha):
    try:
        if not fecha:
            return ""

        texto_fecha = str(fecha)

        texto_fecha = texto_fecha.replace("Z", "+00:00")

        dt = datetime.fromisoformat(texto_fecha)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        dt_chile = dt.astimezone(ZoneInfo("America/Santiago"))

        meses = {
            "Jan": "ene",
            "Feb": "feb",
            "Mar": "mar",
            "Apr": "abr",
            "May": "may",
            "Jun": "jun",
            "Jul": "jul",
            "Aug": "ago",
            "Sep": "sep",
            "Oct": "oct",
            "Nov": "nov",
            "Dec": "dic",
        }

        fecha_formateada = dt_chile.strftime("%H:%M - %d %b")

        for mes_en, mes_es in meses.items():
            fecha_formateada = fecha_formateada.replace(mes_en, mes_es)

        return fecha_formateada

    except Exception:
        return str(fecha)[:16] if fecha else ""