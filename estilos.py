import streamlit as st


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