import streamlit as st


# --------------------------------------------------
# AVAILABLE THEMES
# --------------------------------------------------

THEMES = {
    "🌸 Pastel Dream": {
        "background": "#FFF4F8",
        "surface": "#FFFFFF",
        "sidebar": "#F3E4FA",
        "primary": "#A855C7",
        "secondary": "#F472B6",
        "text": "#382344",
        "muted": "#796580",
        "border": "#E7D3EF",
        "button_text": "#FFFFFF",
        "card_accent": "#FCE7F3",
        "banner": "#F8E7FC",
        "shadow": "rgba(168, 85, 199, 0.10)",
    },
    "🌙 Midnight AI": {
        "background": "#0F1020",
        "surface": "#191A30",
        "sidebar": "#15162A",
        "primary": "#A78BFA",
        "secondary": "#7C3AED",
        "text": "#F5F3FF",
        "muted": "#B5B0D0",
        "border": "#34304F",
        "button_text": "#FFFFFF",
        "card_accent": "#24213F",
        "banner": "#211C3A",
        "shadow": "rgba(0, 0, 0, 0.18)",
    },
    "🤍 Clean Minimal": {
        "background": "#F4F7FC",
        "surface": "#FFFFFF",
        "sidebar": "#EAF0FA",
        "primary": "#6254D9",
        "secondary": "#8B7CF6",
        "text": "#202642",
        "muted": "#65708A",
        "border": "#DCE3F0",
        "button_text": "#FFFFFF",
        "card_accent": "#EAE8FF",
        "banner": "#E8EDFF",
        "shadow": "rgba(54, 65, 120, 0.08)",
    },
    "💙 Cyber Academic": {
        "background": "#071521",
        "surface": "#102536",
        "sidebar": "#0B1D2B",
        "primary": "#22D3EE",
        "secondary": "#3B82F6",
        "text": "#E6F7FF",
        "muted": "#9BBACB",
        "border": "#244457",
        "button_text": "#071521",
        "card_accent": "#153448",
        "banner": "#102D40",
        "shadow": "rgba(0, 0, 0, 0.22)",
    },
}


# --------------------------------------------------
# APPLY SELECTED THEME
# --------------------------------------------------

def apply_theme():
    selected_theme = st.session_state.get(
        "selected_theme",
        "🌸 Pastel Dream",
    )

    theme = THEMES.get(
        selected_theme,
        THEMES["🌸 Pastel Dream"],
    )

    # CSS uses a normal string, not an f-string.
    # Theme values are inserted using unique placeholders.

    css = """
    <style>
    :root {
        --app-bg: THEME_BACKGROUND;
        --app-surface: THEME_SURFACE;
        --app-sidebar: THEME_SIDEBAR;
        --app-primary: THEME_PRIMARY;
        --app-secondary: THEME_SECONDARY;
        --app-text: THEME_TEXT;
        --app-muted: THEME_MUTED;
        --app-border: THEME_BORDER;
        --app-accent: THEME_ACCENT;
        --app-banner: THEME_BANNER;
        --app-shadow: THEME_SHADOW;
    }

    /* GLOBAL */

    .stApp {
        background: var(--app-bg);
        color: var(--app-text);
    }

    [data-testid="stHeader"],
    [data-testid="stMain"] {
        background: var(--app-bg);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;
    }

    /* HIDE AUTOMATIC PAGE NAVIGATION */

    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background: var(--app-sidebar);
        border-right: 1px solid var(--app-border);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: var(--app-text) !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: var(--app-muted) !important;
    }

    /* NAVIGATION */

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 10px;
        padding-top: 5px;
        padding-bottom: 5px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: var(--app-accent);
    }

    /* THEME SELECTOR */

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: var(--app-surface) !important;
        border: 1px solid var(--app-border) !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: var(--app-text) !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="option"] {
        background-color: var(--app-surface) !important;
        color: var(--app-text) !important;
    }

    [data-baseweb="popover"] [role="option"]:hover {
        background-color: var(--app-accent) !important;
        color: var(--app-text) !important;
    }

    /* TYPOGRAPHY */

    h1, h2, h3, h4, h5 {
        color: var(--app-text);
        letter-spacing: -0.35px;
    }

    p, label {
        color: var(--app-text);
    }

    [data-testid="stCaptionContainer"] p {
        color: var(--app-muted);
    }

    [data-testid="stMarkdownContainer"] a {
        color: var(--app-primary);
    }

    /* WELCOME BANNER */

    .welcome-banner {
        background: linear-gradient(
            120deg,
            var(--app-banner),
            var(--app-surface)
        );
        border: 1px solid var(--app-border);
        border-left: 6px solid var(--app-primary);
        border-radius: 22px;
        padding: 30px 32px;
        margin: 8px 0 26px 0;
        box-shadow: 0 5px 20px var(--app-shadow);
    }

    .welcome-banner h1 {
        color: var(--app-text);
        font-size: 2.35rem;
        font-weight: 750;
        margin: 10px 0;
    }

    .welcome-banner p {
        color: var(--app-muted);
        font-size: 1.03rem;
        line-height: 1.7;
        margin-bottom: 0;
    }

    .welcome-label {
        color: var(--app-primary);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 2px;
    }

    /* DASHBOARD CARDS */

    .metric-card {
        background: var(--app-surface);
        border: 1px solid var(--app-border);
        border-radius: 18px;
        padding: 21px;
        min-height: 145px;
        box-shadow: 0 5px 18px var(--app-shadow);
        transition: transform 0.2s ease,
                    border-color 0.2s ease,
                    box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--app-primary);
        box-shadow: 0 8px 22px var(--app-shadow);
    }

    .metric-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: var(--app-accent);
        border-radius: 12px;
        padding: 8px;
        font-size: 1.45rem;
        margin-bottom: 12px;
    }

    .metric-label {
        color: var(--app-muted);
        font-size: 0.86rem;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--app-primary);
        font-size: 1.65rem;
        font-weight: 800;
        overflow-wrap: anywhere;
    }

    /* STREAMLIT METRICS */

    [data-testid="stMetric"] {
        background: var(--app-surface);
        border: 1px solid var(--app-border);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 14px var(--app-shadow);
    }

    [data-testid="stMetricLabel"] {
        color: var(--app-muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--app-primary);
    }

    /* CONTENT CONTAINERS */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--app-surface);
        border-color: var(--app-border);
        border-radius: 18px;
    }

    [data-testid="stAlert"] {
        background: var(--app-accent);
        border-radius: 14px;
        border-color: var(--app-border);
    }

    hr {
        border-color: var(--app-border);
    }

    /* BUTTONS */

    .stButton > button {
        background: var(--app-primary);
        color: THEME_BUTTON_TEXT;
        border: 1px solid var(--app-primary);
        border-radius: 12px;
        min-height: 44px;
        font-weight: 650;
        transition: filter 0.2s ease,
                    transform 0.2s ease;
    }

    .stButton > button p {
        color: THEME_BUTTON_TEXT;
    }

    .stButton > button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
        border-color: var(--app-secondary);
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 2px var(--app-secondary);
    }

    /* INPUTS */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: var(--app-surface);
        color: var(--app-text);
        border: 1px solid var(--app-border);
        border-radius: 10px;
    }

    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input {
        background: var(--app-surface);
        color: var(--app-text);
        border-radius: 10px;
    }

    /* FOOTER */

    .dashboard-footer {
        color: var(--app-muted);
        border-top: 1px solid var(--app-border);
        padding-top: 18px;
        text-align: center;
        font-size: 0.85rem;
    }

    /* SMALL SCREENS */

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }

        .welcome-banner {
            padding: 22px;
        }

        .welcome-banner h1 {
            font-size: 1.8rem;
        }

        .metric-card {
            padding: 15px;
        }

        .metric-value {
            font-size: 1.35rem;
        }
    }
    </style>
    """

    # Insert the selected theme's colors safely.

    replacements = {
        "THEME_BACKGROUND": theme["background"],
        "THEME_SURFACE": theme["surface"],
        "THEME_SIDEBAR": theme["sidebar"],
        "THEME_PRIMARY": theme["primary"],
        "THEME_SECONDARY": theme["secondary"],
        "THEME_TEXT": theme["text"],
        "THEME_MUTED": theme["muted"],
        "THEME_BORDER": theme["border"],
        "THEME_ACCENT": theme["card_accent"],
        "THEME_BANNER": theme["banner"],
        "THEME_SHADOW": theme["shadow"],
        "THEME_BUTTON_TEXT": theme["button_text"],
    }

    for placeholder, value in replacements.items():
        css = css.replace(placeholder, value)

    st.markdown(css, unsafe_allow_html=True)
