import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
from pathlib import Path
import base64

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentHub — Team Profiles",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load CSS ──────────────────────────────────────────────────────────────────
def load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ─── Data Helpers ──────────────────────────────────────────────────────────────
DATA_FILE = Path(__file__).parent / "data" / "profiles.json"

def load_profiles():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        default = [
            {
                "id": 1, "name": "Dr. Sarah Okonkwo", "specialty": "Psychology",
                "education": "PhD", "gender": "Female",
                "manual_status": "Open", "scheduled_date": None,
                "gdrive_link": "https://drive.google.com/file/d/example1/view",
                "bio": "Specialist in cognitive behavioral therapy and organizational psychology.",
                "photo_initial": "SO"
            },
            {
                "id": 2, "name": "Marcus Dubois", "specialty": "History",
                "education": "Master", "gender": "Male",
                "manual_status": "Occupied", "scheduled_date": "2026-05-04",
                "gdrive_link": "https://drive.google.com/file/d/example2/view",
                "bio": "Expert in modern European history and archival research methods.",
                "photo_initial": "MD"
            },
            {
                "id": 3, "name": "Amina Traoré", "specialty": "Sociology",
                "education": "PhD", "gender": "Female",
                "manual_status": "Open", "scheduled_date": None,
                "gdrive_link": "https://drive.google.com/file/d/example3/view",
                "bio": "Researcher focused on social structures and community development in Sub-Saharan Africa.",
                "photo_initial": "AT"
            },
            {
                "id": 4, "name": "James Whitfield", "specialty": "Economics",
                "education": "Bachelor", "gender": "Male",
                "manual_status": "Occupied", "scheduled_date": None,
                "gdrive_link": "https://drive.google.com/file/d/example4/view",
                "bio": "Analyst specializing in macroeconomic modeling and policy evaluation.",
                "photo_initial": "JW"
            },
            {
                "id": 5, "name": "Layla Haddad", "specialty": "Political Science",
                "education": "Master", "gender": "Female",
                "manual_status": "Open", "scheduled_date": None,
                "gdrive_link": "https://drive.google.com/file/d/example5/view",
                "bio": "Specialist in Middle Eastern politics and international relations.",
                "photo_initial": "LH"
            },
            {
                "id": 6, "name": "Chen Wei", "specialty": "Anthropology",
                "education": "PhD", "gender": "Male",
                "manual_status": "Occupied", "scheduled_date": "2026-06-01",
                "gdrive_link": "https://drive.google.com/file/d/example6/view",
                "bio": "Cultural anthropologist with fieldwork experience across Southeast Asia.",
                "photo_initial": "CW"
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
            return "Occupied", f"Available after {scheduled.strftime('%d/%m/%Y')}"
        else:
            return "Open", "Available"
    status = profile.get("manual_status", "Open")
    return status, "Available" if status == "Open" else "Occupied"

def get_next_id(profiles):
    return max((p["id"] for p in profiles), default=0) + 1

# ─── Session State ─────────────────────────────────────────────────────────────
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2024")

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">✦</span>
        <span class="logo-text">TalentHub</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-subtitle">Find the right expert for your project</p>', unsafe_allow_html=True)
    st.markdown("---")

    # ── Filters ──
    st.markdown('<p class="filter-label">🔍 FILTERS</p>', unsafe_allow_html=True)

    profiles_all = load_profiles()
    specialties = sorted(set(p["specialty"] for p in profiles_all))
    educations = ["Bachelor", "Master", "PhD"]

    filter_status = st.selectbox("Availability", ["All", "Open", "Occupied"])
    filter_specialty = st.multiselect("Specialty", specialties, placeholder="All specialties")
    filter_education = st.multiselect("Education Level", educations, placeholder="All levels")
    filter_gender = st.selectbox("Gender", ["All", "Female", "Male"])

    st.markdown("---")

    # ── Admin Login ──
    st.markdown('<p class="filter-label">⚙️ ADMIN</p>', unsafe_allow_html=True)
    if not st.session_state.admin_authenticated:
        pwd = st.text_input("Admin Password", type="password", placeholder="Enter password")
        if st.button("Login", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.admin_mode = True
                st.rerun()
            else:
                st.error("Incorrect password")
    else:
        st.success("✓ Admin mode active")
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_mode = False
            st.rerun()

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-tag">TEAM DIRECTORY</div>
    <h1 class="hero-title">Our Expert Talent Pool</h1>
    <p class="hero-sub">Browse, filter, and connect with our specialists. Download their CVs and check real-time availability.</p>
</div>
""", unsafe_allow_html=True)

# ─── Load & Filter ─────────────────────────────────────────────────────────────
profiles = load_profiles()

# Apply scheduled date logic
for p in profiles:
    eff_status, eff_label = get_effective_status(p)
    p["_effective_status"] = eff_status
    p["_status_label"] = eff_label

# Apply filters
filtered = profiles
if filter_status != "All":
    filtered = [p for p in filtered if p["_effective_status"] == filter_status]
if filter_specialty:
    filtered = [p for p in filtered if p["specialty"] in filter_specialty]
if filter_education:
    filtered = [p for p in filtered if p["education"] in filter_education]
if filter_gender != "All":
    filtered = [p for p in filtered if p["gender"] == filter_gender]

# ─── Stats Bar ─────────────────────────────────────────────────────────────────
total = len(profiles)
open_count = sum(1 for p in profiles if p["_effective_status"] == "Open")
occupied_count = total - open_count

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item">
        <span class="stat-number">{total}</span>
        <span class="stat-label">Total Experts</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number open-num">{open_count}</span>
        <span class="stat-label">Available Now</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number occ-num">{occupied_count}</span>
        <span class="stat-label">Currently Engaged</span>
    </div>
    <div class="stat-divider"></div>
    <div class="stat-item">
        <span class="stat-number">{len(filtered)}</span>
        <span class="stat-label">Showing</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Profile Cards ─────────────────────────────────────────────────────────────
if not filtered:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔎</div>
        <p>No profiles match your current filters.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # 3-column grid
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
                        sched_note = f'<div class="sched-note">🗓 Available after {sched.strftime("%d/%m/%Y")}</div>'

                edu_icons = {"Bachelor": "🎓", "Master": "📚", "PhD": "🏛️"}
                edu_icon = edu_icons.get(profile["education"], "🎓")
                gender_icon = "♀" if profile["gender"] == "Female" else "♂"

                initials = profile.get("photo_initial", profile["name"][:2].upper())

                card_html = f"""
                <div class="profile-card">
                    <div class="card-header">
                        <div class="avatar avatar-{status_class}">{initials}</div>
                        <div class="card-meta">
                            <h3 class="card-name">{profile['name']}</h3>
                            <p class="card-specialty">{profile['specialty']}</p>
                        </div>
                    </div>
                    <div class="card-tags">
                        <span class="tag tag-edu">{edu_icon} {profile['education']}</span>
                        <span class="tag tag-gender">{gender_icon} {profile['gender']}</span>
                    </div>
                    <p class="card-bio">{profile.get('bio', '')}</p>
                    {sched_note}
                    <div class="status-badge status-{status_class}">{eff_status}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

                # Download button
                gdrive = profile.get("gdrive_link", "")
                if gdrive and "example" not in gdrive:
                    # Convert view link to direct download
                    if "/view" in gdrive:
                        file_id = gdrive.split("/d/")[1].split("/")[0] if "/d/" in gdrive else ""
                        if file_id:
                            dl_link = f"https://drive.google.com/uc?export=download&id={file_id}"
                        else:
                            dl_link = gdrive
                    else:
                        dl_link = gdrive
                    st.markdown(f"""
                    <a href="{dl_link}" target="_blank" class="dl-button">
                        ⬇ Download CV
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="dl-button-disabled">CV not uploaded yet</div>', unsafe_allow_html=True)

                # Admin Controls
                if st.session_state.admin_mode:
                    with st.expander("⚙️ Edit Profile", expanded=False):
                        pid = profile["id"]

                        new_status = st.selectbox(
                            "Status", ["Open", "Occupied"],
                            index=0 if profile["manual_status"] == "Open" else 1,
                            key=f"status_{pid}"
                        )

                        sched_val = None
                        if profile.get("scheduled_date"):
                            sched_val = datetime.strptime(profile["scheduled_date"], "%Y-%m-%d").date()

                        new_date = st.date_input(
                            "Available after (optional)",
                            value=sched_val,
                            min_value=date.today(),
                            key=f"date_{pid}",
                            help="Set a future date; profile shows as Occupied until then."
                        )
                        clear_date = st.checkbox("Clear scheduled date", key=f"clear_{pid}")

                        new_link = st.text_input(
                            "Google Drive Link",
                            value=profile.get("gdrive_link", ""),
                            key=f"link_{pid}",
                            placeholder="https://drive.google.com/file/d/..."
                        )

                        if st.button("💾 Save", key=f"save_{pid}", use_container_width=True):
                            all_profiles = load_profiles()
                            for p in all_profiles:
                                if p["id"] == pid:
                                    p["manual_status"] = new_status
                                    p["gdrive_link"] = new_link
                                    if clear_date:
                                        p["scheduled_date"] = None
                                    elif new_date:
                                        p["scheduled_date"] = new_date.strftime("%Y-%m-%d")
                            save_profiles(all_profiles)
                            st.success("Saved!")
                            st.rerun()

# ─── Admin: Add New Profile ────────────────────────────────────────────────────
if st.session_state.admin_mode:
    st.markdown("---")
    st.markdown('<h2 class="section-title">➕ Add New Profile</h2>', unsafe_allow_html=True)

    with st.form("add_profile_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("Full Name *", placeholder="e.g. Dr. Jane Smith")
            new_specialty = st.text_input("Specialty *", placeholder="e.g. Psychology")
            new_bio = st.text_area("Short Bio", placeholder="Brief description of expertise…", height=80)
        with c2:
            new_education = st.selectbox("Education Level *", ["Bachelor", "Master", "PhD"])
            new_gender = st.selectbox("Gender *", ["Female", "Male"])
            new_link = st.text_input("Google Drive CV Link", placeholder="https://drive.google.com/file/d/…")

        c3, c4 = st.columns(2)
        with c3:
            new_status = st.selectbox("Initial Status", ["Open", "Occupied"])
        with c4:
            new_avail_date = st.date_input("Scheduled availability date (optional)", value=None, min_value=date.today())

        submitted = st.form_submit_button("✦ Add Profile", use_container_width=True)
        if submitted:
            if not new_name or not new_specialty:
                st.error("Name and Specialty are required.")
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
                    "gdrive_link": new_link,
                    "bio": new_bio,
                    "photo_initial": initials,
                }
                all_p.append(new_profile)
                save_profiles(all_p)
                st.success(f"✓ Profile for **{new_name}** added successfully!")
                st.rerun()

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>✦ TalentHub</span>
    <span>·</span>
    <span>Professional Talent Directory</span>
    <span>·</span>
    <span>All profiles updated in real-time</span>
</div>
""", unsafe_allow_html=True)
