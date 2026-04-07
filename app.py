import streamlit as st
import requests
import re
from pathlib import Path

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnnotaCore — CV by Specialty",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Specialty Folders (Google Drive folder links) ─────────────────────────────
# These are the exact links you provided. We extract folder IDs automatically.
SPECIALTY_FOLDERS = {
    "Astronomy": "https://drive.google.com/drive/folders/1pP5ReGGCa7hl7xvN7Uq2ifaKO_9k7g52",
    "Chemistry": "https://drive.google.com/drive/folders/1QTCIbzqHq_4A7uqsj4xt8zRgQGZYvhwH",
    "Law": "https://drive.google.com/drive/folders/1CdRdDuJ8gAMY4HyYtPNMsPDByz7DsqFq",
    "Materials Engineering": "https://drive.google.com/drive/folders/1kUEk83-j0G5RvoFTo4tj3xCyvK64Zgq2",
    "Electrical Engineering": "https://drive.google.com/drive/folders/1bj3dQgHBPwfPyvAiYgzsxp64mHExPMSx",
    "History": "https://drive.google.com/drive/folders/1IFVTa8tV9pE8HruPLhtKWCSkU8O3Qasa",
    "Mathematics": "https://drive.google.com/drive/folders/192hXOppB_-0f7TPVGzQId0nb1wxbdsAO",
    "Neuroscience": "https://drive.google.com/drive/folders/1UP45h2U6_6XVLpnBA-xvo1RltwRWIl5i",
    "Philosophy": "https://drive.google.com/drive/folders/1LoJz1MZLt3WZ_9dQRziw21kHkdh8r8s_",
    "Physics": "https://drive.google.com/drive/folders/1TViay4Os-Jyo2f2L592ZfDiBM608ZjL8",
    "Psychology": "https://drive.google.com/drive/folders/15xzZQrYc6u43xXsLzlLbyedDaQv2duPd",
    "Information Science": "https://drive.google.com/drive/folders/171wR4DVBONV6tvKLoaJMWVePC-hOcflN",
    "Earth Sciences": "https://drive.google.com/drive/folders/1MnAOT99SJt7CVj5SjbQAa-McWg7_isVn",
    "Life Sciences": "https://drive.google.com/drive/folders/1Y8TRFetyqn-KuP_XgaO6MjrYa2_Ku8bP",
}

SPECIALTY_ICONS = {
    "Astronomy": "🔭", "Chemistry": "⚗️", "Law": "⚖️",
    "Materials Engineering": "🧱", "Electrical Engineering": "⚡", "History": "📜",
    "Mathematics": "∑", "Neuroscience": "🧠", "Philosophy": "💡",
    "Physics": "⚛️", "Psychology": "🧘", "Information Science": "💻",
    "Earth Sciences": "🌍", "Life Sciences": "🧬",
}

# ─── Helper functions for Google Drive API ─────────────────────────────────────
def extract_folder_id(url):
    """Extract folder ID from Google Drive folder URL."""
    match = re.search(r'folders/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None

def get_files_in_folder(folder_id, api_key):
    """List all PDF files in a public Google Drive folder using API."""
    url = f"https://www.googleapis.com/drive/v3/files"
    params = {
        "q": f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false",
        "key": api_key,
        "fields": "files(id, name, webViewLink, size)",
        "pageSize": 100
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            files = response.json().get("files", [])
            return files
        else:
            st.error(f"API error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch files: {e}")
        return []

# ─── API Key from secrets ──────────────────────────────────────────────────────
try:
    DRIVE_API_KEY = st.secrets["DRIVE_API_KEY"]
except:
    DRIVE_API_KEY = None

if not DRIVE_API_KEY:
    st.error("⚠️ Google Drive API key not found. Please set DRIVE_API_KEY in .streamlit/secrets.toml")
    st.stop()

# ─── Session state for selected specialty ──────────────────────────────────────
if "selected_specialty" not in st.session_state:
    st.session_state.selected_specialty = list(SPECIALTY_FOLDERS.keys())[0]

# ─── CSS Theme (same elegant style) ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-deep: #020812;
    --bg-card: #060f1e;
    --bg-card2: #081526;
    --accent-cyan: #00e5ff;
    --accent-blue: #2979ff;
    --text-primary: #e8f4fd;
    --text-secondary: #7fa8c9;
    --text-muted: #3d6080;
    --border: rgba(0,229,255,0.12);
    --border-hover: rgba(0,229,255,0.35);
    --glow-cyan: 0 0 30px rgba(0,229,255,0.15);
}

.stApp {
    background: var(--bg-deep) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* Starfield background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(0,229,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 50% 10%, rgba(0,229,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 35%, rgba(0,229,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 90%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 45%, rgba(41,121,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 70%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(2px 2px at 40% 30%, rgba(0,229,255,0.3) 0%, transparent 100%),
        radial-gradient(2px 2px at 75% 15%, rgba(41,121,255,0.4) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* Grid overlay */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,229,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c1a 0%, #030e1f 100%) !important;
    border-right: 1px solid var(--border) !important;
}

.sidebar-brand {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}

.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    color: var(--accent-cyan);
    letter-spacing: -0.02em;
    text-shadow: 0 0 20px rgba(0,229,255,0.5);
}

.sidebar-logo span {
    color: var(--text-secondary);
    font-size: 0.65rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.15em;
    display: block;
    margin-top: 4px;
    text-transform: uppercase;
}

/* Specialty buttons */
.specialty-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin: 2rem 0 2rem;
    justify-content: center;
}

/* CV Cards */
.cv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.cv-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.cv-card:hover {
    border-color: var(--border-hover);
    background: var(--bg-card2);
    transform: translateY(-3px);
    box-shadow: var(--glow-cyan);
}

.cv-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.cv-card:hover::before {
    opacity: 1;
}

.cv-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    word-break: break-word;
}

.cv-desc {
    font-size: 0.75rem;
    color: var(--text-secondary);
    line-height: 1.4;
    margin-bottom: 1rem;
}

.cv-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.5rem;
    flex-wrap: wrap;
}

.cv-button {
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.25);
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent-cyan);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: all 0.2s;
    cursor: pointer;
}

.cv-button:hover {
    background: rgba(0,229,255,0.2);
    border-color: var(--accent-cyan);
    transform: translateY(-1px);
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: var(--text-muted);
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

.footer {
    text-align: center;
    padding: 2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-muted);
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}

.preview-container {
    margin-top: 1rem;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">📄 AnnotaCore
            <span>CV by Specialty</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**{len(SPECIALTY_FOLDERS)} specialties**")
    st.markdown("---")
    st.markdown("CVs are fetched live from Google Drive folders.")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <div style="font-size: 2.5rem;">📂</div>
    <h1 style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.5rem;">
        Expert <span style="color: #00e5ff;">CVs</span>
    </h1>
    <p style="color: #7fa8c9; max-width: 600px; margin: 0 auto;">
        Browse, preview and download CVs by specialty — live from Google Drive.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Specialty Buttons (2 rows of 7) ──────────────────────────────────────────
specialties = list(SPECIALTY_FOLDERS.keys())
st.markdown('<div class="specialty-buttons">', unsafe_allow_html=True)
cols = st.columns(7)
for idx, spec in enumerate(specialties):
    col = cols[idx % 7]
    icon = SPECIALTY_ICONS.get(spec, "📂")
    if st.session_state.selected_specialty == spec:
        btn = col.button(f"{icon} {spec}", key=f"spec_{spec}", use_container_width=True, type="primary")
    else:
        btn = col.button(f"{icon} {spec}", key=f"spec_{spec}", use_container_width=True, type="secondary")
    if btn:
        st.session_state.selected_specialty = spec
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ─── Fetch and display CVs for selected specialty ──────────────────────────────
selected = st.session_state.selected_specialty
folder_url = SPECIALTY_FOLDERS[selected]
folder_id = extract_folder_id(folder_url)

st.markdown(f"## {SPECIALTY_ICONS.get(selected, '📁')} {selected}")

if not folder_id:
    st.error("Invalid folder URL.")
else:
    with st.spinner("Fetching CVs from Google Drive..."):
        files = get_files_in_folder(folder_id, DRIVE_API_KEY)
    
    if not files:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <p>No PDF CVs found in <strong>{selected}</strong> folder.<br>
            Make sure the folder is public and contains PDF files.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption(f"{len(files)} CV(s) available")
        # Display in 2-column grid
        cols = st.columns(2)
        for i, file in enumerate(files):
            with cols[i % 2]:
                file_id = file["id"]
                file_name = file["name"]
                # Preview URL (embed)
                preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                # Download URL
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                
                # Human-readable size
                size_bytes = file.get("size", 0)
                size_kb = int(size_bytes) / 1024 if size_bytes else 0
                size_str = f"{size_kb:.0f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
                
                with st.container():
                    st.markdown(f"""
                    <div class="cv-card">
                        <div class="cv-title">📄 {file_name}</div>
                        <div class="cv-desc">Size: {size_str}</div>
                        <div class="cv-actions">
                            <a href="{download_url}" class="cv-button" target="_blank">⬇️ Download</a>
                    """, unsafe_allow_html=True)
                    preview_key = f"preview_{file_id}"
                    if st.button("🔍 Preview", key=f"preview_btn_{file_id}", use_container_width=True):
                        st.session_state[preview_key] = not st.session_state.get(preview_key, False)
                    if st.session_state.get(preview_key, False):
                        st.markdown(f"""
                        <div class="preview-container">
                            <iframe src="{preview_url}" width="100%" height="400" style="border:none;"></iframe>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div></div>", unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⚛ AnnotaCore · Live CVs from Google Drive</span>
    <span>—</span>
    <span>Updated automatically</span>
</div>
""", unsafe_allow_html=True)
