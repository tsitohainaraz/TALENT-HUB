import streamlit as st
import json
import os
from datetime import datetime, date
from pathlib import Path

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnnotaCore — Expert AI Annotators",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Drive Folder Links by Specialty ───────────────────────────────────────────
SPECIALTY_DRIVE_FOLDERS = {
    "Astronomie": "https://drive.google.com/drive/u/0/folders/1pP5ReGGCa7hl7xvN7Uq2ifaKO_9k7g52",
    "Chimie": "https://drive.google.com/drive/u/0/folders/1QTCIbzqHq_4A7uqsj4xt8zRgQGZYvhwH",
    "Droit": "https://drive.google.com/drive/u/0/folders/1CdRdDuJ8gAMY4HyYtPNMsPDByz7DsqFq",
    "Génie des matériaux": "https://drive.google.com/drive/u/0/folders/1kUEk83-j0G5RvoFTo4tj3xCyvK64Zgq2",
    "Génie Electrique": "https://drive.google.com/drive/u/0/folders/1bj3dQgHBPwfPyvAiYgzsxp64mHExPMSx",
    "Histoire": "https://drive.google.com/drive/u/0/folders/1IFVTa8tV9pE8HruPLhtKWCSkU8O3Qasa",
    "Mathématiques": "https://drive.google.com/drive/u/0/folders/192hXOppB_-0f7TPVGzQId0nb1wxbdsAO",
    "Neurosciences": "https://drive.google.com/drive/u/0/folders/1UP45h2U6_6XVLpnBA-xvo1RltwRWIl5i",
    "Philosophie": "https://drive.google.com/drive/u/0/folders/1LoJz1MZLt3WZ_9dQRziw21kHkdh8r8s_",
    "Physique": "https://drive.google.com/drive/u/0/folders/1TViay4Os-Jyo2f2L592ZfDiBM608ZjL8",
    "Psychologie": "https://drive.google.com/drive/u/0/folders/15xzZQrYc6u43xXsLzlLbyedDaQv2duPd",
    "Sciences de l'information": "https://drive.google.com/drive/u/0/folders/171wR4DVBONV6tvKLoaJMWVePC-hOcflN",
    "Sciences de la Terre": "https://drive.google.com/drive/u/0/folders/1MnAOT99SJt7CVj5SjbQAa-McWg7_isVn",
    "Sciences du vivant": "https://drive.google.com/drive/u/0/folders/1Y8TRFetyqn-KuP_XgaO6MjrYa2_Ku8bP",
}

SPECIALTY_ICONS = {
    "Astronomie": "🔭",
    "Chimie": "⚗️",
    "Droit": "⚖️",
    "Génie des matériaux": "🧱",
    "Génie Electrique": "⚡",
    "Histoire": "📜",
    "Mathématiques": "∑",
    "Neurosciences": "🧠",
    "Philosophie": "💡",
    "Physique": "⚛️",
    "Psychologie": "🧘",
    "Sciences de l'information": "💻",
    "Sciences de la Terre": "🌍",
    "Sciences du vivant": "🧬",
}

# ─── Inline CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-deep: #020812;
    --bg-card: #060f1e;
    --bg-card2: #081526;
    --accent-cyan: #00e5ff;
    --accent-blue: #2979ff;
    --accent-purple: #7c3aed;
    --accent-green: #00e676;
    --accent-amber: #ffab00;
    --text-primary: #e8f4fd;
    --text-secondary: #7fa8c9;
    --text-muted: #3d6080;
    --border: rgba(0,229,255,0.12);
    --border-hover: rgba(0,229,255,0.35);
    --glow-cyan: 0 0 30px rgba(0,229,255,0.15);
    --glow-blue: 0 0 30px rgba(41,121,255,0.2);
}

/* Global reset */
.stApp {
    background: var(--bg-deep) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}

/* Animated starfield background */
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
        radial-gradient(1px 1px at 85% 35%, rgba(0,229,255,0.4) 0%, transparent 100%),
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

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
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

.filter-section {
    margin-bottom: 1.5rem;
}

.filter-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--accent-cyan);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* Streamlit widget overrides */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(0,229,255,0.04) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
}

.stTextInput > div > div > input {
    background: rgba(0,229,255,0.04) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(0,229,255,0.1), rgba(41,121,255,0.1)) !important;
    border: 1px solid rgba(0,229,255,0.3) !important;
    color: var(--accent-cyan) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    border-radius: 6px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,229,255,0.2), rgba(41,121,255,0.2)) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 20px rgba(0,229,255,0.2) !important;
    transform: translateY(-1px) !important;
}

/* Hero Section */
.hero-section {
    text-align: center;
    padding: 3rem 2rem 2rem;
    position: relative;
    z-index: 1;
    animation: fadeInDown 0.8s ease;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0,229,255,0.2); }
    50% { box-shadow: 0 0 40px rgba(0,229,255,0.4), 0 0 60px rgba(41,121,255,0.2); }
}

@keyframes scan-line {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes spin-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent-cyan);
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.hero-eyebrow::before,
.hero-eyebrow::after {
    content: '';
    width: 30px;
    height: 1px;
    background: var(--accent-cyan);
    opacity: 0.5;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 1rem;
}

.hero-title .accent {
    color: var(--accent-cyan);
    text-shadow: 0 0 30px rgba(0,229,255,0.4);
}

.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.7;
    font-weight: 300;
}

.hero-atom {
    font-size: 3rem;
    animation: float 4s ease-in-out infinite;
    display: inline-block;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 15px rgba(0,229,255,0.5));
}

/* Stats Bar */
.stats-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin: 0 auto 2.5rem;
    max-width: 700px;
    background: rgba(0,229,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 2rem;
    backdrop-filter: blur(10px);
    animation: fadeInUp 1s ease 0.3s both;
}

.stat-item {
    flex: 1;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: var(--text-primary);
    display: block;
    line-height: 1;
}

.stat-number.open-num { color: var(--accent-green); text-shadow: 0 0 15px rgba(0,230,118,0.4); }
.stat-number.occ-num { color: var(--accent-amber); }

.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 4px;
    display: block;
}

.stat-divider {
    width: 1px;
    height: 40px;
    background: var(--border);
    margin: 0 1.5rem;
}

/* Specialty Folders Section */
.folders-section {
    margin: 0 0 3rem;
    animation: fadeInUp 0.8s ease 0.5s both;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--accent-cyan);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

.folders-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
}

.folder-card {
    background: rgba(0,229,255,0.03);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    text-decoration: none;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    position: relative;
    overflow: hidden;
}

.folder-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.05), transparent);
    transition: left 0.5s ease;
}

.folder-card:hover::before {
    left: 100%;
}

.folder-card:hover {
    border-color: var(--border-hover);
    background: rgba(0,229,255,0.07);
    transform: translateY(-2px);
    box-shadow: var(--glow-cyan);
    text-decoration: none;
}

.folder-icon {
    font-size: 1.4rem;
    filter: drop-shadow(0 0 8px rgba(0,229,255,0.3));
    flex-shrink: 0;
}

.folder-name {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: var(--text-primary);
    font-weight: 500;
    line-height: 1.3;
}

.folder-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: var(--accent-cyan);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Profile Cards */
.profiles-section {
    animation: fadeInUp 0.8s ease 0.7s both;
}

.profile-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s ease;
    animation: fadeInUp 0.6s ease both;
}

.profile-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.profile-card:hover {
    border-color: var(--border-hover);
    background: var(--bg-card2);
    transform: translateY(-3px);
    box-shadow: var(--glow-cyan), 0 20px 40px rgba(0,0,0,0.4);
}

.profile-card:hover::before {
    opacity: 1;
}

/* Corner decoration */
.profile-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 40px; height: 40px;
    background: linear-gradient(225deg, rgba(0,229,255,0.08) 0%, transparent 60%);
    border-radius: 0 14px 0 0;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.avatar {
    width: 52px;
    height: 52px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--bg-deep);
    flex-shrink: 0;
    position: relative;
    animation: pulse-glow 3s ease-in-out infinite;
}

.avatar-open {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
}

.avatar-occupied {
    background: linear-gradient(135deg, #4a5568, #2d3748);
    color: var(--text-secondary);
    animation: none;
}

.card-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-primary);
    margin: 0 0 2px;
    letter-spacing: -0.01em;
}

.card-specialty {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--accent-cyan);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0;
}

.card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.85rem;
}

.tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.tag-edu {
    background: rgba(41,121,255,0.12);
    color: #82b1ff;
    border: 1px solid rgba(41,121,255,0.2);
}

.tag-gender {
    background: rgba(124,58,237,0.12);
    color: #c084fc;
    border: 1px solid rgba(124,58,237,0.2);
}

.card-bio {
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.65;
    margin-bottom: 1rem;
    font-weight: 300;
}

.sched-note {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--accent-amber);
    margin-bottom: 0.75rem;
    padding: 5px 10px;
    background: rgba(255,171,0,0.08);
    border-radius: 5px;
    border: 1px solid rgba(255,171,0,0.15);
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.85rem;
}

.status-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

.status-open {
    background: rgba(0,230,118,0.1);
    color: var(--accent-green);
    border: 1px solid rgba(0,230,118,0.25);
}

.status-open::before {
    background: var(--accent-green);
    box-shadow: 0 0 6px var(--accent-green);
    animation: blink 2s ease-in-out infinite;
}

.status-occupied {
    background: rgba(255,171,0,0.08);
    color: var(--accent-amber);
    border: 1px solid rgba(255,171,0,0.2);
}

.status-occupied::before {
    background: var(--accent-amber);
}

/* Download button */
.dl-button {
    display: block;
    text-align: center;
    padding: 0.6rem 1rem;
    background: linear-gradient(135deg, rgba(0,229,255,0.08), rgba(41,121,255,0.08));
    border: 1px solid rgba(0,229,255,0.25);
    border-radius: 8px;
    color: var(--accent-cyan) !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-decoration: none !important;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.dl-button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.1), transparent);
    transition: left 0.4s ease;
}

.dl-button:hover {
    background: linear-gradient(135deg, rgba(0,229,255,0.15), rgba(41,121,255,0.15));
    border-color: var(--accent-cyan);
    box-shadow: 0 0 20px rgba(0,229,255,0.2);
    transform: translateY(-1px);
    color: var(--accent-cyan) !important;
    text-decoration: none !important;
}

.dl-button:hover::before {
    left: 100%;
}

.dl-button-disabled {
    display: block;
    text-align: center;
    padding: 0.6rem 1rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2.5rem 1rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}

.footer span:first-child {
    color: var(--accent-cyan);
    font-weight: 700;
}

/* Scan line animation */
.scan-line {
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.4), transparent);
    animation: scan-line 8s linear infinite;
    pointer-events: none;
    z-index: 9999;
}

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
}

/* Admin panel */
.stExpander {
    background: rgba(0,229,255,0.02) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* Override Streamlit defaults */
h1, h2, h3 { color: var(--text-primary) !important; }
p { color: var(--text-secondary); }
label { color: var(--text-secondary) !important; font-family: 'Space Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.05em !important; }

/* Responsive */
@media (max-width: 768px) {
    .stats-bar { flex-wrap: wrap; gap: 1rem; padding: 1rem; }
    .stat-divider { display: none; }
    .folders-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 2rem; }
}
</style>

<div class="scan-line"></div>
""", unsafe_allow_html=True)

# ─── Data Helpers ──────────────────────────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "data" / "profiles.json"

def load_profiles():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        default = [
            {
                "id": 1, "name": "Dr. Amara Diallo", "specialty": "Physique",
                "education": "PhD", "gender": "Female",
                "manual_status": "Open", "scheduled_date": None,
                "bio": "Spécialiste en physique des particules — maîtrise de ROOT, Geant4 et analyse de données de collisions.",
                "photo_initial": "AD"
            },
            {
                "id": 2, "name": "Marcus Chen", "specialty": "Neurosciences",
                "education": "PhD", "gender": "Male",
                "manual_status": "Open", "scheduled_date": None,
                "bio": "Expert en neuroimagerie et analyse de signaux EEG/IRM. Expérience en annotation de benchmarks cognitifs.",
                "photo_initial": "MC"
            },
            {
                "id": 3, "name": "Fatou Ndiaye", "specialty": "Astronomie",
                "education": "Master", "gender": "Female",
                "manual_status": "Occupied", "scheduled_date": "2026-05-15",
                "bio": "Astronome spécialisée dans l'analyse de données spectrales avec Aladin, DS9 et TOPCAT.",
                "photo_initial": "FN"
            },
            {
                "id": 4, "name": "Dr. Ibrahim Koné", "specialty": "Génie Electrique",
                "education": "PhD", "gender": "Male",
                "manual_status": "Open", "scheduled_date": None,
                "bio": "Ingénieur expert en simulation de circuits avec KiCad, LTspice et Qucs-S.",
                "photo_initial": "IK"
            },
            {
                "id": 5, "name": "Léa Fontaine", "specialty": "Chimie",
                "education": "Master", "gender": "Female",
                "manual_status": "Open", "scheduled_date": None,
                "bio": "Chimiste computationnelle spécialisée en modélisation moléculaire et analyse structurale.",
                "photo_initial": "LF"
            },
            {
                "id": 6, "name": "Dr. Youssouf Barry", "specialty": "Mathématiques",
                "education": "PhD", "gender": "Male",
                "manual_status": "Occupied", "scheduled_date": None,
                "bio": "Mathématicien expert en calcul symbolique, analyse numérique et traitement de données avec SageMath.",
                "photo_initial": "YB"
            },
        ]
        with open(DATA_FILE, "w") as f:
            json.dump(default, f, indent=2)
    with open(DATA_FILE) as f:
        return json.load(f)

def save_profiles(profiles):
    with open(DATA_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def get_effective_status(profile):
    today = date.today()
    if profile.get("scheduled_date"):
        scheduled = datetime.strptime(profile["scheduled_date"], "%Y-%m-%d").date()
        if today < scheduled:
            return "Occupied", f"Disponible après le {scheduled.strftime('%d/%m/%Y')}"
        else:
            return "Open", "Disponible"
    status = profile.get("manual_status", "Open")
    return status, "Disponible" if status == "Open" else "En mission"

def get_next_id(profiles):
    return max((p["id"] for p in profiles), default=0) + 1

# ─── Session State ─────────────────────────────────────────────────────────────
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", st.secrets.get("ADMIN_PASSWORD", "admin2024") if hasattr(st, 'secrets') else "admin2024")

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">⚛ AnnotaCore
            <span>AI Data Annotation Specialists</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="filter-label">🔍 Filtres</p>', unsafe_allow_html=True)

    profiles_all = load_profiles()
    specialties = sorted(set(p["specialty"] for p in profiles_all))
    educations = ["Bachelor", "Master", "PhD"]

    filter_status = st.selectbox("Disponibilité", ["Tous", "Open", "Occupied"])
    filter_specialty = st.multiselect("Spécialité", specialties, placeholder="Toutes les spécialités")
    filter_education = st.multiselect("Niveau d'études", educations, placeholder="Tous les niveaux")
    filter_gender = st.selectbox("Genre", ["Tous", "Female", "Male"])

    st.markdown("---")
    st.markdown('<p class="filter-label">⚙️ Admin</p>', unsafe_allow_html=True)

    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Mot de passe admin", type="password", placeholder="••••••••")
        if st.button("Connexion", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.admin_mode = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect")
    else:
        st.success("✓ Mode admin actif")
        if st.button("Déconnexion", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_mode = False
            st.rerun()

# ─── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-atom">⚛</div>
    <div class="hero-eyebrow">Intelligence Artificielle · Annotation Scientifique</div>
    <h1 class="hero-title">Nos Experts en<br><span class="accent">Data Annotation</span></h1>
    <p class="hero-subtitle">
        Spécialistes pluridisciplinaires formés aux benchmarks d'IA de niveau recherche.
        Parcourez nos profils, consultez les CV et contactez les experts disponibles.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Bar ─────────────────────────────────────────────────────────────────
profiles = load_profiles()
for p in profiles:
    eff_status, eff_label = get_effective_status(p)
    p["_effective_status"] = eff_status
    p["_status_label"] = eff_label

total = len(profiles)
open_count = sum(1 for p in profiles if p["_effective_status"] == "Open")
occupied_count = total - open_count

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-number">{total}</span>
        <span class="stat-label">Experts Total</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number open-num">{open_count}</span>
        <span class="stat-label">Disponibles</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number occ-num">{occupied_count}</span>
        <span class="stat-label">En mission</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number">{len(SPECIALTY_DRIVE_FOLDERS)}</span>
        <span class="stat-label">Domaines</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Specialty Folders Section ─────────────────────────────────────────────────
st.markdown("""
<div class="folders-section">
    <div class="section-header">📁 Dossiers CV par Spécialité</div>
    <div class="folders-grid">
""", unsafe_allow_html=True)

folders_html = ""
for specialty, link in SPECIALTY_DRIVE_FOLDERS.items():
    icon = SPECIALTY_ICONS.get(specialty, "📂")
    folders_html += f"""
        <a href="{link}" target="_blank" class="folder-card">
            <span class="folder-icon">{icon}</span>
            <div>
                <div class="folder-name">{specialty}</div>
                <div class="folder-sub">Voir les CV →</div>
            </div>
        </a>
    """

st.markdown(folders_html + "</div></div>", unsafe_allow_html=True)

# ─── Filter Profiles ───────────────────────────────────────────────────────────
filtered = profiles
if filter_status != "Tous":
    filtered = [p for p in filtered if p["_effective_status"] == filter_status]
if filter_specialty:
    filtered = [p for p in filtered if p["specialty"] in filter_specialty]
if filter_education:
    filtered = [p for p in filtered if p["education"] in filter_education]
if filter_gender != "Tous":
    filtered = [p for p in filtered if p["gender"] == filter_gender]

# ─── Profile Cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">👤 Profils des Spécialistes</div>', unsafe_allow_html=True)

if not filtered:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔎</div>
        <p>Aucun profil ne correspond aux filtres sélectionnés.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    cols_per_row = 3
    rows = [filtered[i:i+cols_per_row] for i in range(0, len(filtered), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, profile in enumerate(row):
            with cols[idx]:
                eff_status = profile["_effective_status"]
                status_label = profile["_status_label"]
                status_class = "open" if eff_status == "Open" else "occupied"

                sched_note = ""
                if profile.get("scheduled_date"):
                    sched = datetime.strptime(profile["scheduled_date"], "%Y-%m-%d").date()
                    if date.today() < sched:
                        sched_note = f'<div class="sched-note">🗓 Disponible après le {sched.strftime("%d/%m/%Y")}</div>'

                edu_icons = {"Bachelor": "🎓", "Master": "📚", "PhD": "🏛️"}
                edu_icon = edu_icons.get(profile["education"], "🎓")
                gender_icon = "♀" if profile["gender"] == "Female" else "♂"
                specialty_icon = SPECIALTY_ICONS.get(profile["specialty"], "🔬")
                initials = profile.get("photo_initial", profile["name"][:2].upper())

                status_text = "Disponible" if eff_status == "Open" else "En mission"

                card_html = f"""
                <div class="profile-card">
                    <div class="card-header">
                        <div class="avatar avatar-{status_class}">{initials}</div>
                        <div class="card-meta">
                            <h3 class="card-name">{profile['name']}</h3>
                            <p class="card-specialty">{specialty_icon} {profile['specialty']}</p>
                        </div>
                    </div>
                    <div class="card-tags">
                        <span class="tag tag-edu">{edu_icon} {profile['education']}</span>
                        <span class="tag tag-gender">{gender_icon} {profile['gender']}</span>
                    </div>
                    <p class="card-bio">{profile.get('bio', '')}</p>
                    {sched_note}
                    <div class="status-badge status-{status_class}">{status_text}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # CV Download button — links to specialty folder
                specialty = profile.get("specialty", "")
                folder_link = SPECIALTY_DRIVE_FOLDERS.get(specialty)

                if folder_link:
                    st.markdown(f"""
                    <a href="{folder_link}" target="_blank" class="dl-button">
                        📁 Voir les CV — {specialty}
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="dl-button-disabled">CV non disponible</div>', unsafe_allow_html=True)

                # Admin Controls
                if st.session_state.admin_mode:
                    with st.expander("⚙️ Modifier le profil", expanded=False):
                        pid = profile["id"]

                        new_name = st.text_input("Nom complet", value=profile["name"], key=f"name_{pid}")
                        new_specialty = st.selectbox(
                            "Spécialité",
                            list(SPECIALTY_DRIVE_FOLDERS.keys()),
                            index=list(SPECIALTY_DRIVE_FOLDERS.keys()).index(profile["specialty"]) if profile["specialty"] in SPECIALTY_DRIVE_FOLDERS else 0,
                            key=f"spec_{pid}"
                        )
                        new_bio = st.text_area("Bio", value=profile.get("bio",""), key=f"bio_{pid}", height=80)
                        new_status = st.selectbox(
                            "Statut", ["Open", "Occupied"],
                            index=0 if profile["manual_status"] == "Open" else 1,
                            key=f"status_{pid}"
                        )
                        new_edu = st.selectbox(
                            "Niveau",
                            ["Bachelor", "Master", "PhD"],
                            index=["Bachelor", "Master", "PhD"].index(profile.get("education","Master")),
                            key=f"edu_{pid}"
                        )

                        sched_val = None
                        if profile.get("scheduled_date"):
                            sched_val = datetime.strptime(profile["scheduled_date"], "%Y-%m-%d").date()
                        new_date = st.date_input(
                            "Disponible après (optionnel)",
                            value=sched_val, min_value=date.today(),
                            key=f"date_{pid}"
                        )
                        clear_date = st.checkbox("Effacer la date", key=f"clear_{pid}")

                        if st.button("💾 Sauvegarder", key=f"save_{pid}", use_container_width=True):
                            all_profiles = load_profiles()
                            for p in all_profiles:
                                if p["id"] == pid:
                                    p["name"] = new_name
                                    p["specialty"] = new_specialty
                                    p["bio"] = new_bio
                                    p["manual_status"] = new_status
                                    p["education"] = new_edu
                                    p["photo_initial"] = "".join([w[0].upper() for w in new_name.split()[:2]])
                                    if clear_date:
                                        p["scheduled_date"] = None
                                    elif new_date:
                                        p["scheduled_date"] = new_date.strftime("%Y-%m-%d")
                            save_profiles(all_profiles)
                            st.success("Profil mis à jour !")
                            st.rerun()

# ─── Admin: Add New Profile ────────────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("---")
    st.markdown('<h2 class="section-title">➕ Ajouter un nouveau profil</h2>', unsafe_allow_html=True)

    with st.form("add_profile_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("Nom complet *", placeholder="ex: Dr. Jane Smith")
            new_specialty = st.selectbox("Spécialité *", list(SPECIALTY_DRIVE_FOLDERS.keys()))
            new_bio = st.text_area("Bio courte", placeholder="Description de l'expertise…", height=80)
        with c2:
            new_education = st.selectbox("Niveau d'études *", ["Bachelor", "Master", "PhD"])
            new_gender = st.selectbox("Genre *", ["Female", "Male"])
            new_status = st.selectbox("Statut initial", ["Open", "Occupied"])

        new_avail_date = st.date_input("Date de disponibilité (optionnel)", value=None, min_value=date.today())

        submitted = st.form_submit_button("⚛ Ajouter le profil", use_container_width=True)
        if submitted:
            if not new_name or not new_specialty:
                st.error("Le nom et la spécialité sont obligatoires.")
            else:
                all_p = load_profiles()
                initials = "".join([w[0].upper() for w in new_name.split()[:2]])
                new_profile = {
                    "id": get_next_id(all_p),
                    "name": new_name,
                    "specialty": new_specialty,
                    "education": new_education,
                    "gender": new_gender,
                    "manual_status": new_status,
                    "scheduled_date": new_avail_date.strftime("%Y-%m-%d") if new_avail_date else None,
                    "bio": new_bio,
                    "photo_initial": initials,
                }
                all_p.append(new_profile)
                save_profiles(all_p)
                st.success(f"✓ Profil de **{new_name}** ajouté avec succès !")
                st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⚛ AnnotaCore</span>
    <span>·</span>
    <span>AI Data Annotation Specialists</span>
    <span>·</span>
    <span>Profils mis à jour en temps réel</span>
</div>
""", unsafe_allow_html=True)
