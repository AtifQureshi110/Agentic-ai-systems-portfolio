import os
import streamlit as st

SAVE_DIR = "files"

# ==========================================
# FILE UPLOAD
# ==========================================

def upload_file():
    uploaded_file = st.file_uploader("Upload Document", type=[ "pdf", "docx", "txt" ], key="document_uploader" )

    if uploaded_file is None:
        return None

    os.makedirs(SAVE_DIR, exist_ok=True )
    file_path = os.path.join(SAVE_DIR, uploaded_file.name )


    if not os.path.exists(file_path):
        with open(file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
    return file_path

# ==========================================
# URL INPUT
# ==========================================

def input_url():
    url = st.text_input("Enter Website URL", key="url_input" )
    if url:
        return url.strip()
    return None 

# ==========================================
# SOURCE HANDLER
# ==========================================

def get_source():
    tab_file, tab_url = st.tabs( [ "📄 Upload File", "🌐 Add URL" ] )
    source = None 
    with tab_file: 
        file_source = upload_file()
        if file_source:
            source = file_source
    with tab_url:
        url_source = input_url()
        if url_source:
            source = url_source
    return source