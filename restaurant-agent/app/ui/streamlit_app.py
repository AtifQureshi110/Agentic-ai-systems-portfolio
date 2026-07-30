# """
# Restaurant Agent — Streamlit frontend entrypoint.

# Handles top-level page routing (About / Demo) via URL query params and
# renders the sticky navigation bar. Page content lives in dedicated
# render functions so new pages can be added without touching the nav.
# """

# import streamlit as st
# import streamlit.components.v1 as components
# from pathlib import Path
# import textwrap
# import uuid
# import requests

# BACKEND_URL = "http://localhost:8000/chat"

# # ---------------------------------------------------------------------
# # Page config — must be the first Streamlit call
# # ---------------------------------------------------------------------
# st.set_page_config(
#     page_title="Restaurant Assistant",
#     page_icon="🍴",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ---------------------------------------------------------------------
# # Load external CSS
# # ---------------------------------------------------------------------
# def load_css(file_name: str) -> None:
#     css_path = Path(__file__).parent / file_name
#     if css_path.exists():
#         st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# load_css("styles.css")

# # ---------------------------------------------------------------------
# # Routing — read current page from the URL query params
# # ---------------------------------------------------------------------
# PAGES = ["about", "demo"]
# current_page = st.query_params.get("page", "about")
# if current_page not in PAGES:
#     current_page = "about"

# # ---------------------------------------------------------------------
# # Sticky navbar
# # ---------------------------------------------------------------------
# def render_navbar(active: str) -> None:
#     def link(page_key: str, label: str) -> str:
#         active_class = "nav-link active" if page_key == active else "nav-link"
#         return f'<a class="{active_class}" href="?page={page_key}" target="_self">{label}</a>'

#     navbar_html = textwrap.dedent(f"""
#     <div class="navbar">
#         <div class="navbar-inner">
#             <div class="brand">
#                 <span class="brand-mark">RA</span>
#                 <span class="brand-name">Restaurant<span class="brand-accent">Assistant</span></span>
#             </div>
#             <nav class="nav-links">
#                 {link("about", "About")}
#                 {link("demo", "Live Demo")}
#             </nav>
#         </div>
#     </div>
#     """)
#     st.markdown(navbar_html, unsafe_allow_html=True)

# render_navbar(current_page)

# # ---------------------------------------------------------------------
# # Architecture diagram — hand-drawn SVG, rendered via components.html
# # so it can carry its own <style>/markup and isn't dependent on an
# # external image asset. Colors are hardcoded to match styles.css since
# # components.html renders in an isolated iframe (no access to the
# # page's CSS variables).
# # ---------------------------------------------------------------------
# def render_architecture_diagram() -> None:
#     diagram_svg = """
#     <style>
#         html, body {
#             margin: 0;
#             padding: 0;
#             background: #123832;
#         }
#     </style>
#     <div style="max-width:900px; margin:0 auto; padding:0 2rem; box-sizing:border-box; background:#123832;">
#     <svg viewBox="0 0 820 700" xmlns="http://www.w3.org/2000/svg"
#          font-family="Manrope, -apple-system, sans-serif" width="100%" height="auto">

#         <defs>
#             <marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5"
#                     markerWidth="7" markerHeight="7" orient="auto">
#                 <path d="M 0 0 L 10 5 L 0 10 z" fill="#A9C2B7"/>
#             </marker>
#         </defs>

#         <rect x="0" y="0" width="820" height="700" rx="18" fill="#17423B" stroke="rgba(227,168,87,0.18)"/>

#         <rect x="335" y="24" width="150" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
#         <text x="410" y="50" text-anchor="middle" fill="#F3ECDD" font-size="14" font-weight="700">User</text>

#         <rect x="300" y="94" width="220" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
#         <text x="410" y="120" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="600">Streamlit chat UI</text>

#         <rect x="300" y="164" width="220" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
#         <text x="410" y="190" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">FastAPI backend</text>

#         <rect x="260" y="234" width="300" height="64" rx="12" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
#         <text x="410" y="262" text-anchor="middle" fill="#F3ECDD" font-size="14" font-weight="700">LangGraph agent core</text>
#         <text x="410" y="282" text-anchor="middle" fill="#A9C2B7" font-size="11">LangChain + Gemini + memory</text>

#         <line x1="410" y1="66" x2="410" y2="92" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="410" y1="136" x2="410" y2="162" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="410" y1="206" x2="410" y2="232" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

#         <path d="M 560 250 H 780 V 45 H 492" fill="none" stroke="#A9C2B7" stroke-width="1.5"
#               stroke-dasharray="5,4" marker-end="url(#arrow)"/>
#         <text x="700" y="150" text-anchor="middle" fill="#A9C2B7" font-size="11" font-style="italic">response</text>

#         <line x1="410" y1="298" x2="150" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="410" y1="298" x2="410" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="410" y1="298" x2="670" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

#         <rect x="30" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
#         <text x="150" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Structured data tools</text>

#         <rect x="50" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="150" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">Menu tool</text>

#         <rect x="50" y="424" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="150" y="445" text-anchor="middle" fill="#F3ECDD" font-size="12">Reservation tool</text>

#         <rect x="50" y="468" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="150" y="489" text-anchor="middle" fill="#F3ECDD" font-size="12">Availability tool</text>

#         <rect x="290" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
#         <text x="410" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Retrieval tools</text>

#         <rect x="310" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="410" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">FAQ tool</text>

#         <rect x="310" y="424" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="410" y="445" text-anchor="middle" fill="#F3ECDD" font-size="12">Policy tool</text>

#         <rect x="550" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
#         <text x="670" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Contact tool</text>

#         <rect x="570" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="670" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">Contact tool</text>

#         <line x1="150" y1="540" x2="150" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="410" y1="540" x2="410" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
#         <line x1="670" y1="540" x2="670" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

#         <rect x="30" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="150" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">SQLite</text>
#         <text x="150" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">Menu, tables, reservations</text>

#         <rect x="290" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="410" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Pinecone</text>
#         <text x="410" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">FAQ &amp; policy embeddings</text>

#         <rect x="550" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
#         <text x="670" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Config file</text>
#         <text x="670" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">Address, hours, phone</text>

#     </svg>
#     </div>
#     """
#     components.html(diagram_svg, height=700, scrolling=False)

# # ---------------------------------------------------------------------
# # About page content
# # ---------------------------------------------------------------------
# def render_about_page() -> None:
#     st.markdown(
#         textwrap.dedent(
#             """
#             <div class="page-content">
#                 <div class="hero">
#                     <p class="eyebrow">Agentic AI · Restaurant Ops</p>
#                     <h1>An agent that runs the front desk,<br>so your team can run the floor.</h1>
#                     <p class="hero-sub">
#                         Restaurant Assistant answers menu questions, checks table availability,
#                         and books reservations — end to end, without a human in the loop.
#                     </p>
#                 </div>
#                 <div class="section">
#                     <h2>What it does</h2>
#                     <p class="body-text">
#                         This is an agentic AI assistant for a restaurant — it answers questions about
#                         the menu, checks table availability, makes reservations, and handles FAQs,
#                         all through natural conversation. What makes it <em>agentic</em> rather than a
#                         simple chatbot is that it uses LangGraph to reason through multi-step tasks —
#                         like realizing it needs a time before it can check availability, remembering
#                         what you already told it, and deciding on its own whether to search the menu,
#                         check the database, or answer a policy question.
#                     </p>
#                 </div>
#                 <div class="section">
#                     <h2>Architecture</h2>
#                     <p class="body-text">
#                         The request flow is fully agentic: the LangGraph core decides which tool(s)
#                         to call — structured data, retrieval, or contact info — rather than following
#                         a fixed script.
#                     </p>
#                 </div>
#             </div>
#             """
#         ),
#         unsafe_allow_html=True,
#     )

#     render_architecture_diagram()

#     st.markdown(
#         textwrap.dedent(
#             """
#             <div class="page-content">
#                 <div class="section">
#                     <h2>Try asking</h2>
#                     <div class="example-grid">
#                         <div class="example-card">"Do you have any vegetarian options?"</div>
#                         <div class="example-card">"Is a table for 4 available tonight at 8pm?"</div>
#                         <div class="example-card">"What's your cancellation policy?"</div>
#                     </div>
#                 </div>
#                 <div class="section">
#                     <h2>Built with</h2>
#                     <div class="chip-row">
#                         <span class="chip">FastAPI</span>
#                         <span class="chip">LangGraph</span>
#                         <span class="chip">LangChain</span>
#                         <span class="chip">Gemini</span>
#                         <span class="chip">Pinecone</span>
#                         <span class="chip">SQL Database</span>
#                         <span class="chip">Streamlit</span>
#                     </div>
#                 </div>
#                 <div class="section">
#                     <div class="author-card">
#                         <div class="author-name">Muhammad Atif</div>
#                         <div class="author-title">AI/ML Engineer</div>
#                         <div class="author-links">
#                             <a class="author-link" href="https://github.com/AtifQureshi110?tab=repositories" target="_blank" rel="noopener noreferrer">⬡ GitHub</a>
#                             <a class="author-link" href="https://www.youtube.com/@AICornerOfficial110" target="_blank" rel="noopener noreferrer">▶ YouTube</a>
#                             <a class="author-link" href="https://www.linkedin.com/in/matif110/" target="_blank" rel="noopener noreferrer">◈ LinkedIn</a>
#                             <a class="author-link" href="https://www.instagram.com/atif_qureshi_110/" target="_blank" rel="noopener noreferrer">◎ Instagram</a>
#                         </div>
#                     </div>
#                 </div>
#             </div>
#             """
#         ),
#         unsafe_allow_html=True,
#     )

# def render_demo_page() -> None:
#     st.markdown(
#         textwrap.dedent(
#             """
#             <div class="page-content">
#                 <div class="hero">
#                     <p class="eyebrow">Live Demo</p>
#                     <h1>Talk to the assistant.</h1>
#                     <p class="hero-sub">
#                         Ask about the menu, check table availability, or make a reservation —
#                         the agent figures out what it needs to do.
#                     </p>
#                 </div>
#             </div>
#             """
#         ),
#         unsafe_allow_html=True,
#     )

#     if "thread_id" not in st.session_state:
#         st.session_state.thread_id = str(uuid.uuid4())
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     for msg in st.session_state.chat_history:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     user_message = st.chat_input("Ask about the menu, a reservation, or anything else…")

#     if user_message:
#         st.session_state.chat_history.append({"role": "user", "content": user_message})
#         with st.chat_message("user"):
#             st.markdown(user_message)

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking…"):
#                 try:
#                     response = requests.post(
#                         BACKEND_URL,
#                         json={
#                             "message": user_message,
#                             "thread_id": st.session_state.thread_id,
#                         },
#                         timeout=60,
#                     )
#                     response.raise_for_status()
#                     reply = response.json().get("reply", "Sorry, I didn't get a reply back.")
#                 except requests.exceptions.ConnectionError:
#                     reply = (
#                         "⚠️ Can't reach the backend right now. "
#                         "Make sure the FastAPI server is running on **http://localhost:8000** "
#                         "(`uvicorn app.main:app --reload`), then try again."
#                     )
#                 except requests.exceptions.Timeout:
#                     reply = "⚠️ The backend took too long to respond. Please try again."
#                 except requests.exceptions.HTTPError:
#                     reply = f"⚠️ The backend returned an error (status {response.status_code}). Please try again."
#                 except Exception:
#                     reply = "⚠️ Something went wrong talking to the backend. Please try again."

#             st.markdown(reply)

#         st.session_state.chat_history.append({"role": "assistant", "content": reply})

# if current_page == "about":
#     render_about_page()
# else:
#     render_demo_page()


"""
Restaurant Agent — Streamlit frontend entrypoint.

Handles top-level page routing (About / Demo) via URL query params and
renders the sticky navigation bar. Page content lives in dedicated
render functions so new pages can be added without touching the nav.
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import textwrap
import uuid
import time
import requests

BACKEND_URL = "http://localhost:8000/chat"

TOOL_LABELS = {
    "menu": "🍽️ Checking the menu…",
    "faq": "📖 Looking that up…",
    "availability_check": "📅 Checking table availability…",
    "reservation_create": "✅ Booking your table…",
    "unknown": "💬 Thinking…",
}

# ---------------------------------------------------------------------
# Page config — must be the first Streamlit call
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Restaurant Assistant",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------
# Load external CSS
# ---------------------------------------------------------------------
def load_css(file_name: str) -> None:
    css_path = Path(__file__).parent / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

load_css("styles.css")

# ---------------------------------------------------------------------
# Routing — read current page from the URL query params
# ---------------------------------------------------------------------
PAGES = ["about", "demo"]
current_page = st.query_params.get("page", "about")
if current_page not in PAGES:
    current_page = "about"

# ---------------------------------------------------------------------
# Sticky navbar
# ---------------------------------------------------------------------
def render_navbar(active: str) -> None:
    def link(page_key: str, label: str) -> str:
        active_class = "nav-link active" if page_key == active else "nav-link"
        return f'<a class="{active_class}" href="?page={page_key}" target="_self">{label}</a>'

    navbar_html = textwrap.dedent(f"""
    <div class="navbar">
        <div class="navbar-inner">
            <div class="brand">
                <span class="brand-mark">RA</span>
                <span class="brand-name">Restaurant<span class="brand-accent">Assistant</span></span>
            </div>
            <nav class="nav-links">
                {link("about", "About")}
                {link("demo", "Live Demo")}
            </nav>
        </div>
    </div>
    """)
    st.markdown(navbar_html, unsafe_allow_html=True)

render_navbar(current_page)

# ---------------------------------------------------------------------
# Architecture diagram — hand-drawn SVG, rendered via components.html
# so it can carry its own <style>/markup and isn't dependent on an
# external image asset. Colors are hardcoded to match styles.css since
# components.html renders in an isolated iframe (no access to the
# page's CSS variables).
# ---------------------------------------------------------------------
def render_architecture_diagram() -> None:
    diagram_svg = """
    <style>
        html, body {
            margin: 0;
            padding: 0;
            background: #123832;
        }
    </style>
    <div style="max-width:900px; margin:0 auto; padding:0 2rem; box-sizing:border-box; background:#123832;">
    <svg viewBox="0 0 820 700" xmlns="http://www.w3.org/2000/svg"
         font-family="Manrope, -apple-system, sans-serif" width="100%" height="auto">

        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5"
                    markerWidth="7" markerHeight="7" orient="auto">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#A9C2B7"/>
            </marker>
        </defs>

        <rect x="0" y="0" width="820" height="700" rx="18" fill="#17423B" stroke="rgba(227,168,87,0.18)"/>

        <rect x="335" y="24" width="150" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
        <text x="410" y="50" text-anchor="middle" fill="#F3ECDD" font-size="14" font-weight="700">User</text>

        <rect x="300" y="94" width="220" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
        <text x="410" y="120" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="600">Streamlit chat UI</text>

        <rect x="300" y="164" width="220" height="42" rx="10" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
        <text x="410" y="190" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">FastAPI backend</text>

        <rect x="260" y="234" width="300" height="64" rx="12" fill="#1F4F46" stroke="#A9C2B7" stroke-width="1.5"/>
        <text x="410" y="262" text-anchor="middle" fill="#F3ECDD" font-size="14" font-weight="700">LangGraph agent core</text>
        <text x="410" y="282" text-anchor="middle" fill="#A9C2B7" font-size="11">LangChain + Gemini + memory</text>

        <line x1="410" y1="66" x2="410" y2="92" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="410" y1="136" x2="410" y2="162" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="410" y1="206" x2="410" y2="232" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

        <path d="M 560 250 H 780 V 45 H 492" fill="none" stroke="#A9C2B7" stroke-width="1.5"
              stroke-dasharray="5,4" marker-end="url(#arrow)"/>
        <text x="700" y="150" text-anchor="middle" fill="#A9C2B7" font-size="11" font-style="italic">response</text>

        <line x1="410" y1="298" x2="150" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="410" y1="298" x2="410" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="410" y1="298" x2="670" y2="338" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

        <rect x="30" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
        <text x="150" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Structured data tools</text>

        <rect x="50" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="150" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">Menu tool</text>

        <rect x="50" y="424" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="150" y="445" text-anchor="middle" fill="#F3ECDD" font-size="12">Reservation tool</text>

        <rect x="50" y="468" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="150" y="489" text-anchor="middle" fill="#F3ECDD" font-size="12">Availability tool</text>

        <rect x="290" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
        <text x="410" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Retrieval tools</text>

        <rect x="310" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="410" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">FAQ tool</text>

        <rect x="310" y="424" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="410" y="445" text-anchor="middle" fill="#F3ECDD" font-size="12">Policy tool</text>

        <rect x="550" y="340" width="240" height="200" rx="12" fill="none" stroke="#A9C2B7" stroke-dasharray="4,3"/>
        <text x="670" y="366" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Contact tool</text>

        <rect x="570" y="380" width="200" height="34" rx="8" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="670" y="401" text-anchor="middle" fill="#F3ECDD" font-size="12">Contact tool</text>

        <line x1="150" y1="540" x2="150" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="410" y1="540" x2="410" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>
        <line x1="670" y1="540" x2="670" y2="586" stroke="#A9C2B7" stroke-width="1.5" marker-end="url(#arrow)"/>

        <rect x="30" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="150" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">SQLite</text>
        <text x="150" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">Menu, tables, reservations</text>

        <rect x="290" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="410" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Pinecone</text>
        <text x="410" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">FAQ &amp; policy embeddings</text>

        <rect x="550" y="588" width="240" height="60" rx="10" fill="#1F4F46" stroke="#A9C2B7"/>
        <text x="670" y="612" text-anchor="middle" fill="#F3ECDD" font-size="13" font-weight="700">Config file</text>
        <text x="670" y="630" text-anchor="middle" fill="#A9C2B7" font-size="10.5">Address, hours, phone</text>

    </svg>
    </div>
    """
    components.html(diagram_svg, height=700, scrolling=False)

# ---------------------------------------------------------------------
# About page content
# ---------------------------------------------------------------------
def render_about_page() -> None:
    st.markdown(
        textwrap.dedent(
            """
            <div class="page-content">
                <div class="hero">
                    <p class="eyebrow">Agentic AI · Restaurant Ops</p>
                    <h1>An agent that runs the front desk,<br>so your team can run the floor.</h1>
                    <p class="hero-sub">
                        Restaurant Assistant answers menu questions, checks table availability,
                        and books reservations — end to end, without a human in the loop.
                    </p>
                </div>
                <div class="section">
                    <h2>What it does</h2>
                    <p class="body-text">
                        This is an agentic AI assistant for a restaurant — it answers questions about
                        the menu, checks table availability, makes reservations, and handles FAQs,
                        all through natural conversation. What makes it <em>agentic</em> rather than a
                        simple chatbot is that it uses LangGraph to reason through multi-step tasks —
                        like realizing it needs a time before it can check availability, remembering
                        what you already told it, and deciding on its own whether to search the menu,
                        check the database, or answer a policy question.
                    </p>
                </div>
                <div class="section">
                    <h2>Architecture</h2>
                    <p class="body-text">
                        The request flow is fully agentic: the LangGraph core decides which tool(s)
                        to call — structured data, retrieval, or contact info — rather than following
                        a fixed script.
                    </p>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    render_architecture_diagram()

    st.markdown(
        textwrap.dedent(
            """
            <div class="page-content">
                <div class="section">
                    <h2>Try asking</h2>
                    <div class="example-grid">
                        <div class="example-card">"Do you have any vegetarian options?"</div>
                        <div class="example-card">"Is a table for 4 available tonight at 8pm?"</div>
                        <div class="example-card">"What's your cancellation policy?"</div>
                    </div>
                </div>
                <div class="section">
                    <h2>Built with</h2>
                    <div class="chip-row">
                        <span class="chip">FastAPI</span>
                        <span class="chip">LangGraph</span>
                        <span class="chip">LangChain</span>
                        <span class="chip">Gemini</span>
                        <span class="chip">Pinecone</span>
                        <span class="chip">SQL Database</span>
                        <span class="chip">Streamlit</span>
                    </div>
                </div>
                <div class="section">
                    <div class="author-card">
                        <div class="author-name">Muhammad Atif</div>
                        <div class="author-title">AI/ML Engineer</div>
                        <div class="author-links">
                            <a class="author-link" href="https://github.com/AtifQureshi110?tab=repositories" target="_blank" rel="noopener noreferrer">⬡ GitHub</a>
                            <a class="author-link" href="https://www.youtube.com/@AICornerOfficial110" target="_blank" rel="noopener noreferrer">▶ YouTube</a>
                            <a class="author-link" href="https://www.linkedin.com/in/matif110/" target="_blank" rel="noopener noreferrer">◈ LinkedIn</a>
                            <a class="author-link" href="https://www.instagram.com/atif_qureshi_110/" target="_blank" rel="noopener noreferrer">◎ Instagram</a>
                        </div>
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------
# Demo page — real chat interface talking to the FastAPI backend
# ---------------------------------------------------------------------
def render_demo_page() -> None:
    st.markdown(
        textwrap.dedent(
            """
            <div class="page-content">
                <div class="hero">
                    <p class="eyebrow">Live Demo</p>
                    <h1>Talk to the assistant.</h1>
                    <p class="hero-sub">
                        Ask about the menu, check table availability, or make a reservation —
                        the agent figures out what it needs to do.
                    </p>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown('<div class="page-content"><div class="chat-shell">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input("Ask about the menu, a reservation, or anything else…")

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        with st.chat_message("assistant"):
            with st.status("🤔 Understanding your question…", expanded=True) as status:
                try:
                    time.sleep(1.0)  # ← add this: lets user read the first label before backend even responds

                    response = requests.post(
                        BACKEND_URL,
                        json={
                            "message": user_message,
                            "thread_id": st.session_state.thread_id,
                        },
                        timeout=60,
                    )
                    response.raise_for_status()
                    data = response.json()
                    reply = data.get("reply", "Sorry, I didn't get a reply back.")
                    intent = data.get("intent")

                    status.update(label="🧭 Deciding which tool to use…")
                    time.sleep(1.5)   # ← was 0.8, now 1.5

                    status.update(label=TOOL_LABELS.get(intent, "💬 Thinking…"))
                    time.sleep(1.8)   # ← was 1.2, now 1.8

                    status.update(label="✅ Done", state="complete")
                    time.sleep(0.6)   # ← add this: lets user see "Done" before it collapses
                except requests.exceptions.ConnectionError:
                    reply = (
                        "⚠️ Can't reach the backend right now. "
                        "Make sure the FastAPI server is running on **http://localhost:8000** "
                        "(`uvicorn app.main:app --reload`), then try again."
                    )
                    status.update(label="⚠️ Backend unreachable", state="error")
                except requests.exceptions.Timeout:
                    reply = "⚠️ The backend took too long to respond. Please try again."
                    status.update(label="⚠️ Timed out", state="error")
                except requests.exceptions.HTTPError:
                    reply = f"⚠️ The backend returned an error (status {response.status_code}). Please try again."
                    status.update(label="⚠️ Backend error", state="error")
                except Exception:
                    reply = "⚠️ Something went wrong talking to the backend. Please try again."
                    status.update(label="⚠️ Something went wrong", state="error")

            st.markdown(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    st.markdown("</div></div>", unsafe_allow_html=True)

if current_page == "about":
    render_about_page()
else:
    render_demo_page()