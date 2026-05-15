import streamlit as st
import os
import re
from pathlib import Path
import base64
from io import BytesIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocuMind – Document Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root vars ── */
:root {
    --bg:          #0a0a0f;
    --bg2:         #0d0d15;
    --surface:     #12121e;
    --surface2:    #1a1a2e;
    --surface3:    #1e1e35;
    --border:      #2a2a4a;
    --border2:     #3a3a6a;
    --gold:        #f0c060;
    --gold2:       #e8a030;
    --violet:      #9d6fff;
    --violet2:     #7b4fe0;
    --teal:        #40e0c0;
    --text:        #f0eeff;
    --text-muted:  #9090b8;
    --text-dim:    #6060a0;
    --success:     #40c880;
    --radius:      12px;
    --radius-lg:   18px;
}

/* ── Global ── */
html, body { background-color: var(--bg) !important; }
[class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Decorative background pattern ── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 20% 0%, rgba(157,111,255,.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 30% at 80% 100%, rgba(64,224,192,.07) 0%, transparent 60%),
        var(--bg) !important;
}

/* ══════════════════════════════════
   SIDEBAR
══════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0e1c 0%, #10101f 100%) !important;
    border-right: 1px solid var(--border2) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,.5) !important;
}

/* Force all sidebar text white */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *:not(button):not(.sidebar-brand h1) {
    color: var(--text) !important;
}

/* Sidebar section labels */
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text) !important;
    font-weight: 600 !important;
    letter-spacing: .03em !important;
}

/* ── Sidebar brand ── */
.sidebar-brand {
    background: linear-gradient(135deg, #161630 0%, #1a1040 100%);
    border-bottom: 1px solid var(--border2);
    padding: 30px 20px 24px;
    margin: -1rem -1rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.sidebar-brand::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 70% 80% at 50% -10%, rgba(157,111,255,.25), transparent);
    pointer-events: none;
}
.sidebar-brand h1 {
    font-family: 'Cinzel', serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, var(--gold), var(--violet), var(--teal));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin: 0 0 6px !important;
    letter-spacing: .06em !important;
}
.sidebar-brand p {
    color: var(--text-muted) !important;
    font-size: 0.76rem !important;
    margin: 0 !important;
    letter-spacing: .08em !important;
    text-transform: uppercase !important;
}

/* ── Sidebar input fields (folder path, api key) ── */
[data-testid="stSidebar"] .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    caret-color: var(--violet) !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: var(--text-dim) !important; opacity: 1 !important; }
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(157,111,255,.18) !important;
    outline: none !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border2) !important;
    border-radius: var(--radius-lg) !important;
    transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--violet) !important;
    background: var(--surface3) !important;
}
/* all text inside the dropzone */
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stFileUploaderDropzoneInstructions"] *,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: var(--text) !important;
    opacity: 1 !important;
}
/* secondary hint text */
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: var(--text-muted) !important;
}
/* Browse files button */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] [data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, var(--violet2), var(--violet)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    box-shadow: 0 2px 12px rgba(157,111,255,.35) !important;
}
/* uploaded file name pills */
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    background: rgba(157,111,255,.12) !important;
    border: 1px solid rgba(157,111,255,.3) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] * {
    color: var(--text) !important;
}

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--violet2), var(--violet)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: .04em !important;
    padding: 9px 16px !important;
    transition: all .2s !important;
    box-shadow: 0 2px 12px rgba(157,111,255,.3) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(157,111,255,.45) !important;
}

/* ── Stats cards ── */
.stat-card {
    background: linear-gradient(135deg, var(--surface2), var(--surface3));
    border: 1px solid var(--border2);
    border-radius: var(--radius);
    padding: 14px 12px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,.4);
}
.stat-card .num {
    font-family: 'Cinzel', serif;
    font-size: 1.8rem; font-weight: 700;
    background: linear-gradient(90deg, var(--gold), var(--violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-card .lbl {
    color: var(--text-muted) !important;
    font-size: 0.7rem; letter-spacing: .08em; text-transform: uppercase; margin-top: 4px;
}

/* ══════════════════════════════════
   MAIN AREA
══════════════════════════════════ */
[data-testid="stMain"],
[data-testid="stMain"] * { color: var(--text) !important; }

/* ── Main header ── */
.main-header {
    padding: 2.5rem 1rem 1.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
}
.main-header::after {
    content: '';
    display: block;
    width: 120px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), var(--violet), transparent);
    margin: 1rem auto 0;
    border-radius: 2px;
}
.main-header h2 {
    font-family: 'Cinzel', serif !important;
    font-size: 2.2rem !important; font-weight: 700 !important;
    background: linear-gradient(90deg, var(--gold), var(--violet), var(--teal));
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    margin: 0 0 8px !important; letter-spacing: .05em !important;
}
.main-header p { color: var(--text-muted) !important; font-size: 0.88rem !important; margin: 0 !important; letter-spacing: .04em !important; }

/* ── Chat bubbles ── */
.chat-wrap { display: flex; flex-direction: column; gap: 1.4rem; padding-bottom: 1rem; }

.msg-user { display: flex; justify-content: flex-end; }
.msg-user .bubble {
    background: linear-gradient(135deg, var(--violet2) 0%, #5a2fb0 100%);
    color: #fff !important;
    padding: 14px 20px;
    border-radius: var(--radius-lg) var(--radius-lg) 4px var(--radius-lg);
    max-width: 70%; font-size: 0.93rem; line-height: 1.65;
    box-shadow: 0 6px 24px rgba(123,79,224,.35);
    border: 1px solid rgba(157,111,255,.3);
}

.msg-bot { display: flex; align-items: flex-start; gap: 12px; }
.msg-bot .avatar {
    width: 38px; height: 38px; border-radius: 50%; flex-shrink: 0; margin-top: 2px;
    background: linear-gradient(135deg, var(--gold2), var(--violet));
    display: flex; align-items: center; justify-content: center; font-size: 1.05rem;
    box-shadow: 0 4px 14px rgba(157,111,255,.4);
}
.msg-bot .bubble {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
    border: 1px solid var(--border2);
    color: var(--text) !important;
    padding: 16px 22px;
    border-radius: 4px var(--radius-lg) var(--radius-lg) var(--radius-lg);
    max-width: 80%; font-size: 0.93rem; line-height: 1.75;
    box-shadow: 0 6px 28px rgba(0,0,0,.45);
}

/* ── Source badge ── */
.source-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(157,111,255,.12); border: 1px solid rgba(157,111,255,.3);
    border-radius: 20px; padding: 4px 12px;
    font-size: 0.72rem; color: var(--text-muted) !important;
    margin-top: 10px; margin-right: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Query input (search bar) ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--text) !important;
    caret-color: var(--violet) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px 20px !important;
    transition: all .25s !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-dim) !important; opacity: 1 !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--violet) !important;
    background: var(--surface3) !important;
    box-shadow: 0 0 0 4px rgba(157,111,255,.15), 0 4px 20px rgba(157,111,255,.12) !important;
    outline: none !important;
}

/* ── Main form submit button ── */
[data-testid="stForm"] .stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--gold2) 0%, var(--gold) 100%) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: var(--radius-lg) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: .05em !important;
    padding: 14px 20px !important;
    transition: all .2s !important;
    box-shadow: 0 4px 18px rgba(240,192,96,.3) !important;
}
[data-testid="stForm"] .stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(240,192,96,.45) !important;
}

/* ── Tables ── */
.msg-bot .bubble table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 0.85rem; }
.msg-bot .bubble th {
    background: rgba(157,111,255,.15); color: var(--gold) !important;
    padding: 9px 14px; text-align: left; border: 1px solid var(--border2);
    font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing: .05em;
}
.msg-bot .bubble td {
    padding: 8px 14px; border: 1px solid var(--border); vertical-align: top; color: var(--text) !important;
}
.msg-bot .bubble tr:nth-child(even) td { background: rgba(255,255,255,.03); }

/* ── Code blocks ── */
.msg-bot .bubble code, .msg-bot .bubble pre {
    background: rgba(0,0,0,.4) !important; border-radius: 8px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
    color: var(--teal) !important; border: 1px solid var(--border);
}

/* ── Divider ── */
hr { border-color: var(--border2) !important; }

/* ── Alerts ── */
.stAlert { border-radius: var(--radius) !important; }
.stAlert * { color: inherit !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--violet2); }

/* ── Dataframe toolbar ── */
/* wrapper — no overflow:hidden so toolbar overlay is never clipped */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; }

/* toolbar container */
[data-testid="stElementToolbar"] {
    background: var(--surface3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    padding: 4px 6px !important;
    gap: 2px !important;
    opacity: 1 !important;
    visibility: visible !important;
    display: flex !important;
    align-items: center !important;
}

/* every button in the toolbar */
[data-testid="stElementToolbar"] button {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 7px !important;
    color: var(--text) !important;
    width: 30px !important;
    height: 30px !important;
    padding: 5px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    opacity: 1 !important;
    visibility: visible !important;
    transition: background .15s, border-color .15s !important;
}
[data-testid="stElementToolbar"] button:hover {
    background: rgba(157,111,255,.25) !important;
    border-color: var(--violet) !important;
}

/* force every SVG shape inside toolbar buttons to be white */
[data-testid="stElementToolbar"] button svg { overflow: visible !important; }
[data-testid="stElementToolbar"] button svg *,
[data-testid="stElementToolbar"] button svg path,
[data-testid="stElementToolbar"] button svg polyline,
[data-testid="stElementToolbar"] button svg line,
[data-testid="stElementToolbar"] button svg rect,
[data-testid="stElementToolbar"] button svg circle,
[data-testid="stElementToolbar"] button svg polygon {
    stroke: var(--text) !important;
    fill: none !important;
    opacity: 1 !important;
    visibility: visible !important;
}
[data-testid="stElementToolbar"] button:hover svg *,
[data-testid="stElementToolbar"] button:hover svg path,
[data-testid="stElementToolbar"] button:hover svg polyline,
[data-testid="stElementToolbar"] button:hover svg line,
[data-testid="stElementToolbar"] button:hover svg rect,
[data-testid="stElementToolbar"] button:hover svg circle,
[data-testid="stElementToolbar"] button:hover svg polygon {
    stroke: var(--violet) !important;
}

/* ── Dataframe search input (appears in toolbar when search is clicked) ── */
[data-testid="stDataFrame"] input,
[data-testid="stDataFrameResizable"] input,
[data-testid="stElementToolbar"] input,
[data-testid="stElementToolbar"] + div input,
[class*="stDataFrame"] input,
[class*="dataframe"] input {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    caret-color: var(--violet) !important;
    outline: none !important;
}
[data-testid="stDataFrame"] input::placeholder,
[data-testid="stDataFrameResizable"] input::placeholder,
[data-testid="stElementToolbar"] input::placeholder {
    color: var(--text-dim) !important;
    opacity: 1 !important;
}
[data-testid="stDataFrame"] input:focus,
[data-testid="stDataFrameResizable"] input:focus,
[data-testid="stElementToolbar"] input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(157,111,255,.2) !important;
}

/* ── Thinking / loading dots ── */
.thinking-dots {
    display: inline-flex;
    gap: 5px;
    align-items: center;
    height: 20px;
}
.thinking-dots span {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--violet);
    display: inline-block;
    animation: thinking-bounce 1.2s infinite ease-in-out;
}
.thinking-dots span:nth-child(1) { animation-delay: 0s; }
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes thinking-bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%            { transform: scale(1.2); opacity: 1; }
}

/* ── Stop button — styled via dynamic injection in Python, not here ── */

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }

/* ── Header — themed to match app ── */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #0e0e1c 0%, #10101f 100%) !important;
    border-bottom: 1px solid var(--border2) !important;
    box-shadow: 0 2px 16px rgba(0,0,0,.4) !important;
}

/* All text/icons inside header */
header[data-testid="stHeader"] * {
    color: var(--text) !important;
    fill: var(--text) !important;
}

/* Deploy button */
header[data-testid="stHeader"] [data-testid="stDeployButton"],
header[data-testid="stHeader"] [data-testid="stDeployButton"] * {
    background: linear-gradient(135deg, var(--violet2), var(--violet)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: .82rem !important;
    letter-spacing: .03em !important;
}
header[data-testid="stHeader"] [data-testid="stDeployButton"]:hover {
    background: linear-gradient(135deg, var(--violet), var(--gold)) !important;
    box-shadow: 0 0 12px rgba(157,111,255,.5) !important;
}

/* Toolbar icon buttons (fullscreen, share, etc.) */
header[data-testid="stHeader"] button {
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    transition: background .2s, color .2s !important;
}
header[data-testid="stHeader"] button:hover {
    background: var(--surface3) !important;
    color: var(--gold) !important;
}
header[data-testid="stHeader"] button svg {
    fill: var(--text-muted) !important;
}
header[data-testid="stHeader"] button:hover svg {
    fill: var(--gold) !important;
}

.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Imports (after page config) ───────────────────────────────────────────────
try:
    import fitz  # PyMuPDF
    PYMUPDF_OK = True
except ImportError:
    PYMUPDF_OK = False

try:
    from docx import Document as DocxDocument
    DOCX_OK = True
except ImportError:
    DOCX_OK = False

try:
    import pandas as pd
    PANDAS_OK = True
except ImportError:
    PANDAS_OK = False

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    EMBEDDING_OK = True
except ImportError:
    EMBEDDING_OK = False

try:
    import anthropic
    ANTHROPIC_OK = True
except ImportError:
    ANTHROPIC_OK = False

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = []   # list of {text, source, page, images, tables}
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None
if "loaded_files" not in st.session_state:
    st.session_state.loaded_files = []

# ── Helpers ───────────────────────────────────────────────────────────────────

def img_to_b64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode()


def _get_media_type(img_b64: str) -> str:
    """Detect image MIME type from the opening bytes of its base64 string."""
    if img_b64.startswith("/9j/"):
        return "image/jpeg"
    if img_b64.startswith("R0lG"):
        return "image/gif"
    if img_b64.startswith("Qk"):
        return "image/bmp"
    return "image/png"


def analyze_image(img_b64: str, query: str, api_key: str):
    """
    Classify an image in the context of the user's query.
    Returns (kind, data) where kind is:
      "table"      → image is a table; data = list of rows
      "relevant"   → image is relevant to the query (diagram, figure, text); data = None
      "irrelevant" → logo, watermark, decoration; data = None
    Results are cached per (img_b64, query) so the same image isn't re-sent twice.
    """
    if not ANTHROPIC_OK or not api_key:
        return "irrelevant", None
    cache = st.session_state.setdefault("_img_cache", {})
    cache_key = (img_b64[:64], query[:120])
    if cache_key in cache:
        return cache[cache_key]
    try:
        client = anthropic.Anthropic(api_key=api_key)
        media_type = _get_media_type(img_b64)
        prompt = (
            f"The user asked: \"{query[:200]}\"\n\n"
            "Look at this image and respond with EXACTLY ONE of the following:\n\n"
            "TABLE\n[[row1col1, row1col2, ...], [row2col1, ...], ...]\n"
            "  → Use this if the image IS a table, data grid, or spreadsheet. "
            "    Extract every row and column as a JSON array of arrays.\n\n"
            "RELEVANT\n"
            "  → Use this if the image is a diagram, chart, figure, flowchart, or contains "
            "    text/data that is useful for answering the question.\n\n"
            "IRRELEVANT\n"
            "  → Use this if the image is a logo, watermark, company header, signature, "
            "    decorative element, or otherwise unrelated to the question.\n\n"
            "Reply with ONLY the category keyword (TABLE / RELEVANT / IRRELEVANT) "
            "and, for TABLE only, the JSON array below it."
        )
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64", "media_type": media_type, "data": img_b64}},
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        resp = msg.content[0].text.strip()
        if resp.startswith("TABLE"):
            import json
            m = re.search(r'\[[\s\S]*\]', resp)
            if m:
                try:
                    data = json.loads(m.group())
                    if isinstance(data, list) and len(data) > 1:
                        rows = [[str(c) if c is not None else "" for c in row] for row in data]
                        result = ("table", rows)
                    else:
                        result = ("relevant", None)
                except Exception:
                    result = ("relevant", None)
            else:
                result = ("relevant", None)
        elif resp.startswith("RELEVANT"):
            result = ("relevant", None)
        else:
            result = ("irrelevant", None)
    except Exception:
        result = ("irrelevant", None)
    cache[cache_key] = result
    return result


def extract_pdf(file_bytes: bytes, filename: str):
    """Extract text, tables, images chunk-by-chunk from PDF."""
    chunks = []
    if not PYMUPDF_OK:
        st.warning("PyMuPDF not installed – install with `pip install pymupdf`")
        return chunks
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page_num, page in enumerate(doc, 1):
        text = page.get_text("text").strip()
        images = []
        for img in page.get_images(full=True):
            xref = img[0]
            base = doc.extract_image(xref)
            img_bytes = base["image"]
            images.append(img_to_b64(img_bytes))
        # ── Table extraction: try three methods in order ──────────────────────
        tables = []

        # Method 1: PyMuPDF structural find_tables (best for bordered tables)
        try:
            tbl_list = page.find_tables()
            for t in tbl_list.tables:
                rows = t.extract()
                if rows and len(rows) > 1:
                    tables.append([[str(c) if c is not None else "" for c in row] for row in rows])
        except Exception:
            pass

        # Method 2: Word-position reconstruction (best for borderless/complex tables)
        # Groups words by Y coordinate into rows, sorts by X within each row.
        # Clinical assessment schedules score well here: wide tables with short cells.
        if not tables:
            try:
                words = page.get_text("words")  # (x0,y0,x1,y1,word,blk,ln,wrd)
                if words and len(words) >= 15:
                    TOL = 5  # pt — words within 5pt vertically = same row
                    rows_by_y: dict = {}
                    for w in words:
                        y_key = round(w[1] / TOL) * TOL
                        rows_by_y.setdefault(y_key, []).append((w[0], w[4]))
                    sorted_rows = [
                        [cell[1] for cell in sorted(cells, key=lambda c: c[0])]
                        for _, cells in sorted(rows_by_y.items())
                    ]
                    if len(sorted_rows) >= 4:
                        all_cells = [c for r in sorted_rows for c in r]
                        avg_cols = sum(len(r) for r in sorted_rows) / len(sorted_rows)
                        short_ratio = sum(1 for c in all_cells if len(c) <= 3) / max(len(all_cells), 1)
                        # Wide table OR table with many short cells (x-markers, numbers)
                        if avg_cols >= 6 or (avg_cols >= 3 and short_ratio >= 0.4):
                            tables.append(sorted_rows)
            except Exception:
                pass

        # Method 3: Line-split fallback for x-marker grids with any spacing
        if not tables:
            _XG = re.compile(r'\b[xX]\b.*\b[xX]\b.*\b[xX]\b', re.MULTILINE)
            if _XG.search(text):
                raw_rows = []
                for line in text.splitlines():
                    parts = re.split(r'\s{2,}|\t', line.rstrip())
                    if len(parts) >= 2:
                        raw_rows.append(parts)
                if len(raw_rows) >= 3:
                    tables.append(raw_rows)
        if text or images or tables:
            chunks.append({
                "text": text,
                "source": filename,
                "page": page_num,
                "images": images,
                "tables": tables,
            })
    return chunks


def extract_docx(file_bytes: bytes, filename: str):
    """Extract text, tables, inline images from DOCX."""
    chunks = []
    if not DOCX_OK:
        st.warning("python-docx not installed – install with `pip install python-docx`")
        return chunks
    from docx.oxml.ns import qn
    doc = DocxDocument(BytesIO(file_bytes))
    text_parts = []
    tables = []
    images = []
    for elem in doc.element.body:
        tag = elem.tag.split("}")[-1]
        if tag == "p":
            para_text = "".join(n.text or "" for n in elem.iter() if n.tag.split("}")[-1] == "t")
            if para_text.strip():
                text_parts.append(para_text)
        elif tag == "tbl":
            rows = []
            for row in elem.iter(qn("w:tr")):
                cells = [
                    "".join(n.text or "" for n in cell.iter() if n.tag.split("}")[-1] == "t")
                    for cell in row.iter(qn("w:tc"))
                ]
                rows.append(cells)
            if rows:
                tables.append(rows)
    # Images
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            try:
                img_bytes = rel.target_part.blob
                images.append(img_to_b64(img_bytes))
            except Exception:
                pass
    chunks.append({
        "text": "\n".join(text_parts),
        "source": filename,
        "page": 1,
        "images": images,
        "tables": tables,
    })
    return chunks


def extract_txt(file_bytes: bytes, filename: str):
    text = file_bytes.decode("utf-8", errors="ignore")
    lines = [l for l in text.split("\n") if l.strip()]
    # split into ~500-char chunks
    chunks = []
    buf = []
    buf_len = 0
    for line in lines:
        buf.append(line)
        buf_len += len(line)
        if buf_len > 800:
            chunks.append({"text": "\n".join(buf), "source": filename, "page": len(chunks)+1, "images": [], "tables": []})
            buf, buf_len = [], 0
    if buf:
        chunks.append({"text": "\n".join(buf), "source": filename, "page": len(chunks)+1, "images": [], "tables": []})
    return chunks


def extract_csv(file_bytes: bytes, filename: str):
    if not PANDAS_OK:
        st.warning("pandas not installed – install with `pip install pandas`")
        return []
    import io
    df = pd.read_csv(io.BytesIO(file_bytes))
    rows = [df.columns.tolist()] + df.values.tolist()
    rows = [[str(c) for c in r] for r in rows]
    return [{"text": df.to_string(index=False), "source": filename, "page": 1, "images": [], "tables": [rows]}]


def extract_excel(file_bytes: bytes, filename: str):
    """Extract each sheet of an Excel file as a separate chunk with a table."""
    if not PANDAS_OK:
        st.warning("pandas not installed – install with `pip install pandas openpyxl`")
        return []
    import io
    chunks = []
    try:
        xl = pd.ExcelFile(io.BytesIO(file_bytes), engine="openpyxl")
    except Exception:
        try:
            xl = pd.ExcelFile(io.BytesIO(file_bytes), engine="xlrd")
        except Exception:
            return []
    for page_num, sheet in enumerate(xl.sheet_names, 1):
        try:
            df = xl.parse(sheet)
            if df.empty:
                continue
            rows = [df.columns.tolist()] + df.values.tolist()
            rows = [[str(c) for c in r] for r in rows]
            chunks.append({
                "text": f"Sheet: {sheet}\n" + df.to_string(index=False),
                "source": filename,
                "page": page_num,
                "images": [],
                "tables": [rows],
            })
        except Exception:
            continue
    return chunks


def load_file(uploaded_file):
    name = uploaded_file.name
    data = uploaded_file.read()
    ext = Path(name).suffix.lower()
    if ext == ".pdf":
        return extract_pdf(data, name)
    elif ext == ".docx":
        return extract_docx(data, name)
    elif ext in (".txt", ".md"):
        return extract_txt(data, name)
    elif ext == ".csv":
        return extract_csv(data, name)
    elif ext in (".xlsx", ".xls"):
        return extract_excel(data, name)
    else:
        return extract_txt(data, name)


@st.cache_resource
def get_embedder():
    if not EMBEDDING_OK:
        return None
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks):
    embedder = get_embedder()
    if embedder is None or not chunks:
        return None
    texts = [c["text"][:512] for c in chunks]
    return embedder.encode(texts, show_progress_bar=False)


_DOC_GENERIC = {
    "the", "and", "for", "from", "with", "data", "plan", "review", "file",
    "spec", "guide", "form", "report", "list", "log", "test", "study",
    "clinical", "trial", "version", "final", "draft", "new", "old", "doc",
    "document", "template", "sample", "example", "ref", "information",
}


def _doc_filter(query: str, all_chunks: list) -> tuple:
    """
    Restrict chunks to documents whose name is mentioned in the query.
    Uses a generic-word stoplist so common filename words (data, plan, review…)
    don't cause false matches across unrelated documents.
    Falls back to all chunks only when truly no document name is detected.
    """
    q_lower = query.lower()
    sources = list({c["source"] for c in all_chunks})

    matched = []
    for src in sources:
        stem = Path(src).stem
        # Split on common separators, lowercase each part
        parts = re.split(r'[\s\-_\.]+', stem.lower())
        # Keep only distinctive identifiers: len ≥ 3 and not generic
        distinctive = [p for p in parts if len(p) >= 3 and p not in _DOC_GENERIC]
        # Also test the full stem (space-normalised) as a phrase
        stem_phrase = re.sub(r'[\-_\.]+', ' ', stem.lower())
        identifiers = distinctive + [stem_phrase]
        if any(ident and ident in q_lower for ident in identifiers):
            matched.append(src)

    if not matched:
        # For schedule/table queries prefer protocol-named documents
        SCHED_Q = re.compile(
            r'\b(assessment\s+schedule|schedule\s+of\s+assessments?|'
            r'visit\s+schedule|time\s+and\s+events?|table\s+\d)\b',
            re.IGNORECASE
        )
        if SCHED_Q.search(query):
            proto_docs = [s for s in sources
                          if re.search(r'protocol', Path(s).stem, re.IGNORECASE)]
            if proto_docs:
                matched = proto_docs

    matched_set = set(matched) if matched else {c["source"] for c in all_chunks}
    filtered = [(i, c) for i, c in enumerate(all_chunks) if c["source"] in matched_set]
    indices = [i for i, _ in filtered]
    pool    = [c for _, c in filtered]
    return pool, indices


def _expand_table_refs(retrieved: list, pool: list) -> list:
    """
    Expand retrieved chunks with adjacent pages when table-related content is referenced.
    Looks both forward and backward to handle tables that appear before/after references.
    """
    import re

    TABLE_REF   = re.compile(
        r'\bTable\s+[\d]+(?:[.\-–][\d]+)?|\bFigure\s+[\d]+(?:[.\-–][\d]+)?',
        re.IGNORECASE
    )
    SCHEDULE_KW = re.compile(
        r'\b(schedule\s+of\s+assessments?|assessment\s+schedule|'
        r'visit\s+schedule|study\s+schedule|time\s+and\s+events?|'
        r'procedures?\s+and\s+assessments?)\b',
        re.IGNORECASE
    )

    by_src_page = {(c["source"], c["page"]): c for c in pool}
    seen  = {(c["source"], c["page"]) for c in retrieved}
    extra = []
    _MAX_EXTRA = 10  # never add more than 10 pages via expansion

    def _add_window(src, center_page, before, after):
        for offset in range(-before, after + 1):
            if len(extra) >= _MAX_EXTRA:
                return
            if offset == 0:
                continue
            key = (src, center_page + offset)
            if key not in by_src_page or key in seen:
                continue
            extra.append(by_src_page[key])
            seen.add(key)

    for chunk in retrieved:
        src, page = chunk["source"], chunk["page"]
        text = chunk["text"]

        # Explicit table reference → look ±pages (table may be before or after the text)
        # Note: always expand even if the current chunk already has some table data
        if TABLE_REF.search(text):
            _add_window(src, page, before=2, after=8)

        # Schedule section heading: table is usually 1-5 pages after
        if SCHEDULE_KW.search(text):
            _add_window(src, page, before=1, after=6)

    # Scan entire pool for x-grid pages (assessment schedule columns of x markers)
    X_GRID = re.compile(r'(?:^|\s)[xX](?:[\s\t]+[xX]){2,}', re.MULTILINE)
    for c in pool:
        key = (c["source"], c["page"])
        if key not in seen and X_GRID.search(c.get("text", "")):
            extra.append(c)
            seen.add(key)

    return retrieved + extra


_STOP_WORDS = {
    "the","a","an","is","in","on","at","to","for","of","and","or","from",
    "with","by","as","be","are","was","were","this","that","it","its",
    "have","has","not","but","what","which","who","when","where","how",
    "give","show","me","get","find","provide","tell","list","all","only",
}

def retrieve(query: str, chunks, embeddings, top_k=5):
    if not chunks:
        return []

    # Narrow to the document named in the query (e.g. "from protocol", "from DRP")
    pool, pool_idx = _doc_filter(query, chunks)

    # Meaningful query words only (strip stop words + short tokens)
    q_words = {w for w in query.lower().split()
               if w not in _STOP_WORDS and len(w) > 2}
    if not q_words:                          # fallback if all words stripped
        q_words = set(query.lower().split())

    # Keyword pre-score on the pool
    kw_scores = []
    for local_i, c in enumerate(pool):
        t = c["text"].lower()
        score = sum(t.count(w) for w in q_words)
        kw_scores.append((score, local_i))
    kw_scores.sort(key=lambda x: -x[0])

    if embeddings is None or not EMBEDDING_OK:
        result = [pool[i] for s, i in kw_scores[:top_k] if s > 0]
        return result or pool[:top_k]

    import numpy as np

    # Candidate selection:
    # - If pool is small (single doc after filter) → search ALL chunks semantically
    # - If pool is large (all docs) → keyword pre-filter top-50 then semantic
    if len(pool) <= 60:
        candidate_local = list(range(len(pool)))
    else:
        candidate_local = [i for _, i in kw_scores[:50]] or list(range(min(50, len(pool))))

    candidate_global = [pool_idx[i] for i in candidate_local]

    # Cache query embedding
    if "q_emb_cache" not in st.session_state:
        st.session_state.q_emb_cache = {}
    if query not in st.session_state.q_emb_cache:
        embedder = get_embedder()
        st.session_state.q_emb_cache[query] = embedder.encode(
            [query], show_progress_bar=False, convert_to_numpy=True
        )
    q_emb = st.session_state.q_emb_cache[query]

    candidate_embs = embeddings[candidate_global]
    scores = np.dot(candidate_embs, q_emb.T).flatten()
    top_local = scores.argsort()[::-1][:top_k]

    result = [pool[candidate_local[i]] for i in top_local]
    result = result or pool[:top_k]

    # Table-reference expansion: only for schedule/table queries
    _TABLE_Q_INNER = re.compile(
        r'\b(assessment\s+schedule|schedule\s+of\s+assessments?|'
        r'visit\s+schedule|time\s+and\s+events?|'
        r'procedures?\s+and\s+assessments?)\b',
        re.IGNORECASE
    )
    if _TABLE_Q_INNER.search(query):
        result = _expand_table_refs(result, pool)

    # ── Targeted schedule/table search ──────────────────────────────────────
    # Only triggered when the query explicitly asks for a schedule or table.
    # KEY CHANGE: anchor uses schedule-specific keywords ONLY — NOT generic
    # "Table X.X" references (those appear on every page of a protocol and
    # previously caused the entire document to be returned).
    TABLE_Q = re.compile(
        r'\b(assessment\s+schedule|schedule\s+of\s+assessments?|'
        r'visit\s+schedule|time\s+and\s+events?|'
        r'procedures?\s+and\s+assessments?)\b',
        re.IGNORECASE
    )
    if TABLE_Q.search(query):
        by_src_page = {(c["source"], c["page"]): c for c in pool}
        seen_keys   = {(c["source"], c["page"]) for c in result}

        # Anchor: pages where "Schedule of Assessments" appears as a HEADING
        # (i.e. the phrase is prominent, not buried mid-paragraph)
        SCHED_HEADING = re.compile(
            r'\b(schedule\s+of\s+assessments?|assessment\s+schedule|'
            r'time\s+and\s+events?\s+table|visit\s+schedule)\b',
            re.IGNORECASE
        )
        anchor_pages = sorted(
            {(c["source"], c["page"]) for c in pool
             if SCHED_HEADING.search(c.get("text", ""))},
            key=lambda x: x[1]   # ascending page order
        )

        # Take only the first 2 anchors and add pages forward — enough for multi-page tables.
        # Skip TOC-only mentions: prefer anchors where the heading is on a page that also
        # has table data (extracted tables or x-grid markers).
        X_GRID = re.compile(r'(?:^|\s)[xX](?:[\s\t]+[xX]){2,}', re.MULTILINE)
        def _anchor_score(src_page):
            c = by_src_page.get(src_page)
            if not c:
                return 0
            has_table = 1 if c.get("tables") else 0
            has_xgrid = 1 if X_GRID.search(c.get("text", "")) else 0
            return has_table + has_xgrid

        anchor_pages = sorted(anchor_pages, key=_anchor_score, reverse=True)
        for src, page in anchor_pages[:2]:
            for offset in range(-1, 9):
                key = (src, page + offset)
                if key in by_src_page and key not in seen_keys:
                    result.append(by_src_page[key])
                    seen_keys.add(key)

    # ── Final trim: never send more than 12 chunks to the LLM ───────────────
    # Prioritise: pages with tables > pages matching schedule keywords > rest
    if len(result) > 12:
        SCHED_KW = re.compile(
            r'\b(schedule|assessment|visit|procedure|endpoint)\b', re.IGNORECASE
        )
        def _priority(c):
            has_table   = 1 if c.get("tables") else 0
            has_kw      = 1 if SCHED_KW.search(c.get("text", "")) else 0
            return (has_table * 2 + has_kw, c["page"])

        if TABLE_Q.search(query):
            result = sorted(result, key=_priority, reverse=True)[:12]
        else:
            result = result[:12]

    return result


def build_context(relevant_chunks):
    parts = []
    for c in relevant_chunks:
        part = f"[Source: {c['source']}, Page: {c['page']}]\n{c['text']}"
        if c.get("tables"):
            for t in c["tables"]:
                if t and len(t) >= 1:
                    # Proper markdown table: header | sep | rows
                    cols = len(t[0])
                    header  = "| " + " | ".join(str(x) for x in t[0]) + " |"
                    sep     = "| " + " | ".join("---" for _ in range(cols)) + " |"
                    rows    = "\n".join(
                        "| " + " | ".join(str(x) for x in r) + " |"
                        for r in t[1:]
                    )
                    part += f"\n\n[TABLE]\n{header}\n{sep}\n{rows}\n[/TABLE]"
        parts.append(part)
    return "\n\n---\n\n".join(parts)


def ask_llm(query: str, context: str, vision_images: list = None, table_query: bool = False) -> str:
    """
    vision_images: optional list of (b64, src, page) for relevant non-table images.
    table_query:   True when the user is asking for a schedule/table — triggers a
                   strict "table only, no surrounding text" system prompt.
    """
    if not ANTHROPIC_OK:
        return f"(Anthropic SDK not installed)\n\nRelevant content found:\n\n{context[:2000]}"
    api_key = st.session_state.get("anthropic_api_key", "") or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "⚠️ Please enter your Anthropic API key in the sidebar to enable AI answers."
    client = anthropic.Anthropic(api_key=api_key)

    if table_query:
        system = (
            "You are a precise table extraction assistant.\n\n"
            "DOCUMENT RULES:\n"
            "- Each context block is labelled [Source: filename, Page: N].\n"
            "- If the user names a specific document, use ONLY chunks from that document.\n"
            "- NEVER mix data from different documents.\n\n"
            "YOUR ONLY JOB FOR THIS REQUEST:\n"
            f"- The user asked: \"{query}\"\n"
            "- Identify the ONE table whose title or heading best matches the user's request.\n"
            "- DO NOT return tables whose headings do not match — e.g. if the user asks for the "
            "  'assessment schedule', do NOT return eligibility criteria tables, endpoint tables, "
            "  or any other table.\n"
            "- Reproduce that matched table as a COMPLETE markdown table — every column header, "
            "  every row, every cell. Do not skip any rows.\n"
            "- If the matching table spans multiple context blocks, merge them into one table.\n"
            "- If an image is provided and its heading matches the request, extract it as markdown.\n\n"
            "OUTPUT FORMAT — strictly:\n"
            "**[Exact table title from document]**\n"
            "<complete markdown table>\n"
            "[Source: filename, Page: N]\n\n"
            "FORBIDDEN:\n"
            "- Do NOT include any introductory sentences, explanations, footnotes, or surrounding text.\n"
            "- Do NOT return unrelated tables.\n"
            "- Do NOT summarise or abbreviate any rows.\n"
            "- Do NOT output anything except the heading, the markdown table, and the source citation."
        )
        instruction = (
            f"Return ONLY the table whose heading matches: \"{query}\". "
            "No other tables. No surrounding text."
        )
    else:
        system = (
            "You are a precise document extraction assistant. Return exact content — never paraphrase.\n\n"
            "DOCUMENT RULES (most important):\n"
            "- Each context block is labelled [Source: filename, Page: N].\n"
            "- If the user names a specific document (e.g. 'from protocol', 'from DRP'), use ONLY "
            "  chunks whose Source matches that document. Ignore all other sources completely.\n"
            "- If the requested information is not found in the specified document, say exactly: "
            "  'This information is not available in [document name].'\n"
            "- NEVER pull information from a different document to fill gaps.\n\n"
            "TOPIC FOCUS:\n"
            "- Answer ONLY the specific topic asked. Do NOT reproduce surrounding paragraphs, "
            "  unrelated sections, or the full document text.\n"
            "- Extract the minimum content that directly answers the question.\n"
            "- If the user names multiple documents, extract the topic from each separately.\n\n"
            "ANSWER LENGTH RULES:\n"
            "- For factual questions (dosage, date, name, number, eligibility criterion, etc.): "
            "  answer in 1-5 sentences. Quote the exact text from the document, nothing more.\n"
            "- NEVER dump entire sections or chapters. If the relevant answer is one sentence, "
            "  return one sentence — not the surrounding page.\n\n"
            "TABLE RULES:\n"
            "- Every [TABLE]...[/TABLE] block → reproduce as a complete markdown table, every row.\n"
            "- Columnar plain text → reconstruct as markdown table.\n"
            "- If images are provided, read them; if they contain tables extract as markdown table.\n\n"
            "FORMAT:\n"
            "1. Bold heading matching the topic.\n"
            "2. Exact content (concise for facts, complete for tables).\n"
            "3. [Source: filename, Page: N]"
        )
        instruction = (
            "Extract ONLY the content about the specific topic asked, "
            "from the correct source document only. "
            "Reproduce tables in full as markdown tables."
        )

    # Build message content — include vision images so Claude can read them
    user_content: list = []
    if vision_images:
        for b64, src, page in vision_images[:6]:
            user_content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": _get_media_type(b64), "data": b64},
            })
    user_content.append({
        "type": "text",
        "text": (
            f"Documents:\n{context}\n\n"
            f"User question: {query}\n\n"
            f"Instruction: {instruction}"
        ),
    })
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    return msg.content[0].text


def table_to_html(rows):
    if not rows:
        return ""
    html = "<table>"
    for i, row in enumerate(rows):
        html += "<tr>"
        tag = "th" if i == 0 else "td"
        for cell in row:
            html += f"<{tag}>{cell}</{tag}>"
        html += "</tr>"
    html += "</table>"
    return html




def render_answer(answer: str, relevant_chunks):
    """Strip markdown tables from bubble text; collect ALL tables as dataframes."""
    lines = answer.split("\n")
    non_table_lines: list = []
    _tbl_buf: list = []        # accumulates rows of the current markdown table
    md_tables: list = []       # parsed tables from LLM markdown output

    for line in lines:
        stripped = line.strip()
        is_data_row = bool(re.match(r"^\|.+\|$", stripped)) and not re.match(r"^\|[\s\-|:]+\|$", stripped)
        is_sep_row  = bool(re.match(r"^\|[\s\-|:]+\|$", stripped))
        if is_data_row:
            _tbl_buf.append(stripped)
        elif is_sep_row:
            pass  # skip separator, keep buffer open
        else:
            if _tbl_buf:
                rows = [[c.strip() for c in tl.strip("|").split("|")] for tl in _tbl_buf]
                if len(rows) >= 2:
                    md_tables.append(rows)
                _tbl_buf = []
            non_table_lines.append(line)
    if _tbl_buf:
        rows = [[c.strip() for c in tl.strip("|").split("|")] for tl in _tbl_buf]
        if len(rows) >= 2:
            md_tables.append(rows)

    # Collapse consecutive blank lines
    cleaned: list[str] = []
    prev_blank = False
    for line in non_table_lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        cleaned.append(line)
        prev_blank = is_blank
    answer_html = "<br>".join(cleaned).strip()

    # Images — deduplicate; logos appear on every page so skip them
    from collections import Counter
    _img_count: Counter = Counter()
    _img_first: dict = {}
    for c in relevant_chunks:
        for img_b64 in c.get("images", []):
            _img_count[img_b64] += 1
            if img_b64 not in _img_first:
                _img_first[img_b64] = (img_b64, c["source"], c["page"])
    images = [info for b64, info in _img_first.items() if _img_count[b64] == 1]

    # Tables: chunk-extracted (structured) first, then LLM-generated markdown tables
    seen = set()
    extra_tables = []
    for c in relevant_chunks:
        for t in c.get("tables", []):
            key = (c["source"], c["page"])
            if key not in seen:
                seen.add(key)
                extra_tables.append((t, c["source"], c["page"]))
    # Add LLM markdown tables that have no corresponding chunk-extracted table
    # (this happens when find_tables() failed but LLM reconstructed from plain text)
    for rows in md_tables:
        extra_tables.append((rows, "protocol", 0))

    return answer_html, images, extra_tables


def _md_table_to_html(lines):
    if not lines:
        return ""
    # Filter separator lines (---|---|---)
    rows = [l for l in lines if not re.match(r"^\|[\s\-|:]+\|$", l)]
    html = "<table>"
    for i, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        html += "<tr>"
        tag = "th" if i == 0 else "td"
        for c in cells:
            html += f"<{tag}>{c}</{tag}>"
        html += "</tr>"
    html += "</table>"
    return html


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>📚 StudyGuide</h1>
        <p>Document Intelligence Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Upload Documents")
    uploaded_files = st.file_uploader(
        "Drop files here",
        type=["pdf", "docx", "txt", "md", "csv", "xlsx", "xls"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    # Folder path only works when running locally (not on Streamlit Cloud)
    _is_cloud = os.environ.get("STREAMLIT_SERVER_HEADLESS", "").lower() in ("1", "true")
    if _is_cloud:
        folder_path = ""
        st.markdown(
            '<div style="font-size:.75rem;color:var(--text-muted);padding:6px 10px;'
            'background:var(--surface2);border:1px solid var(--border);border-radius:8px;'
            'margin-top:4px;">📁 Folder path loading is only available when running locally.</div>',
            unsafe_allow_html=True,
        )
    else:
        folder_path = st.text_input(
            "Or enter a folder path",
            placeholder="C:/path/to/your/documents",
        )

    col1, col2 = st.columns(2)
    with col1:
        load_btn = st.button("⚡ Load", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑 Clear", use_container_width=True)

    if clear_btn:
        st.session_state.doc_chunks = []
        st.session_state.embeddings = None
        st.session_state.loaded_files = []
        st.session_state.messages = []
        st.rerun()

    if load_btn:
        import concurrent.futures

        EXTS = {".pdf", ".docx", ".txt", ".md", ".csv", ".xlsx", ".xls"}

        # Collect all files to process (uploaded + folder), skip already-loaded
        tasks = []  # list of (name, bytes)

        if uploaded_files:
            for f in uploaded_files:
                if f.name not in st.session_state.loaded_files:
                    tasks.append((f.name, f.read()))

        if folder_path and Path(folder_path).is_dir():
            for fp in Path(folder_path).rglob("*"):
                if fp.suffix.lower() in EXTS and fp.name not in st.session_state.loaded_files:
                    try:
                        tasks.append((fp.name, fp.read_bytes()))
                    except Exception:
                        pass

        if not tasks and not uploaded_files and not folder_path:
            st.warning("Please upload files or enter a folder path.")
        elif tasks:
            def _parse(name_bytes):
                name, data = name_bytes
                class _F:
                    def __init__(self): self.name = name
                    def read(self): return data
                try:
                    return name, load_file(_F())
                except Exception:
                    return name, []

            new_chunks = []
            with st.spinner(f"Reading {len(tasks)} file(s)…"):
                # Parallel parse — I/O already done above, this parallelises CPU parsing
                with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(tasks))) as ex:
                    for name, chunks in ex.map(_parse, tasks):
                        new_chunks.extend(chunks)
                        st.session_state.loaded_files.append(name)

            if new_chunks:
                st.session_state.doc_chunks.extend(new_chunks)
                # Only embed the NEW chunks, then concatenate with existing embeddings
                with st.spinner(f"Indexing {len(new_chunks)} chunks…"):
                    new_embs = embed_chunks(new_chunks)
                    if new_embs is not None:
                        import numpy as np
                        if st.session_state.embeddings is not None:
                            st.session_state.embeddings = np.vstack(
                                [st.session_state.embeddings, new_embs]
                            )
                        else:
                            st.session_state.embeddings = new_embs
                st.success(f"Loaded {len(new_chunks)} chunks from {len(tasks)} file(s)!")

    st.markdown("---")

    # Stats
    n_files = len(set(c["source"] for c in st.session_state.doc_chunks)) if st.session_state.doc_chunks else 0
    n_chunks = len(st.session_state.doc_chunks)
    n_imgs = sum(len(c["images"]) for c in st.session_state.doc_chunks)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="num">{n_files}</div><div class="lbl">Files</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="num">{n_chunks}</div><div class="lbl">Chunks</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="stat-card"><div class="num">{n_imgs}</div><div class="lbl">Images Indexed</div></div>', unsafe_allow_html=True)

    if st.session_state.loaded_files:
        st.markdown("---")
        st.markdown(
            '<p style="font-size:.85rem;font-weight:700;color:#f0eeff;'
            'margin:0 0 8px;letter-spacing:.04em;text-transform:uppercase;">Loaded Files</p>',
            unsafe_allow_html=True,
        )
        icons = {"pdf":"📄","docx":"📝","txt":"📃","md":"📋","csv":"📊","xlsx":"📗","xls":"📗"}
        for fname in st.session_state.loaded_files:
            ext = Path(fname).suffix.lower().lstrip(".")
            icon = icons.get(ext, "📁")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:6px;'
                f'padding:5px 8px;margin-bottom:4px;border-radius:6px;'
                f'background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);">'
                f'<span style="font-size:.9rem;">{icon}</span>'
                f'<span style="font-size:.78rem;color:#c8c5ff;word-break:break-all;">{fname}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown('<span style="font-size:.75rem;color:var(--text-muted);letter-spacing:.04em;text-transform:uppercase;">API Key</span>', unsafe_allow_html=True)
    api_key_input = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-…",
        label_visibility="collapsed",
        value=st.session_state.get("anthropic_api_key", os.environ.get("ANTHROPIC_API_KEY", "")),
    )
    if api_key_input:
        st.session_state["anthropic_api_key"] = api_key_input

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h2>Ask Your Documents</h2>
    <p>Exact answers · Tables preserved · Images displayed</p>
</div>
""", unsafe_allow_html=True)

# Welcome state
if not st.session_state.doc_chunks:
    st.markdown("""
    <div style="text-align:center; padding:4rem 2rem; color:var(--text-muted);">
        <div style="font-size:4rem; margin-bottom:1rem;">📂</div>
        <div style="font-size:1.1rem; font-family:'Playfair Display',serif; color:var(--text); margin-bottom:.5rem;">
            No documents loaded yet
        </div>
        <div style="font-size:.85rem;">Upload files in the sidebar to get started.</div>
        <br>
        <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap; margin-top:1rem;">
            <span style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:.78rem;">📄 PDF</span>
            <span style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:.78rem;">📝 DOCX</span>
            <span style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:.78rem;">📃 TXT / MD</span>
            <span style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:.78rem;">📊 CSV</span>
            <span style="background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:.78rem;">📗 XLSX / XLS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Chat history
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-user"><div class="bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            answer_html = msg.get("answer_html", msg["content"])
            images = msg.get("images", [])
            tables = msg.get("tables", [])

            st.markdown(f"""
            <div class="msg-bot">
                <div class="avatar">🤖</div>
                <div class="bubble">
                    {answer_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Inline images
            if images:
                cols = st.columns(min(len(images), 3))
                for i, (b64, src, page) in enumerate(images):
                    with cols[i % 3]:
                        st.image(
                            base64.b64decode(b64),
                            caption=f"{src} – p.{page}",
                            use_container_width=True,
                        )

            # Extra tables — plain Streamlit dataframe
            for (t, src, page) in tables:
                if t and len(t) > 1:
                    try:
                        import pandas as pd
                        df = pd.DataFrame(t[1:], columns=[str(c) for c in t[0]])
                        st.dataframe(df, use_container_width=True)
                    except Exception:
                        st.markdown(table_to_html(t), unsafe_allow_html=True)

    # Thinking indicator + Stop button — shown while query is pending
    thinking_slot = st.empty()
    if st.session_state.get("_pending_query"):
        thinking_slot.markdown("""
        <div class="msg-bot">
            <div class="avatar">🤖</div>
            <div class="bubble" style="padding:14px 20px;">
                <span class="thinking-dots">
                    <span></span><span></span><span></span>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-scroll
    st.markdown("""
    <script>
    (function() {
        function scrollToBottom() {
            var chatWrap = document.querySelector('.chat-wrap');
            if (chatWrap) chatWrap.scrollIntoView({ behavior: 'smooth', block: 'end' });
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }
        setTimeout(scrollToBottom, 150);
    })();
    </script>
    """, unsafe_allow_html=True)

    # ── Input row: Send form OR Stop button ─────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.get("_pending_query"):
        # While processing: show Stop button instead of the Send form.
        # Inject CSS here (not in global block) so it only targets the one button
        # visible at this moment — the send form is hidden, so no false matches.
        st.markdown("""
        <style>
        .stop-row { display:flex; align-items:center; gap:12px; padding:8px 0; }
        .stop-hint { font-size:.8rem; color:#9090b8; font-family:'Inter',sans-serif; }
        /* Valid selector: data-testid is the real attribute Streamlit sets on buttons */
        button[data-testid="baseButton-secondary"] {
            background: rgba(220,50,50,.22) !important;
            border: 1.5px solid #ff5555 !important;
            color: #ff7070 !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: .88rem !important;
            padding: 7px 22px !important;
            min-width: 110px !important;
            transition: background .2s, box-shadow .2s !important;
        }
        button[data-testid="baseButton-secondary"]:hover {
            background: rgba(220,50,50,.40) !important;
            box-shadow: 0 0 12px rgba(220,50,50,.45) !important;
        }
        </style>
        <div class="stop-row">
            <span class="stop-hint">⏳ Searching documents…</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⏹ Stop", key="stop_btn", use_container_width=False,
                     help="Cancel this query"):
            st.session_state.pop("_pending_query", None)
            st.session_state.pop("_processing", None)
            st.toast("Query cancelled.", icon="🛑")
            st.rerun()
    else:
        with st.form(key="query_form", clear_on_submit=True):
            col_in, col_btn = st.columns([5, 1])
            with col_in:
                query = st.text_input(
                    "Ask a question",
                    placeholder="What does the document say about…?",
                    label_visibility="collapsed",
                )
            with col_btn:
                submit = st.form_submit_button("Send ➤", use_container_width=True)

        # Step 1 — user hits Send: show message immediately, queue the query
        if submit and query.strip():
            st.session_state.messages.append({"role": "user", "content": query.strip()})
            st.session_state["_pending_query"] = query.strip()
            st.rerun()

    # Process pending query (only runs when _pending_query is still set after the
    # Stop button check above — i.e., user did not click Stop on this rerun)
    if st.session_state.get("_pending_query"):
        from collections import Counter
        pending = st.session_state.pop("_pending_query")
        _is_table_q = bool(re.search(
            r'\b(assessment\s+schedule|schedule\s+of\s+assessments?|'
            r'visit\s+schedule|time\s+and\s+events?|'
            r'procedures?\s+and\s+assessments?)\b',
            pending, re.IGNORECASE
        ))
        relevant = retrieve(pending, st.session_state.doc_chunks, st.session_state.embeddings,
                            top_k=8 if _is_table_q else 5)

        # ── Hard document filter ──────────────────────────────────────────────
        # Re-run _doc_filter to find which documents the query refers to.
        # If specific documents were identified, remove any chunks from other docs
        # that may have crept in via table expansion or semantic search.
        _filter_pool, _ = _doc_filter(pending, st.session_state.doc_chunks)
        _matched_srcs = {c["source"] for c in _filter_pool}
        _all_srcs     = {c["source"] for c in st.session_state.doc_chunks}
        if _matched_srcs != _all_srcs:
            # A specific document was identified → enforce strictly
            relevant = [c for c in relevant if c["source"] in _matched_srcs]
            if not relevant:
                relevant = _filter_pool[:8]  # fallback if over-filtered

        context = build_context(relevant)

        # ── Image classification (table / relevant / irrelevant) ─────────────
        api_key = st.session_state.get("anthropic_api_key", "") or os.environ.get("ANTHROPIC_API_KEY", "")

        # Deduplicate: images appearing on multiple pages are logos → discard
        _img_cnt: Counter = Counter()
        for c in relevant:
            for b64 in c.get("images", []):
                _img_cnt[b64] += 1
        _uniq_imgs: list = []
        _seen_b64: set = set()
        for c in relevant:
            for b64 in c.get("images", []):
                if _img_cnt[b64] == 1 and b64 not in _seen_b64:
                    _uniq_imgs.append((b64, c["source"], c["page"]))
                    _seen_b64.add(b64)

        display_images: list = []   # relevant non-table images → shown to user
        vision_images:  list = []   # same, passed to LLM for reading
        img_tables:     list = []   # table images → shown as dataframes

        if api_key and ANTHROPIC_OK and _uniq_imgs:
            with st.spinner("Analysing images…"):
                for b64, src, page in _uniq_imgs[:10]:
                    kind, rows = analyze_image(b64, pending, api_key)
                    if kind == "table" and rows:
                        img_tables.append((rows, src, page))
                        # Append image-extracted table to text context
                        cols = len(rows[0])
                        hdr    = "| " + " | ".join(str(x) for x in rows[0]) + " |"
                        sep_ln = "| " + " | ".join("---" for _ in range(cols)) + " |"
                        body   = "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows[1:])
                        context += (f"\n\n---\n\n[Image Table from {src}, Page {page}]"
                                    f"\n[TABLE]\n{hdr}\n{sep_ln}\n{body}\n[/TABLE]")
                    elif kind == "relevant":
                        display_images.append((b64, src, page))
                        vision_images.append((b64, src, page))
                    # irrelevant → silently dropped
        else:
            display_images = _uniq_imgs   # no API key: show all unique images as fallback

        # Pass relevant images to LLM so it can read diagrams / figures
        raw_answer = ask_llm(pending, context, vision_images=vision_images, table_query=_is_table_q)
        thinking_slot.empty()
        answer_html, _, extra_tables = render_answer(raw_answer, relevant)

        sources = list({f"{c['source']} p.{c['page']}" for c in relevant})
        st.session_state.messages.append({
            "role": "assistant",
            "content": raw_answer,
            "answer_html": answer_html,
            "images": display_images,
            "tables": extra_tables + img_tables,
            "sources": sources,
        })
        st.rerun()

