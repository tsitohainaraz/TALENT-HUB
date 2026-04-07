import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnnotaCore — CV par Spécialité",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Liens Google Drive par spécialité ─────────────────────────────────────────
SPECIALTY_DRIVE_FOLDERS = {
    "Astronomie": "https://drive.google.com/drive/folders/1pP5ReGGCa7hl7xvN7Uq2ifaKO_9k7g52",
    "Chimie": "https://drive.google.com/drive/folders/1QTCIbzqHq_4A7uqsj4xt8zRgQGZYvhwH",
    "Droit": "https://drive.google.com/drive/folders/1CdRdDuJ8gAMY4HyYtPNMsPDByz7DsqFq",
    "Génie des matériaux": "https://drive.google.com/drive/folders/1kUEk83-j0G5RvoFTo4tj3xCyvK64Zgq2",
    "Génie Electrique": "https://drive.google.com/drive/folders/1bj3dQgHBPwfPyvAiYgzsxp64mHExPMSx",
    "Histoire": "https://drive.google.com/drive/folders/1IFVTa8tV9pE8HruPLhtKWCSkU8O3Qasa",
    "Mathématiques": "https://drive.google.com/drive/folders/192hXOppB_-0f7TPVGzQId0nb1wxbdsAO",
    "Neurosciences": "https://drive.google.com/drive/folders/1UP45h2U6_6XVLpnBA-xvo1RltwRWIl5i",
    "Philosophie": "https://drive.google.com/drive/folders/1LoJz1MZLt3WZ_9dQRziw21kHkdh8r8s_",
    "Physique": "https://drive.google.com/drive/folders/1TViay4Os-Jyo2f2L592ZfDiBM608ZjL8",
    "Psychologie": "https://drive.google.com/drive/folders/15xzZQrYc6u43xXsLzlLbyedDaQv2duPd",
    "Sciences de l'information": "https://drive.google.com/drive/folders/171wR4DVBONV6tvKLoaJMWVePC-hOcflN",
    "Sciences de la Terre": "https://drive.google.com/drive/folders/1MnAOT99SJt7CVj5SjbQAa-McWg7_isVn",
    "Sciences du vivant": "https://drive.google.com/drive/folders/1Y8TRFetyqn-KuP_XgaO6MjrYa2_Ku8bP",
}

SPECIALTY_ICONS = {
    "Astronomie": "🔭", "Chimie": "⚗️", "Droit": "⚖️",
    "Génie des matériaux": "🧱", "Génie Electrique": "⚡", "Histoire": "📜",
    "Mathématiques": "∑", "Neurosciences": "🧠", "Philosophie": "💡",
    "Physique": "⚛️", "Psychologie": "🧘", "Sciences de l'information": "💻",
    "Sciences de la Terre": "🌍", "Sciences du vivant": "🧬",
}

# ─── CSS Thème (style spatial/cyber) ───────────────────────────────────────────
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

/* Boutons de spécialité */
.specialty-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin: 2rem 0 2rem;
    justify-content: center;
}

.spec-btn {
    background: rgba(0,229,255,0.05);
    border: 1px solid var(--border);
    border-radius: 40px;
    padding: 0.6rem 1.4rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.25s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.spec-btn:hover {
    background: rgba(0,229,255,0.15);
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    transform: translateY(-2px);
    box-shadow: var(--glow-cyan);
}

/* Carte du dossier */
.folder-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    max-width: 500px;
    margin: 2rem auto;
    transition: all 0.3s ease;
}

.folder-card:hover {
    border-color: var(--border-hover);
    background: var(--bg-card2);
    transform: translateY(-3px);
    box-shadow: var(--glow-cyan);
}

.folder-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.folder-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
}

.folder-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}

.drive-link {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,229,255,0.1), rgba(41,121,255,0.1));
    border: 1px solid var(--accent-cyan);
    border-radius: 40px;
    padding: 0.7rem 1.8rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: bold;
    color: var(--accent-cyan);
    text-decoration: none;
    transition: all 0.2s;
}

.drive-link:hover {
    background: rgba(0,229,255,0.2);
    transform: translateY(-2px);
    box-shadow: var(--glow-cyan);
    color: var(--accent-cyan);
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: var(--text-muted);
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
</style>
""", unsafe_allow_html=True)

# ─── Sidebar (informations) ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">📄 AnnotaCore
            <span>CV par spécialité</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"**{len(SPECIALTY_DRIVE_FOLDERS)} domaines disponibles**")
    st.markdown("---")
    st.markdown("Cliquez sur un domaine pour accéder aux CV stockés dans son dossier Google Drive.")

# ─── En-tête ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <div style="font-size: 2.5rem;">📂</div>
    <h1 style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.5rem;">
        CV des <span style="color: #00e5ff;">Experts</span>
    </h1>
    <p style="color: #7fa8c9; max-width: 600px; margin: 0 auto;">
        Sélectionnez votre domaine pour consulter l’ensemble des Curriculum Vitae.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── 14 boutons de spécialité (2 lignes de 7) ──────────────────────────────────
if "selected_specialty" not in st.session_state:
    st.session_state.selected_specialty = list(SPECIALTY_DRIVE_FOLDERS.keys())[0]

# Affichage des boutons
specialties = list(SPECIALTY_DRIVE_FOLDERS.keys())
cols = st.columns(7)
for idx, spec in enumerate(specialties):
    col = cols[idx % 7]
    icon = SPECIALTY_ICONS.get(spec, "📂")
    # Style actif si c'est la spécialité sélectionnée
    if st.session_state.selected_specialty == spec:
        btn = col.button(f"{icon} {spec}", key=f"btn_{spec}", use_container_width=True, type="primary")
    else:
        btn = col.button(f"{icon} {spec}", key=f"btn_{spec}", use_container_width=True, type="secondary")
    if btn:
        st.session_state.selected_specialty = spec
        st.rerun()

# ─── Affichage du dossier correspondant ────────────────────────────────────────
selected = st.session_state.selected_specialty
drive_url = SPECIALTY_DRIVE_FOLDERS[selected]
icon = SPECIALTY_ICONS.get(selected, "📂")

st.markdown(f"""
<div class="folder-card">
    <div class="folder-icon">{icon}</div>
    <div class="folder-title">{selected}</div>
    <div class="folder-sub">Dossier Google Drive · CV des spécialistes</div>
    <a href="{drive_url}" target="_blank" class="drive-link">📁 Ouvrir le dossier CV</a>
</div>
""", unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⚛ AnnotaCore · Accès direct aux CV par spécialité</span>
    <span>—</span>
    <span>Liens mis à jour le 08/04/2026</span>
</div>
""", unsafe_allow_html=True)
