import html
import re
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import streamlit as st

ZONA_CHILE = ZoneInfo("America/Santiago")


def texto_seguro(valor) -> str:
    """Escapa contenido escrito por usuarios antes de insertarlo en HTML."""
    return html.escape(str(valor or ""), quote=True)


def correo_valido(correo: str) -> bool:
    patron = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return bool(re.match(patron, correo.strip()))


def password_segura(password: str) -> bool:
    return (
        len(password) >= 8
        and any(c.islower() for c in password)
        and any(c.isupper() for c in password)
        and any(c.isdigit() for c in password)
    )


def format_fecha(fecha) -> str:
    try:
        if not fecha:
            return ""

        texto_fecha = str(fecha).replace("Z", "+00:00")
        dt = datetime.fromisoformat(texto_fecha)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        dt_chile = dt.astimezone(ZONA_CHILE)
        meses = {
            "Jan": "ene", "Feb": "feb", "Mar": "mar", "Apr": "abr",
            "May": "may", "Jun": "jun", "Jul": "jul", "Aug": "ago",
            "Sep": "sep", "Oct": "oct", "Nov": "nov", "Dec": "dic",
        }
        resultado = dt_chile.strftime("%H:%M - %d %b %Y")

        for mes_en, mes_es in meses.items():
            resultado = resultado.replace(mes_en, mes_es)

        return resultado
    except (TypeError, ValueError):
        return str(fecha)[:19] if fecha else ""


def rango_fechas_iso(inicio: date, fin: date) -> tuple[str, str]:
    inicio_dt = datetime.combine(inicio, time.min, tzinfo=ZONA_CHILE)
    fin_dt = datetime.combine(fin, time.max, tzinfo=ZONA_CHILE)
    return inicio_dt.isoformat(), fin_dt.isoformat()


def limpiar_sesion() -> None:
    cliente = st.session_state.get("_supabase_cliente")
    if cliente is not None:
        try:
            cliente.auth.sign_out()
        except Exception:
            pass

    st.session_state.clear()
