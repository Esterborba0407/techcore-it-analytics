"""Design system (CSS customizado) do TechCore IT Analytics."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Space+Grotesk:wght@600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% -10%, #16255a 0%, #060b1d 45%, #030512 100%);
    color: #f5f7ff;
}

[data-testid="stSidebar"] {
    background: #050a1c;
    border-right: 1px solid #1d2a52;
}

/* ---------- Cabeçalho / Hero ---------- */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6dd5ff 0%, #7c8bff 45%, #ff7ce0 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0;
    line-height: 1.1;
}
.hero-subtitle { color: #9eacd0; margin-top: 4px; font-size: 1.02rem; }

.badge-live {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(38,217,163,.12); border: 1px solid rgba(38,217,163,.4);
    color: #26d9a3; padding: 4px 12px; border-radius: 999px; font-size: .75rem; font-weight: 600;
    margin-bottom: 10px;
}
.badge-live span.dot {
    width: 7px; height: 7px; border-radius: 50%; background: #26d9a3; box-shadow: 0 0 8px #26d9a3;
    animation: pulse 1.6s infinite;
}
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: .35; } 100% { opacity: 1; } }

/* ---------- KPIs ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #101d3e, #0b1530);
    border: 1px solid #263967;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,.18);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 30px rgba(80,100,255,.25);
    border-color: #4a63c9;
}
[data-testid="stMetricValue"] { color: #ffffff; }
h1, h2, h3 { color: #ffffff !important; }
.subtitle { color: #9eacd0; margin-top: -12px; }

/* ---------- Cartões genéricos ---------- */
.glass-card {
    background: rgba(16,29,62,.55);
    border: 1px solid #263967;
    border-radius: 18px;
    padding: 18px 20px;
    backdrop-filter: blur(6px);
    margin-bottom: 12px;
}
.glass-card h4 { margin-top: 0; color: #d8e0ff !important; }
.glass-card p { color: #c3cdf0; font-size: .93rem; line-height: 1.5; margin: 0 0 6px 0; }

/* ---------- Alertas ---------- */
.alert { padding: 12px 14px; border-radius: 12px; margin-bottom: 10px; background: #121d3b; border: 1px solid #283967; }
.alert-danger { border-left: 4px solid #ff4f81; }
.alert-warning { border-left: 4px solid #ffb84d; }
.alert-success { border-left: 4px solid #26d9a3; }

/* ---------- Abas ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #0b1430; border-radius: 10px 10px 0 0; padding: 8px 16px; color: #9eacd0;
}
.stTabs [aria-selected="true"] { background: #17224a !important; color: #ffffff !important; }

/* ---------- Botões ---------- */
.stButton > button, .stDownloadButton > button {
    border-radius: 10px; border: 1px solid #3a4f9e;
    background: linear-gradient(135deg, #2b3f8c, #5c3fb8);
    color: #ffffff; font-weight: 600; transition: all .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px); box-shadow: 0 8px 18px rgba(100,90,255,.35);
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: #26355e; border-radius: 8px; }

/* ---------- Rodapé ---------- */
.footer-note { color: #6c7aa5; font-size: .8rem; text-align: center; margin-top: 18px; }
</style>
"""
