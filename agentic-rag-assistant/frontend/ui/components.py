import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components
FRONTEND_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CSS_PATH = FRONTEND_DIR / "assets" / "style.css"


def load_css(css_path: Path = DEFAULT_CSS_PATH) -> None:
    css_file = Path(css_path)
    if css_file.exists():
        with open(css_file, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Stylesheet not found at {css_file}")


def render_navbar(active_page: str) -> None:
    pages = {"About the Project": "Home", "Live Demo": "Demo"}

    links_html = "".join(
        f'<a class="nav-link {"active" if page_key == active_page else ""}" '
        f'href="?page={page_key}" target="_self">{label}</a>'
        for page_key, label in pages.items()
    )

    navbar_html = (
        '<div class="navbar">'
        '<div class="navbar-brand">Agentic RAG Assistant</div>'
        '<div class="navbar-links">'
        + links_html +
        '</div>'
        '</div>'
    )
    st.markdown(navbar_html, unsafe_allow_html=True)


def render_workflow_diagram() -> None:
    components.html("""
    <svg width="340" height="520" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, sans-serif">
        <rect x="95" y="10" width="150" height="36" rx="18" fill="#1A1D23"/>
        <text x="170" y="33" text-anchor="middle" fill="white" font-size="13" font-weight="600">START</text>
        <line x1="170" y1="46" x2="170" y2="70" stroke="#54585f" stroke-width="2"/>
        <polygon points="165,68 175,68 170,76" fill="#54585f"/>
        <rect x="70" y="76" width="200" height="38" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="170" y="100" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Question Classifier</text>
        <line x1="170" y1="114" x2="170" y2="128" stroke="#54585f" stroke-width="2"/>
        <line x1="80" y1="128" x2="260" y2="128" stroke="#54585f" stroke-width="2"/>
        <line x1="80" y1="128" x2="80" y2="148" stroke="#54585f" stroke-width="2"/>
        <line x1="260" y1="128" x2="260" y2="148" stroke="#54585f" stroke-width="2"/>
        <text x="80" y="164" text-anchor="middle" fill="#444" font-size="10" font-weight="700">SIMPLE PATH</text>
        <text x="260" y="164" text-anchor="middle" fill="#444" font-size="10" font-weight="700">COMPLEX PATH</text>
        <rect x="18" y="170" width="124" height="36" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="80" y="193" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Retriever</text>
        <rect x="198" y="170" width="124" height="36" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="260" y="193" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Planner Agent</text>
        <line x1="260" y1="206" x2="260" y2="220" stroke="#54585f" stroke-width="2"/>
        <polygon points="255,218 265,218 260,226" fill="#54585f"/>
        <rect x="198" y="226" width="124" height="36" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="260" y="249" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Retriever</text>
        <line x1="80" y1="206" x2="80" y2="282" stroke="#54585f" stroke-width="2"/>
        <line x1="260" y1="262" x2="260" y2="282" stroke="#54585f" stroke-width="2"/>
        <line x1="80" y1="282" x2="260" y2="282" stroke="#54585f" stroke-width="2"/>
        <line x1="170" y1="282" x2="170" y2="296" stroke="#54585f" stroke-width="2"/>
        <polygon points="165,294 175,294 170,302" fill="#54585f"/>
        <rect x="60" y="302" width="220" height="38" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="170" y="326" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Verification Agent</text>
        <line x1="170" y1="340" x2="170" y2="364" stroke="#54585f" stroke-width="2"/>
        <polygon points="165,362 175,362 170,370" fill="#54585f"/>
        <rect x="60" y="370" width="220" height="38" rx="8" fill="white" stroke="#54585f" stroke-width="1.5"/>
        <text x="170" y="394" text-anchor="middle" fill="#1A1D23" font-size="12" font-weight="600">Answer Generator</text>
        <line x1="170" y1="408" x2="170" y2="432" stroke="#54585f" stroke-width="2"/>
        <polygon points="165,430 175,430 170,438" fill="#54585f"/>
        <rect x="95" y="438" width="150" height="36" rx="18" fill="#1A1D23"/>
        <text x="170" y="461" text-anchor="middle" fill="white" font-size="13" font-weight="600">END</text>
    </svg>
    """, height=530)