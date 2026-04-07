import streamlit as st
import json
import os
from pathlib import Path
from datetime import date

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnnotaCore — CV par Spécialité",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Spécialités et icônes ────────────────────────────────────────────────────
SPECIALTIES = [
    "Astronomie", "Chimie", "Droit", "Génie des matériaux",
    "Génie Electrique", "Histoire", "Mathématiques", "Neurosciences",
    "Philosophie", "Physique", "Psychologie", "Sciences de l'information",
    "Sciences de la Terre", "Sciences du vivant"
]

SPECIALTY_ICONS = {
    "Astronomie": "🔭", "Chimie": "⚗️", "Droit": "⚖️",
    "Génie des matériaux": "🧱", "Génie Electrique": "⚡", "Histoire": "📜",
    "Mathématiques": "∑", "Neurosciences": "🧠", "Philosophie": "💡",
    "Physique": "⚛️", "Psychologie": "🧘", "Sciences de l'information": "💻",
    "Sciences de la Terre": "🌍", "Sciences du vivant": "🧬",
}

# ─── Fichier de données pour les CV ───────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
CV_FILE = DATA_DIR / "cvs.json"

def load_cvs():
    """Charge la liste des CV depuis le fichier JSON."""
    if not CV_FILE.exists():
        # Données d'exemple (liens PDF factices)
        default_cvs = [
            {"id": 1, "title": "CV - Dr. Amara Diallo", "specialty": "Physique",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Spécialiste en physique des particules."},
            {"id": 2, "title": "CV - Marcus Chen", "specialty": "Neurosciences",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Expert en neuroimagerie."},
            {"id": 3, "title": "CV - Fatou Ndiaye", "specialty": "Astronomie",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Astronome spécialisée en analyse spectrale."},
            {"id": 4, "title": "CV - Dr. Ibrahim Koné", "specialty": "Génie Electrique",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Ingénieur en simulation de circuits."},
            {"id": 5, "title": "CV - Léa Fontaine", "specialty": "Chimie",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Chimiste computationnelle."},
            {"id": 6, "title": "CV - Dr. Youssouf Barry", "specialty": "Mathématiques",
             "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
             "description": "Mathématicien expert en calcul symbolique."},
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

# ─── Session State ─────────────────────────────────────────────────────────────
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2024")

# ─── CSS Thème (inchangé, très stylé) ─────────────────────────────────────────
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

.spec-btn-active {
    background: linear-gradient(135deg, rgba(0,229,255,0.2), rgba(41,121,255,0.2));
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    box-shadow: var(--glow-cyan);
}

/* Cartes CV */
.cv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
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

.cv-icon {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
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
    cursor: pointer;
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
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">📄 AnnotaCore
            <span>CV par spécialité</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Administration")
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
        st.success("✅ Mode admin actif")
        if st.button("Déconnexion", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_mode = False
            st.rerun()

    st.markdown("---")
    st.markdown(f"**Total CV :** {len(load_cvs())}")

# ─── En-tête ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem;">
    <div style="font-size: 2.5rem;">📄</div>
    <h1 style="font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.5rem;">
        CV des <span style="color: #00e5ff;">Experts</span>
    </h1>
    <p style="color: #7fa8c9; max-width: 600px; margin: 0 auto;">
        Parcourez les Curriculum Vitae de nos spécialistes par domaine scientifique.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Sélection de la spécialité (14 boutons) ──────────────────────────────────
st.markdown('<div class="specialty-buttons">', unsafe_allow_html=True)
cols = st.columns(7)  # 2 lignes de 7
for idx, spec in enumerate(SPECIALTIES):
    col = cols[idx % 7]
    icon = SPECIALTY_ICONS.get(spec, "📂")
    # Utilisation de session state pour garder la spécialité sélectionnée
    if "selected_specialty" not in st.session_state:
        st.session_state.selected_specialty = SPECIALTIES[0]
    active = st.session_state.selected_specialty == spec
    btn_label = f"{icon} {spec}"
    if col.button(btn_label, key=f"spec_{spec}", use_container_width=True,
                  type="secondary" if not active else "primary"):
        st.session_state.selected_specialty = spec
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ─── Affichage des CV pour la spécialité sélectionnée ─────────────────────────
selected = st.session_state.selected_specialty
cvs = load_cvs()
filtered_cvs = [cv for cv in cvs if cv["specialty"] == selected]

st.markdown(f"## {SPECIALTY_ICONS.get(selected, '📁')} {selected}")
st.caption(f"{len(filtered_cvs)} CV disponible(s)")

if not filtered_cvs:
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">📭</div>
        <p>Aucun CV pour la spécialité <strong>{selected}</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Grille de CV
    cols = st.columns(2)
    for i, cv in enumerate(filtered_cvs):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="cv-card">
                    <div class="cv-icon">📄</div>
                    <div class="cv-title">{cv['title']}</div>
                    <div class="cv-desc">{cv.get('description', '')}</div>
                    <div class="cv-actions">
                        <a href="{cv['file_url']}" target="_blank" class="cv-button">📖 Ouvrir le PDF</a>
                """, unsafe_allow_html=True)
                if st.session_state.admin_mode:
                    if st.button("🗑 Supprimer", key=f"del_{cv['id']}", use_container_width=True):
                        new_cvs = [c for c in load_cvs() if c["id"] != cv["id"]]
                        save_cvs(new_cvs)
                        st.success("CV supprimé")
                        st.rerun()
                st.markdown("</div></div>", unsafe_allow_html=True)

# ─── Ajout de CV (mode admin) ─────────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("---")
    st.markdown("## ➕ Ajouter un CV")
    with st.form("add_cv_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Titre du CV *", placeholder="ex: CV - Dr. Jean Dupont")
            specialty = st.selectbox("Spécialité *", SPECIALTIES)
        with c2:
            file_url = st.text_input("Lien vers le PDF *", placeholder="https://...")
            description = st.text_area("Description (optionnelle)", height=80)
        submitted = st.form_submit_button("📄 Ajouter ce CV", use_container_width=True)
        if submitted:
            if not title or not specialty or not file_url:
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                all_cvs = load_cvs()
                new_id = get_next_id(all_cvs)
                all_cvs.append({
                    "id": new_id,
                    "title": title,
                    "specialty": specialty,
                    "file_url": file_url,
                    "description": description
                })
                save_cvs(all_cvs)
                st.success(f"CV « {title} » ajouté avec succès !")
                st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>⚛ AnnotaCore · CV par spécialité</span>
    <span>—</span>
    <span>Données mises à jour en temps réel</span>
</div>
""", unsafe_allow_html=True)
