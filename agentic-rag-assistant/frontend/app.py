from ui.components import (load_css, render_navbar, render_workflow_diagram)
from components.uploader import get_source
from api.client import (check_source,ingest_source)
import streamlit as st
import os, sys
from api.client import ask_ai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ================================================================
# BACKEND CONFIG
# ================================================================
BACKEND_URL = "http://localhost:8000"

# set_page_config MUST be the very first Streamlit command
st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS once, using the real loader — reads frontend/assets/style.css
load_css()
active_page = st.query_params.get("page", "About the Project")
render_navbar(active_page)

# ================================================================
# STREAMLIT STATE MANAGEMENT
# ================================================================

def clear_source_state():
    keys = [ "source", "source_check", "document_uploader", "url_input" ]
    for key in keys:
        st.session_state.pop(key, None)
    st.rerun()
if active_page == "About the Project":
    # Hero section
    st.markdown("""
    <div class="hero">
        <h2>What is this project?</h2>
        <p>
        The Agentic RAG Assistant is a production-grade AI system that reads your documents
        — websites, PDFs, Word files, or plain text — stores them as searchable vectors in Pinecone,
        and answers your questions using only the information inside those documents.
        It uses a LangGraph state machine to intelligently route each question through either
        a fast simple path or a deeper multi-step reasoning path depending on complexity.
        </p>
        <div class="author">Built by Muhammad Atif &nbsp;·&nbsp; AI/ML Engineer</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card"><div class="feature-icon">📥</div><div class="feature-title">Ingest</div><div class="feature-desc">URLs · PDFs · DOCX · TXT files stored as vectors in Pinecone</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><div class="feature-title">Retrieve</div><div class="feature-desc">Questions are embedded and matched against stored document chunks</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card"><div class="feature-icon">💬</div><div class="feature-title">Answer</div><div class="feature-desc">Gemini generates a grounded human-toned answer using only your documents</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### LangGraph Workflow")
        render_workflow_diagram()

    with col2:
        st.markdown("#### Key Features")
        st.markdown("""
        <ul class="feature-list">
            <li>Simple vs Complex query routing</li>
            <li>Planner Agent for multi-step reasoning</li>
            <li>Verification before answer generation</li>
            <li>Vocabulary expansion for better retrieval</li>
            <li>Human-toned answers, no hallucination</li>
            <li>Supports URLs, PDF, DOCX, TXT</li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("#### Tech Stack")
        st.markdown("`LangGraph` `Pinecone` `Gemini` `Python` `Streamlit` `FastApi`")

        st.markdown("#### Author")
        st.markdown("""
        <div class="author-card">
            <div class="author-name">Muhammad Atif</div>
            <div class="author-title">AI/ML Engineer</div>
            <div class="author-links">
                <a class="author-link" href="https://github.com/AtifQureshi110?tab=repositories" target="_blank">⬡ GitHub</a>
                <a class="author-link" href="https://www.youtube.com/@AICornerOfficial110" target="_blank">▶ YouTube</a>
                <a class="author-link" href="https://www.linkedin.com/in/matif110/" target="_blank">in LinkedIn</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


elif active_page == "Live Demo":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ================================================================
    # MAIN LAYOUT
    # ================================================================

    col_source, col_chat = st.columns([1, 2],gap="large")

    # ================================================================
    # LEFT PANEL
    # ================================================================

    with col_source:
        with st.container(border=True):
            st.markdown("""
                ### 📚 Knowledge Base
                Upload documents or add website URLs
                to create your private AI knowledge base.
                """
            )

            # -----------------------------
            # SOURCE INPUT
            # -----------------------------

            source = get_source()
            if source:
                st.session_state["source"] = source
                with st.spinner("🔍 Checking knowledge base..."):
                    result = check_source( source )
                st.session_state["source_check"] = result
            # -----------------------------
            # SOURCE STATUS
            # -----------------------------

            if "source_check" in st.session_state:
                result = st.session_state["source_check"]

                # Existing source
                if result["exists"]:
                    st.warning("⚠️ This source already exists in your knowledge base.")

                    col1, col2 = st.columns(2)

                    # UPDATE BUTTON
                    with col1:
                        if st.button("🔄 Update",use_container_width=True,key="update_source"):
                            with st.spinner("Updating knowledge base..."):
                                response = ingest_source(st.session_state["source"],force_update=True)
                            if response["success"]:
                                st.success("✅ Knowledge base updated successfully")
                                clear_source_state()
                            else:
                                st.error(response["message"])
                    # CANCEL BUTTON
                    with col2:
                        if st.button("❌ Cancel",use_container_width=True,key="cancel_source"):
                            clear_source_state()
                            st.success("✅ Operation cancelled")
                # New source
                else:
                    st.success("✅ New source detected")
                    if st.button("🚀 Start Processing",use_container_width=True,key="start_ingestion"):
                        with st.spinner("Processing document..."):
                            response = ingest_source(st.session_state["source"],force_update=False)
                        if response["success"]:
                            st.success("🎉 Document added successfully")
                            clear_source_state()
                        else:
                            st.error(response["message"])

        # ============================================================
        # SYSTEM STATUS CARD
        # ============================================================


        with st.container(border=True):

            st.markdown("""
                ### 📊 System Status

                🟢 Backend: Connected
                        
                🧠 Vector Database: Pinecone
                        
                🔗 Workflow Engine: LangGraph
                        
                ⚡ LLM: Gemini
                """
            )

    # ================================================================
    # RIGHT PANEL - CHAT
    # ================================================================

    with col_chat:
        with st.container(border=True):

            # -----------------------------
            # SESSION STATE INIT
            # -----------------------------
            if "messages" not in st.session_state:
                st.session_state.messages = []

            if "pending_question" not in st.session_state:
                st.session_state.pending_question = None

            # -----------------------------
            # HEADER
            # -----------------------------
            col_title, col_new = st.columns([6, 1])

            with col_title:
                st.markdown(
                    """
                    ### 💬 AI Assistant
                    Ask questions from your uploaded documents.
                    """
                )

            with col_new:
                if st.button(
                    "🗑️ New Chat",
                    key="new_chat_btn",
                    use_container_width=True
                ):
                    st.session_state.messages = []
                    st.session_state.pending_question = None
                    st.rerun()

            # -----------------------------
            # EXAMPLE QUESTIONS
            # -----------------------------
            st.info(
                """
                Example questions:

                • Summarize this document

                • Explain the important concepts

                • Find key information

                • Compare two documents
                """
            )

            # -----------------------------
            # DISPLAY CHAT HISTORY
            # -----------------------------
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Show a live "Thinking..." bubble if a question is awaiting an answer
            if st.session_state.pending_question:
                with st.chat_message("assistant"):
                    st.write("Thinking...")

            # -----------------------------
            # CHAT INPUT
            # -----------------------------
            question = st.chat_input( "Ask something about your documents..." )

            # -----------------------------
            # PROCESS QUESTION (two-phase rerun)
            # -----------------------------

            if question:
                # Phase 1: save the question, mark it pending, rerun immediately
                st.session_state.messages.append(
                    { "role": "user", "content": question }
                )
                st.session_state.pending_question = question
                st.rerun()

            elif st.session_state.pending_question:
                # Phase 2: fetch the answer, save it, clear pending, rerun again
                q = st.session_state.pending_question

                response = ask_ai(q)
                answer = response.get("answer", "No answer received.")

                st.session_state.messages.append( {"role": "assistant", "content": answer} )
                st.session_state.pending_question = None
                st.rerun()