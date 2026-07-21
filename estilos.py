import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --ww-ink: #12324a;
            --ww-ink-soft: #496879;
            --ww-muted: #708a98;
            --ww-ocean: #087f9c;
            --ww-ocean-dark: #075b77;
            --ww-ocean-deep: #073b59;
            --ww-aqua: #33b9ca;
            --ww-aqua-soft: #dff7fa;
            --ww-sky: #eaf7fc;
            --ww-sand: #fff8ec;
            --ww-coral: #e9684a;
            --ww-coral-soft: #fff0eb;
            --ww-success: #147b63;
            --ww-warning: #9a6207;
            --ww-danger: #b53b3b;
            --ww-surface: #ffffff;
            --ww-surface-soft: #f7fbfd;
            --ww-border: #d5e6ed;
            --ww-border-strong: #b7d4df;
            --ww-shadow-sm: 0 4px 14px rgba(7, 59, 89, 0.07);
            --ww-shadow-md: 0 12px 32px rgba(7, 59, 89, 0.11);
            --ww-radius-sm: 10px;
            --ww-radius: 16px;
            --ww-radius-lg: 24px;
        }

        *, *::before, *::after {
            box-sizing: border-box;
            color-scheme: light !important;
        }

        html {
            scroll-behavior: smooth;
        }

        html, body,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main,
        .stApp {
            color: var(--ww-ink) !important;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 2%, rgba(51, 185, 202, 0.13), transparent 23rem),
                radial-gradient(circle at 96% 10%, rgba(255, 210, 144, 0.15), transparent 24rem),
                linear-gradient(180deg, #f8fdff 0%, #f3fafc 48%, #f9fcfd 100%) !important;
            min-height: 100vh;
        }

        [data-testid="stMainBlockContainer"],
        .main .block-container {
            max-width: 1180px;
            padding-top: 0.7rem;
            padding-bottom: 5rem;
        }

        #MainMenu, footer, header,
        [data-testid="stDecoration"] {
            display: none !important;
        }

        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Texto ---------------------------------------------------------- */
        h1, h2, h3, h4, h5, h6,
        p, label, [data-testid="stMarkdownContainer"] {
            color: var(--ww-ink);
        }

        a {
            color: var(--ww-ocean-dark) !important;
        }

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        small {
            color: var(--ww-muted) !important;
        }

        hr {
            border: 0 !important;
            border-top: 1px solid var(--ww-border) !important;
            margin: 1.6rem 0 !important;
        }

        /* Cabecera ------------------------------------------------------- */
        .navbar {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 86px;
            padding: 16px 24px;
            margin: 0 0 16px;
            gap: 18px;
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 0 0 var(--ww-radius-lg) var(--ww-radius-lg);
            background:
                radial-gradient(circle at 85% 10%, rgba(114, 224, 232, 0.34), transparent 15rem),
                linear-gradient(118deg, #063d5d 0%, #087e99 58%, #16a5b5 100%);
            box-shadow: 0 14px 34px rgba(7, 59, 89, 0.20);
        }

        .navbar::after {
            content: "";
            position: absolute;
            right: -70px;
            bottom: -96px;
            width: 270px;
            height: 150px;
            border: 22px solid rgba(255,255,255,0.08);
            border-radius: 50%;
            transform: rotate(-8deg);
            pointer-events: none;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            z-index: 1;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 46px;
            height: 46px;
            flex: 0 0 46px;
            border-radius: 15px;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.28);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.25);
            font-size: 1.45rem;
        }

        .navbar .brand {
            color: #ffffff !important;
            font-size: 1.28rem;
            font-weight: 900;
            line-height: 1.1;
            letter-spacing: 0.15em;
        }

        .navbar .tagline {
            color: rgba(255,255,255,0.82) !important;
            font-size: 0.76rem;
            margin-top: 4px;
            letter-spacing: 0.02em;
        }

        .nav-profile {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            flex-wrap: wrap;
            gap: 8px;
        }

        .nav-user {
            color: #ffffff !important;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .role-badge {
            display: inline-flex;
            align-items: center;
            min-height: 27px;
            padding: 4px 11px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.38);
            font-size: 0.66rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            box-shadow: 0 4px 12px rgba(7, 59, 89, 0.12);
        }

        .role-ciudadano {
            background: #e5fbff !important;
            color: #075b77 !important;
        }

        .role-administrador {
            background: #fff0eb !important;
            color: #a8432e !important;
        }

        .role-autoridad {
            background: #f0efff !important;
            color: #5545a8 !important;
        }

        /* Navegación de botones ----------------------------------------- */
        .nav-button-area {
            margin: 0.2rem auto 2rem;
            max-width: 760px;
        }

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button,
        div[data-testid="stDownloadButton"] > button {
            min-height: 2.75rem;
            border: 1px solid var(--ww-border-strong) !important;
            border-radius: 12px !important;
            background: rgba(255,255,255,0.94) !important;
            color: var(--ww-ink) !important;
            font-weight: 750 !important;
            box-shadow: 0 3px 10px rgba(7, 59, 89, 0.045);
            transition: transform 160ms ease, box-shadow 160ms ease,
                border-color 160ms ease, background 160ms ease;
        }

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover {
            transform: translateY(-1px);
            border-color: var(--ww-aqua) !important;
            background: #f0fcfe !important;
            color: var(--ww-ocean-deep) !important;
            box-shadow: 0 8px 18px rgba(7, 95, 119, 0.11);
        }

        div[data-testid="stButton"] > button *,
        div[data-testid="stFormSubmitButton"] > button *,
        div[data-testid="stDownloadButton"] > button * {
            color: inherit !important;
        }

        div[data-testid="stButton"] > button:focus-visible,
        div[data-testid="stFormSubmitButton"] > button:focus-visible {
            outline: 3px solid rgba(51, 185, 202, 0.26) !important;
            outline-offset: 2px;
        }

        div[data-testid="stButton"] > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
            color: #ffffff !important;
            border-color: transparent !important;
            background: linear-gradient(135deg, var(--ww-ocean-dark), var(--ww-ocean)) !important;
            box-shadow: 0 8px 18px rgba(8, 127, 156, 0.22);
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
            color: #ffffff !important;
            border-color: transparent !important;
            background: linear-gradient(135deg, #064e68, #0792ad) !important;
            box-shadow: 0 11px 22px rgba(8, 127, 156, 0.28);
        }

        div[data-testid="stButton"] > button:disabled,
        div[data-testid="stButton"] > button[disabled] {
            opacity: 1 !important;
            color: #627c89 !important;
            background: #edf5f7 !important;
            border-color: #d7e5ea !important;
            box-shadow: none !important;
            transform: none !important;
        }

        /* Formularios ---------------------------------------------------- */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input,
        [data-baseweb="select"] > div {
            color: var(--ww-ink) !important;
            background: #ffffff !important;
            border-color: var(--ww-border-strong) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 7px rgba(7, 59, 89, 0.035) !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input {
            min-height: 44px;
        }

        [data-testid="stTextArea"] textarea {
            min-height: 120px;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stDateInput"] input:focus,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--ww-aqua) !important;
            box-shadow: 0 0 0 3px rgba(51, 185, 202, 0.17) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: #91a5af !important;
            opacity: 1 !important;
        }

        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"] {
            color: var(--ww-ink) !important;
            background: #ffffff !important;
        }

        [role="option"] {
            color: var(--ww-ink) !important;
            background: #ffffff !important;
        }

        [role="option"]:hover,
        [aria-selected="true"][role="option"] {
            background: var(--ww-aqua-soft) !important;
            color: var(--ww-ocean-deep) !important;
        }

        [data-testid="stFileUploader"] {
            padding: 4px;
            border-radius: var(--ww-radius);
        }

        [data-testid="stFileUploaderDropzone"] {
            background: linear-gradient(145deg, #fbfeff, #effafd) !important;
            border: 1.5px dashed #8acbd6 !important;
            border-radius: var(--ww-radius) !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: var(--ww-ink-soft) !important;
        }

        [data-testid="stForm"] {
            padding: 1.15rem !important;
            border: 1px solid var(--ww-border) !important;
            border-radius: var(--ww-radius) !important;
            background: rgba(255,255,255,0.92) !important;
            box-shadow: var(--ww-shadow-sm);
        }

        /* Pestañas ------------------------------------------------------- */
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 8px;
            padding: 5px;
            border: 1px solid var(--ww-border);
            border-radius: 14px;
            background: #edf7fa;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            min-height: 42px;
            padding: 8px 15px;
            border-radius: 10px;
            color: var(--ww-ink-soft) !important;
            font-weight: 750;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            color: var(--ww-ocean-deep) !important;
            background: #ffffff !important;
            box-shadow: 0 4px 12px rgba(7, 59, 89, 0.09);
        }

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            display: none;
        }

        /* Encabezados de página ----------------------------------------- */
        .page-title {
            position: relative;
            display: inline-block;
            margin: 0 0 0.45rem;
            color: var(--ww-ocean-deep) !important;
            font-size: clamp(2rem, 4.5vw, 3.05rem);
            font-weight: 950;
            line-height: 1.04;
            letter-spacing: -0.035em;
        }

        .page-title::after {
            content: "";
            display: block;
            width: 74px;
            height: 5px;
            margin-top: 10px;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--ww-aqua), #80d9df);
        }

        .page-subtitle {
            max-width: 780px;
            margin: 0 0 1.8rem;
            color: var(--ww-ink-soft) !important;
            font-size: 1rem;
            line-height: 1.65;
        }

        /* Inicio --------------------------------------------------------- */
        .welcome-box {
            position: relative;
            overflow: hidden;
            max-width: 760px;
            margin: 58px auto 24px;
            padding: 48px 34px 42px;
            text-align: center;
            border: 1px solid rgba(142, 203, 214, 0.60);
            border-radius: 30px;
            background:
                radial-gradient(circle at 14% 0%, rgba(51,185,202,0.20), transparent 18rem),
                radial-gradient(circle at 92% 100%, rgba(255,211,144,0.22), transparent 18rem),
                rgba(255,255,255,0.92);
            box-shadow: var(--ww-shadow-md);
        }

        .welcome-box::before,
        .welcome-box::after {
            content: "";
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }

        .welcome-box::before {
            width: 240px;
            height: 85px;
            left: -62px;
            bottom: -47px;
            border: 14px solid rgba(51,185,202,0.12);
        }

        .welcome-box::after {
            width: 190px;
            height: 65px;
            right: -42px;
            top: -34px;
            border: 12px solid rgba(8,127,156,0.08);
        }

        .welcome-icon {
            display: grid;
            place-items: center;
            width: 76px;
            height: 76px;
            margin: 0 auto 18px;
            border-radius: 24px;
            background: linear-gradient(145deg, #e8fbfd, #cceff4);
            border: 1px solid #b8e4ea;
            box-shadow: 0 12px 24px rgba(8,127,156,0.14);
            font-size: 2.35rem;
        }

        .welcome-eyebrow {
            color: var(--ww-ocean) !important;
            font-size: 0.76rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.18em;
        }

        .welcome-title {
            margin: 8px 0 7px;
            color: var(--ww-ocean-deep) !important;
            font-size: clamp(2.45rem, 7vw, 4.25rem);
            font-weight: 950;
            line-height: 0.98;
            letter-spacing: -0.055em;
        }

        .welcome-sub {
            color: var(--ww-ink-soft) !important;
            font-size: 1.05rem;
            font-weight: 650;
            margin-bottom: 12px;
        }

        .welcome-copy {
            max-width: 560px;
            margin: 0 auto;
            color: var(--ww-muted) !important;
            font-size: 0.94rem;
            line-height: 1.65;
        }

        /* Autenticación -------------------------------------------------- */
        .auth-wrap {
            max-width: 520px;
            margin: 26px auto 8px;
        }

        .auth-heading {
            margin: 0 0 4px;
            color: var(--ww-ocean-deep) !important;
            font-size: 1.8rem;
            font-weight: 900;
            letter-spacing: -0.025em;
        }

        .auth-sub {
            margin-bottom: 20px;
            color: var(--ww-muted) !important;
            font-size: 0.9rem;
        }

        /* Contenedores, tarjetas y reportes ------------------------------ */
        [data-testid="stVerticalBlockBorderWrapper"] {
            overflow: hidden;
            border: 1px solid var(--ww-border) !important;
            border-radius: var(--ww-radius-lg) !important;
            background: rgba(255,255,255,0.94) !important;
            box-shadow: var(--ww-shadow-sm);
            transition: transform 170ms ease, box-shadow 170ms ease,
                border-color 170ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-1px);
            border-color: #b9dce4 !important;
            box-shadow: var(--ww-shadow-md);
        }

        .rcard {
            padding: 4px 2px 1px;
        }

        .rtitle {
            color: var(--ww-ocean-deep) !important;
            font-size: 1.08rem;
            font-weight: 880;
            line-height: 1.35;
        }

        .rmeta {
            margin: 7px 0 11px;
            color: var(--ww-muted) !important;
            font-size: 0.79rem;
            line-height: 1.5;
        }

        .rbadge {
            display: inline-flex;
            align-items: center;
            min-height: 26px;
            margin: 0 5px 5px 0;
            padding: 4px 10px;
            border: 1px solid #bcdfe6;
            border-radius: 999px;
            background: var(--ww-aqua-soft);
            color: var(--ww-ocean-dark) !important;
            font-size: 0.67rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.055em;
        }

        .status-badge {
            border-color: #f0cdbb !important;
            background: var(--ww-coral-soft) !important;
            color: #a14934 !important;
        }

        .fcard,
        .admin-card {
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid var(--ww-border);
            border-radius: var(--ww-radius);
            background: rgba(255,255,255,0.94);
            box-shadow: var(--ww-shadow-sm);
        }

        .admin-title {
            color: var(--ww-ocean-deep) !important;
            font-size: 1rem;
            font-weight: 880;
        }

        .admin-small {
            margin-top: 3px;
            color: var(--ww-muted) !important;
            font-size: 0.78rem;
        }

        [data-testid="stExpander"] {
            overflow: hidden;
            border: 1px solid var(--ww-border) !important;
            border-radius: 14px !important;
            background: #fbfeff !important;
        }

        [data-testid="stExpander"] summary {
            color: var(--ww-ocean-deep) !important;
            font-weight: 750 !important;
        }

        [data-testid="stImage"] img,
        [data-testid="stVideo"] video,
        iframe {
            border-radius: 14px !important;
            box-shadow: 0 7px 20px rgba(7,59,89,0.10);
        }

        /* Métricas ------------------------------------------------------- */
        [data-testid="stMetric"] {
            min-height: 108px;
            padding: 16px 17px;
            border: 1px solid var(--ww-border);
            border-radius: var(--ww-radius);
            background:
                linear-gradient(145deg, rgba(255,255,255,0.98), rgba(238,249,252,0.92));
            box-shadow: var(--ww-shadow-sm);
        }

        [data-testid="stMetricLabel"] {
            color: var(--ww-ink-soft) !important;
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--ww-ocean-deep) !important;
            font-weight: 900;
        }

        /* Riesgo del mar ------------------------------------------------- */
        .risk-card {
            display: flex;
            align-items: center;
            gap: 18px;
            margin: 14px 0 24px;
            padding: 20px 22px;
            border: 1px solid;
            border-radius: var(--ww-radius-lg);
            box-shadow: var(--ww-shadow-sm);
        }

        .risk-icon {
            display: grid;
            place-items: center;
            width: 55px;
            height: 55px;
            flex: 0 0 55px;
            border-radius: 17px;
            background: rgba(255,255,255,0.63);
            font-size: 2rem;
        }

        .risk-label {
            font-size: 1.15rem;
            font-weight: 920;
        }

        .risk-text {
            margin-top: 4px;
            font-size: 0.91rem;
            line-height: 1.5;
        }

        .riesgo-tranquilo {
            border-color: #83d6c0;
            background: linear-gradient(145deg, #ecfbf6, #dcf5ec);
        }
        .riesgo-tranquilo .risk-label,
        .riesgo-tranquilo .risk-text { color: #0a6553 !important; }

        .riesgo-moderado {
            border-color: #efd28b;
            background: linear-gradient(145deg, #fffbed, #fff4cf);
        }
        .riesgo-moderado .risk-label,
        .riesgo-moderado .risk-text { color: #80570b !important; }

        .riesgo-fuerte {
            border-color: #efb180;
            background: linear-gradient(145deg, #fff7ee, #ffe9d5);
        }
        .riesgo-fuerte .risk-label,
        .riesgo-fuerte .risk-text { color: #91451e !important; }

        .riesgo-peligroso {
            border-color: #eca3a3;
            background: linear-gradient(145deg, #fff3f3, #ffe2e2);
        }
        .riesgo-peligroso .risk-label,
        .riesgo-peligroso .risk-text { color: #9f2f2f !important; }

        /* Mensajes de estado -------------------------------------------- */
        [data-testid="stAlert"] {
            border-radius: 14px !important;
            border-width: 1px !important;
            box-shadow: 0 4px 12px rgba(7,59,89,0.05);
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div {
            color: inherit !important;
        }

        /* Tablas --------------------------------------------------------- */
        [data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid var(--ww-border);
            border-radius: var(--ww-radius);
            box-shadow: var(--ww-shadow-sm);
        }

        /* Responsivo ----------------------------------------------------- */
        @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"],
            .main .block-container {
                padding: 0.35rem 0.75rem 4rem;
            }

            .navbar {
                min-height: auto;
                align-items: flex-start;
                flex-direction: column;
                padding: 14px 15px;
                border-radius: 0 0 19px 19px;
            }

            .brand-mark {
                width: 42px;
                height: 42px;
                flex-basis: 42px;
            }

            .nav-profile {
                justify-content: flex-start;
            }

            [data-testid="stHorizontalBlock"] {
                flex-wrap: wrap;
                gap: 0.55rem;
            }

            [data-testid="column"] {
                min-width: 145px;
                flex: 1 1 145px !important;
            }

            .welcome-box {
                margin-top: 30px;
                padding: 36px 18px 32px;
                border-radius: 23px;
            }

            .welcome-icon {
                width: 66px;
                height: 66px;
                border-radius: 20px;
                font-size: 2rem;
            }

            .page-title {
                font-size: 2.05rem;
            }

            .page-subtitle {
                font-size: 0.94rem;
            }

            .risk-card {
                align-items: flex-start;
                padding: 16px;
            }

            [data-testid="stMetric"] {
                min-height: 98px;
            }
        }

        @media (max-width: 440px) {
            [data-testid="column"] {
                min-width: 100%;
                flex-basis: 100% !important;
            }

            .navbar .brand {
                font-size: 1.08rem;
            }

            .role-badge {
                margin-left: 0;
            }

            .welcome-title {
                font-size: 2.55rem;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                scroll-behavior: auto !important;
                transition: none !important;
                animation: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )