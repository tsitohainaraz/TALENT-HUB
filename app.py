import streamlit as st
import json
import os
import re
from pathlib import Path
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnnotaCore — CV by Specialty",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Specialties and Icons ─────────────────────────────────────────────────────
SPECIALTIES = [
    "Astronomy", "Chemistry", "Law", "Materials Engineering",
    "Electrical Engineering", "History", "Mathematics", "Neuroscience",
    "Philosophy", "Physics", "Psychology", "Information Science",
    "Earth Sciences", "Life Sciences"
]

SPECIALTY_ICONS = {
    "Astronomy": "🔭", "Chemistry": "⚗️", "Law": "⚖️",
    "Materials Engineering": "🧱", "Electrical Engineering": "⚡", "History": "📜",
    "Mathematics": "∑", "Neuroscience": "🧠", "Philosophy": "💡",
    "Physics": "⚛️", "Psychology": "🧘", "Information Science": "💻",
    "Earth Sciences": "🌍", "Life Sciences": "🧬",
}

# Map English specialty names back to original French if needed for drive links?
# But we'll keep English for UI, user can adapt specialty names.

# ─── Data file for CVs ─────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
CV_FILE = DATA_DIR / "cvs.json"

def load_cvs():
    """Load CV list from JSON file."""
    if not CV_FILE.exists():
        # Example CVs (replace with your own)
        default_cvs = [
            {
                "id": 1,
                "title": "Dr. Amara Diallo - Particle Physics",
                "specialty": "Physics",
                "drive_link": "https://drive.google.com/file/d/1-example-id-1/preview",
                "description": "Specialist in particle physics, ROOT data analysis."
            },
            {
                "id": 2,
                "title": "Marcus Chen - Neuroimaging",
                "specialty": "Neuroscience",
                "drive_link": "https://drive.google.com/file/d/1-example-id-2/preview",
                "description": "Expert in EEG/fMRI signal processing."
            }
        ]
        save_cvs(default_cvs)
        return default_cvs
    with open(CV_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cvs(cvs):
    with open(CV_FILE, "w", encoding="utf-8") as f:
        json.dump(cvs, f, indent=2, ensure_ascii=False)

def get_next_id(cvs):
    return max((cv["id"] for cv in cvs), default=0) + 1

def extract_preview_url(drive_link):
    """Convert Google Drive share link to preview embed URL."""
    # Pattern for standard drive link: https://drive.google.com/file/d/FILE_ID/view
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"
    # If already a preview link, return as is
    if "/preview" in drive_link:
        return drive_link
    return drive_link

def extract_download_url(drive_link):
    """Extract direct download URL for Google Drive file."""
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return drive_link

# ─── Session State ─────────────────────────────────────────────────────────────
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "selected_specialty" not in st.session_state:
    st.session_state.selected_specialty = SPECIALTIES[0]

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2024")

# ─── CSS Theme (space/cyber style) ─────────────────────────────────────────────
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

.cv-delete {
    background: rgba(255,60,60,0.1);
    border-color: rgba(255,60,60,0.3);
    color: #ff6b6b;
}

.cv-delete:hover {
    background: rgba(255,60,60,0.2);
    border-color: #ff6b6b;
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

/* Preview iframe */
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

    st.markdown("### ⚙️ Admin")
    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Admin password", type="password", placeholder="••••••••")
        if st.button("Login", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.admin_mode = True
                st.rerun()
            else:
                st.error("Incorrect password")
    else:
        st.success("✅ Admin mode active")
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_mode = False
            st.rerun()

    st.markdown("---")
    total_cvs = len(load_cvs())
    st.markdown(f"**Total CVs:** {total_cvs}")

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <div style="font-size: 2.5rem;">📂</div>
    <h1 style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.5rem;">
        Expert <span style="color: #00e5ff;">CVs</span>
    </h1>
    <p style="color: #7fa8c9; max-width: 600px; margin: 0 auto;">
        Browse, preview and download CVs by specialty — all on this site.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Specialty Buttons (2 rows of 7) ──────────────────────────────────────────
st.markdown('<div class="specialty-buttons">', unsafe_allow_html=True)
cols = st.columns(7)
for idx, spec in enumerate(SPECIALTIES):
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

# ─── Display CVs for selected specialty ────────────────────────────────────────
selected = st.session_state.selected_specialty
cvs = load_cvs()
filtered_cvs = [cv for cv in cvs if cv["specialty"] == selected]

st.markdown(f"## {SPECIALTY_ICONS.get(selected, '📁')} {selected}")
st.caption(f"{len(filtered_cvs)} CV(s) available")

if not filtered_cvs:
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">📭</div>
        <p>No CVs found for <strong>{selected}</strong>.<br>Admin can add CVs using the form below.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display CVs in a grid
    cols = st.columns(2)
    for i, cv in enumerate(filtered_cvs):
        with cols[i % 2]:
            preview_url = extract_preview_url(cv["drive_link"])
            download_url = extract_download_url(cv["drive_link"])
            with st.container():
                st.markdown(f"""
                <div class="cv-card">
                    <div class="cv-title">📄 {cv['title']}</div>
                    <div class="cv-desc">{cv.get('description', 'No description')}</div>
                    <div class="cv-actions">
                        <a href="{download_url}" class="cv-button" target="_blank">⬇️ Download</a>
                """, unsafe_allow_html=True)
                # Preview button toggles an iframe
                preview_key = f"preview_{cv['id']}"
                if st.button("🔍 Preview", key=f"btn_preview_{cv['id']}", use_container_width=True):
                    st.session_state[preview_key] = not st.session_state.get(preview_key, False)
                if st.session_state.get(preview_key, False):
                    st.markdown(f"""
                    <div class="preview-container">
                        <iframe src="{preview_url}" width="100%" height="400" style="border:none;"></iframe>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)

                if st.session_state.admin_mode:
                    if st.button("🗑 Delete", key=f"del_{cv['id']}", use_container_width=True):
                        new_cvs = [c for c in load_cvs() if c["id"] != cv["id"]]
                        save_cvs(new_cvs)
                        st.success("CV deleted")
                        st.rerun()

# ─── Admin: Add new CV ─────────────────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("---")
    st.markdown("## ➕ Add a new CV")
    with st.form("add_cv_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("CV Title *", placeholder="e.g., Dr. Jane Smith - Machine Learning")
            specialty = st.selectbox("Specialty *", SPECIALTIES)
        with col2:
            drive_link = st.text_input("Google Drive Link *", placeholder="https://drive.google.com/file/d/.../view")
            description = st.text_area("Description (optional)", height=80)
        submitted = st.form_submit_button("📄 Add CV", use_container_width=True)
        if submitted:
            if not title or not specialty or not drive_link:
                st.error("Please fill all required fields.")
            else:
                all_cvs = load_cvs()
                new_id = get_next_id(all_cvs)
                all_cvs.append({
                    "id": new_id,
                    "title": title,
                    "specialty": specialty,
                    "drive_link": drive_link,
                    "description": description
                })
                save_cvs(all_cvs)
                st.success(f"CV '{title}' added successfully!")
                st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⚛ AnnotaCore · CV Management System</span>
    <span>—</span>
    <span>Data updated in real time</span>
</div>
""", unsafe_allow_html=True)
