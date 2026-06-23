import streamlit as st
from supabase import create_client
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
import time


#config de supabase

SUPABASE_URL = st.secrets["connections"]["supabase"]["url"]
SUPABASE_KEY = st.secrets["connections"]["supabase"]["key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

CATEGORIAS = ["Contaminación", "Fauna", "Infraestructura", "Seguridad", "Otro"]
PLAYAS = ["Playa Laucho", "Playa Lisera", "Playa Chinchorro", "Playa Las Machas", "Otra"]


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

def inject_css():
    st.markdown(
        """
        <style>
        *, *::before, *::after {
            color-scheme: light !important;
        }

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main,
        .main .block-container,
        .stApp {
            background-color: #ffffff !important;
            color: #1E293B !important;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 0.8rem;
            padding-bottom: 4rem;
        }

        #MainMenu, footer, header {
            visibility: hidden;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        label, p, span, h1, h2, h3, h4 {
            color: #1E293B !important;
        }

        .navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #1E40AF;
            padding: 14px 28px;
            border-radius: 0 0 12px 12px;
            margin-bottom: 18px;
            gap: 12px;
        }

        .navbar .brand {
            font-size: 1.35rem;
            font-weight: 900;
            color: #ffffff !important;
            letter-spacing: 2px;
        }

        .navbar .tagline {
            font-size: 0.78rem;
            color: rgba(255,255,255,0.82) !important;
            margin-top: 2px;
        }

        .navbar div,
        .navbar span {
            color: #ffffff !important;
        }

        .nav-user {
            color: #ffffff !important;
            font-size: 0.88rem;
            font-weight: 600;
        }

        .nav-button-area {
            margin: 0.2rem auto 2.2rem auto;
            max-width: 580px;
        }

        div[data-testid="stButton"] > button {
            border-radius: 8px;
            border: 1px solid #CBD5E1;
            background-color: #ffffff;
            color: #1E293B;
            font-weight: 600;
            min-height: 2.7rem;
        }

        div[data-testid="stButton"] > button:hover {
            background-color: #F1F5F9;
            border-color: #94A3B8;
            color: #1E293B;
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #2563EB;
            color: #ffffff;
            border-color: #2563EB;
            font-weight: 700;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #1D4ED8;
            border-color: #1D4ED8;
            color: #ffffff;
        }

        input, textarea,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: #ffffff !important;
            color: #1E293B !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #94A3B8 !important;
        }

        [data-testid="stSelectbox"] > div > div {
            background-color: #ffffff !important;
            color: #1E293B !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
        }

        .welcome-box {
            max-width: 390px;
            margin: 70px auto 20px auto;
            text-align: center;
        }

        .welcome-title {
            font-size: 2.45rem;
            font-weight: 900;
            color: #1E293B !important;
            letter-spacing: 3px;
            margin-bottom: 6px;
        }

        .welcome-sub {
            color: #64748B !important;
            font-size: 0.96rem;
            margin-bottom: 36px;
        }

        .auth-wrap {
            max-width: 430px;
            margin: 22px auto;
        }

        .auth-wrap h2 {
            color: #1E293B !important;
            font-size: 1.55rem;
            margin-bottom: 4px;
        }

        .auth-sub {
            color: #64748B !important;
            font-size: 0.88rem;
            margin-bottom: 20px;
        }

        .page-title {
            font-size: 2.75rem;
            font-weight: 900;
            letter-spacing: 0.03rem;
            margin: 0 0 0.5rem 0;
            color: #1E293B !important;
        }

        .page-subtitle {
            font-size: 1.05rem;
            color: #475569 !important;
            margin-bottom: 2rem;
        }

        .rcard {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 8px;
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .rtitle {
            font-weight: 800;
            font-size: 1rem;
            color: #1E293B !important;
        }

        .rmeta {
            font-size: 0.78rem;
            color: #64748B !important;
            margin: 6px 0 10px;
        }

        .rbadge {
            display: inline-block;
            border: 1px solid #CBD5E1;
            border-radius: 5px;
            font-size: 0.7rem;
            font-weight: 800;
            padding: 3px 9px;
            color: #475569 !important;
            text-transform: uppercase;
            background: #F8FAFC;
        }

        .fcard {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 24px;
            background: #ffffff;
            margin-bottom: 18px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .admin-card {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            background: #ffffff;
            padding: 12px 16px;
            margin-bottom: 10px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .admin-title {
            font-weight: 800;
            font-size: 0.95rem;
            color: #1E293B !important;
        }

        .admin-small {
            font-size: 0.78rem;
            color: #64748B !important;
            margin-top: 2px;
        }

        @media (max-width: 760px) {
            .navbar {
                align-items: flex-start;
                flex-direction: column;
            }

            .page-title {
                font-size: 2rem;
            }

            .welcome-title {
                font-size: 2rem;
            }

            .nav-button-area {
                max-width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar():
    pagina = st.session_state.get("pagina", "bienvenida")
    usuario = st.session_state.get("usuario_nombre", "")

    st.markdown(
        f"""
        <div class="navbar">
            <div>
                <div class="brand">WARA WAVE</div>
                <div class="tagline">Por playas más seguras</div>
            </div>
            <div>
                <span class="nav-user">{usuario if usuario else ""}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if pagina in ("bienvenida", "login", "registro"):
        return

    st.markdown('<div class="nav-button-area">', unsafe_allow_html=True)

    cols = st.columns(4)

    with cols[0]:
        if st.button("Tablón", use_container_width=True):
            st.session_state["pagina"] = "tablon"
            st.rerun()

    with cols[1]:
        if st.button("Crear", use_container_width=True):
            st.session_state["pagina"] = "crear"
            st.rerun()

    with cols[2]:
        if st.button("Admin", use_container_width=True):
            st.session_state["pagina"] = "admin"
            st.rerun()

    with cols[3]:
        if st.button("Salir", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def pagina_bienvenida():
    st.markdown('<div class="welcome-box">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-title">WARA WAVE</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-sub">Por playas más seguras</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("Iniciar sesión", use_container_width=True, type="primary"):
            st.session_state["pagina"] = "login"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Registrarse", use_container_width=True):
            st.session_state["pagina"] = "registro"
            st.rerun()


def pagina_login():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Iniciar sesión")
    st.markdown(
        '<div class="auth-sub">Ingresa tus credenciales para continuar</div>',
        unsafe_allow_html=True,
    )

    correo = st.text_input("Correo electrónico", placeholder="usuario@gmail.com")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar", use_container_width=True, type="primary"):
        if not correo or not password:
            st.error("Completa todos los campos.")
        else:
            res = (
                supabase.table("usuarios")
                .select("id, nombre")
                .eq("correo", correo.strip().lower())
                .eq("password", hash_password(password))
                .execute()
            )

            if res.data:
                usuario = res.data[0]

                st.session_state["logged_in"] = True
                st.session_state["usuario_id"] = usuario["id"]
                st.session_state["usuario_nombre"] = usuario["nombre"]
                st.session_state["pagina"] = "tablon"
                st.rerun()
            else:
                st.error("No se pudo iniciar sesión: credenciales incorrectas.")

    st.markdown("---")

    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def pagina_registro():
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("## Registrarse")
    st.markdown(
        '<div class="auth-sub">Crea tu cuenta para reportar incidentes</div>',
        unsafe_allow_html=True,
    )

    nombre = st.text_input("Nombre completo")
    correo = st.text_input("Correo electrónico", placeholder="usuario@gmail.com")
    password = st.text_input("Contraseña", type="password")
    password2 = st.text_input("Confirmar contraseña", type="password")

    if st.button("Crear cuenta", use_container_width=True, type="primary"):
        if not nombre or not correo or not password or not password2:
            st.error("Completa todos los campos.")
        elif password != password2:
            st.error("Las contraseñas no coinciden.")
        elif len(password) < 6:
            st.error("La contraseña debe tener al menos 6 caracteres :)")
        else:
            existe = (
                supabase.table("usuarios")
                .select("id")
                .eq("correo", correo.strip().lower())
                .execute()
            )

            if existe.data:
                st.error("Este correo ya está registrado. :)")
            else:
                supabase.table("usuarios").insert(
                    {
                        "nombre": nombre,
                        "correo": correo.strip().lower(),
                        "password": hash_password(password),
                    }
                ).execute()

                st.success("Cuenta creada. Ahora inicia sesión :)")
                time.sleep(1.3)
                st.session_state["pagina"] = "login"
                st.rerun()

    st.markdown("---")

    if st.button("Volver", use_container_width=True):
        st.session_state["pagina"] = "bienvenida"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def pagina_tablon():
    if not st.session_state.get("logged_in"):
        st.session_state["pagina"] = "login"
        st.rerun()

    st.markdown('<div class="page-title">TABLÓN DE REPORTES</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Reportes ciudadanos en tiempo real</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        filtro_playa = st.selectbox("Playa", ["Todas"] + PLAYAS)

    with col2:
        filtro_categoria = st.selectbox("Categoría", ["Todas"] + CATEGORIAS)

    query = supabase.table("reportes").select("*").order("fecha", desc=True)

    if filtro_playa != "Todas":
        query = query.eq("ubicacion", filtro_playa)

    if filtro_categoria != "Todas":
        query = query.eq("categoria", filtro_categoria)

    reportes = query.execute().data or []

    if not reportes:
        st.info("No hay reportes todavía. Sé la primera persona en reportar.")
        return

    for reporte in reportes:
        reporte_id = reporte["id"]
        me_sirve = reporte.get("me_sirve", 0)
        no_me_sirve = reporte.get("no_me_sirve", 0)
        key_expander = f"exp_{reporte_id}"

        if key_expander not in st.session_state:
            st.session_state[key_expander] = False

        categoria = reporte.get("categoria", "") or ""
        imagen_url = reporte.get("imagen_url")
        video_url = reporte.get("video_url")
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="rtitle">{reporte.get("titulo", "Sin título")}</div>
                <div class="rmeta">
                    {format_fecha(reporte.get("fecha", ""))} &nbsp;|&nbsp; {reporte.get("ubicacion", "")}
                </div>
                <span class="rbadge">{categoria}</span>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            col_ver, col_me, col_no = st.columns([4, 1.2, 1.3])

            with col_ver:
                texto_boton = "Ocultar" if st.session_state[key_expander] else "Ver más"

                if st.button(texto_boton, key=f"toggle_{reporte_id}"):
                    st.session_state[key_expander] = not st.session_state[key_expander]
                    st.rerun()

            with col_me:
                if st.button(f"Me sirve {me_sirve}", key=f"me_{reporte_id}"):
                    supabase.table("reportes").update(
                        {"me_sirve": me_sirve + 1}
                    ).eq("id", reporte_id).execute()
                    st.rerun()

            with col_no:
                if st.button(f"No me sirve {no_me_sirve}", key=f"no_{reporte_id}"):
                    supabase.table("reportes").update(
                        {"no_me_sirve": no_me_sirve + 1}
                    ).eq("id", reporte_id).execute()
                    st.rerun()

            if st.session_state[key_expander]:
                st.markdown("#### Descripción")
                st.write(reporte.get("descripcion", ""))

                if imagen_url and str(imagen_url).strip():
                    st.markdown("#### Evidencia visual")
                    st.image(imagen_url, use_container_width=True)

                elif video_url and str(video_url).strip():
                    st.markdown("#### Evidencia visual")
                    st.video(video_url)

                else:
                    st.caption("Este reporte no tiene evidencia visual adjunta.")

        st.markdown("<br>", unsafe_allow_html=True)


def pagina_crear():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para crear un reporte.")
        if st.button("Ir a iniciar sesión"):
            st.session_state["pagina"] = "login"
            st.rerun()
        return

    st.markdown('<div class="page-title">CREAR REPORTE</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="page-subtitle">
            Proporciona los detalles de la problemática para que las autoridades y la comunidad puedan actuar.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    titulo = st.text_input(
        "Título del reporte",
        placeholder="Ej. Basura en la orilla",
    )

    col1, col2 = st.columns(2)

    with col1:
        categoria = st.selectbox("Categoría", CATEGORIAS)

    with col2:
        ubicacion = st.selectbox("Playa / Ubicación", PLAYAS)

    descripcion = st.text_area(
        "Descripción del problema",
        placeholder="Describe detalladamente lo que observaste",
        height=120,
    )

    archivo = st.file_uploader(
        "Evidencia visual — PNG, JPG, MP4",
        type=["png", "jpg", "jpeg", "gif", "mp4", "webm", "mov"],
    )

    col_cancelar, col_enviar = st.columns(2)

    with col_cancelar:
        if st.button("Cancelar", use_container_width=True):
            st.session_state["pagina"] = "tablon"
            st.rerun()

    with col_enviar:
        if st.button("Enviar reporte", use_container_width=True, type="primary"):
            if not titulo or not descripcion:
                st.error("Título y descripción son obligatorios.")
                return

            imagen_url = None
            video_url = None

            if archivo:
                try:
                    archivo_bytes = archivo.getvalue()
                    extension = archivo.name.split(".")[-1].lower()

                    nombre_archivo = (
                        f"reporte_{st.session_state['usuario_id']}_"
                        f"{int(datetime.now().timestamp())}.{extension}"
                    )

                    bucket = supabase.storage.from_("reportes-imagenes")

                    bucket.upload(
                        nombre_archivo,
                        archivo_bytes,
                        file_options={
                            "content-type": archivo.type,
                            "upsert": "true",
                        },
                    )

                    url_publica = bucket.get_public_url(nombre_archivo)

                    if extension in ["mp4", "webm", "mov"]:
                        video_url = url_publica
                    else:
                        imagen_url = url_publica

                except Exception as e:
                    st.error(f"No se pudo subir la evidencia visual: {e}")
                    st.stop()

            supabase.table("reportes").insert(
                {
                    "usuario_id": st.session_state["usuario_id"],
                    "titulo": titulo,
                    "ubicacion": ubicacion,
                    "categoria": categoria,
                    "descripcion": descripcion,
                    "imagen_url": imagen_url,
                    "video_url": video_url,
                    "me_sirve": 0,
                    "no_me_sirve": 0,
                }
            ).execute()

            st.success("Reporte enviado exitosamente.")
            time.sleep(1.2)
            st.session_state["pagina"] = "tablon"
            st.rerun()


def pagina_admin():
    if not st.session_state.get("logged_in"):
        st.warning("Debes iniciar sesión para acceder.")
        return

    st.markdown('<div class="page-title">ADMINISTRACIÓN</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Gestiona, ordena y modera los reportes ciudadanos.</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    col_espacio, col_orden = st.columns([3, 1])

    with col_orden:
        orden = st.selectbox("Ordenar por votos", ["Mayor a menor", "Menor a mayor"])

    ascendente = orden == "Menor a mayor"

    reportes = (
        supabase.table("reportes")
        .select("*")
        .order("me_sirve", desc=not ascendente)
        .execute()
        .data
        or []
    )

    if not reportes:
        st.info("No hay reportes.")
        return

    st.markdown("<br>", unsafe_allow_html=True)

    col_reporte, col_votos, col_fecha, col_acciones = st.columns([4, 2, 2, 1])

    with col_reporte:
        st.markdown("**Reporte**")

    with col_votos:
        st.markdown("**Votos**")

    with col_fecha:
        st.markdown("**Fecha**")

    with col_acciones:
        st.markdown("**Acciones**")

    st.divider()

    for reporte in reportes:
        reporte_id = reporte["id"]
        categoria = reporte.get("categoria", "") or ""
        fecha = format_fecha(reporte.get("fecha", ""))
        me_sirve = reporte.get("me_sirve", 0)
        no_me_sirve = reporte.get("no_me_sirve", 0)

        with st.container(border=True):
            col_a, col_b, col_c, col_d = st.columns([4, 2, 2, 1])

            with col_a:
                st.markdown(
                    f"""
                    <div class="admin-title">{reporte.get("titulo", "")}</div>
                    <div class="admin-small">{reporte.get("ubicacion", "")}</div>
                    <br>
                    <span class="rbadge">{categoria}</span>
                    """,
                    unsafe_allow_html=True,
                )

            with col_b:
                st.markdown(
                    f"""
                    <div style="font-size:.9rem; line-height:1.7;">
                        Me sirve: <b>{me_sirve}</b><br>
                        No me sirve: <b>{no_me_sirve}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_c:
                st.markdown(
                    f"""
                    <div style="font-size:.9rem;">
                        {fecha}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_d:
                if st.button("Eliminar", key=f"delete_{reporte_id}"):
                    supabase.table("reportes").delete().eq("id", reporte_id).execute()
                    st.rerun()



#main

def main():
    st.set_page_config(
        page_title="Wara Wave",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_css()

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "bienvenida"

    render_navbar()

    pagina = st.session_state["pagina"]

    if pagina == "bienvenida":
        pagina_bienvenida()
    elif pagina == "login":
        pagina_login()
    elif pagina == "registro":
        pagina_registro()
    elif pagina == "tablon":
        pagina_tablon()
    elif pagina == "crear":
        pagina_crear()
    elif pagina == "admin":
        pagina_admin()


if __name__ == "__main__":
    main()