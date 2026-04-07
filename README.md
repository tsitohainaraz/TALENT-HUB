# ✦ TalentHub — Team Profile Directory

A beautiful, professional Streamlit web app for showcasing your team's CVs to clients. Features real-time availability, smart scheduling, Google Drive CV downloads, and a secure admin panel.

---

## 🚀 Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

**Default admin password:** `admin2024`  
*(Change this before deploying — see below)*

---

## ☁️ Deploy to Streamlit Cloud (Free Hosting)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial TalentHub app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/talenthub.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Click **Advanced settings → Secrets** and add:

```toml
ADMIN_PASSWORD = "your_very_secure_password"
```

6. Click **Deploy** — your app will be live in ~2 minutes with a public URL.

---

## 🔧 How to Use

### For Clients (Visitors)
- Browse all team profiles in a beautiful card grid
- Filter by **availability**, **specialty**, **education level**, or **gender**
- Click **⬇ Download CV** on any profile to get the PDF from Google Drive

### For Admins
1. Click **Login** in the sidebar, enter the admin password
2. Each card now shows an **⚙️ Edit Profile** expander:
   - Change **Open / Occupied** status instantly
   - Set a **scheduled availability date** — the app automatically shows "Occupied" until that date, then switches to "Open"
   - Update the **Google Drive CV link**
3. Scroll down to **➕ Add New Profile** to add a new team member

---

## 📁 Google Drive CV Links

For each profile, paste the **Google Drive sharing link** in the format:
```
https://drive.google.com/file/d/FILE_ID/view
```

The app automatically converts this to a direct download link for clients.

**To get a shareable link:**
1. Upload the PDF to Google Drive
2. Right-click → **Share** → **Anyone with the link can view**
3. Copy the link and paste it into the profile's Drive Link field

---

## 📋 Data Storage

Profiles are stored in `data/profiles.json`. On Streamlit Cloud, this file persists within your deployment session but **resets on redeployment**.

### For Permanent Storage (Recommended for Production)
Consider using one of these options:
- **Streamlit Community Cloud + GitHub**: Commit `data/profiles.json` to your repo and push changes via the admin panel using the GitHub API
- **Supabase** (free PostgreSQL): Replace the JSON read/write functions with Supabase client calls
- **Google Sheets**: Use `gspread` to read/write profiles from a Google Sheet

---

## 🗂️ File Structure

```
talenthub/
├── app.py                  # Main application
├── style.css               # All styling
├── requirements.txt        # Python dependencies
├── data/
│   └── profiles.json       # Auto-generated profile data
└── .streamlit/
    ├── config.toml         # Theme configuration
    └── secrets.toml.template  # Secrets template
```

---

## ⚙️ Customization

- **Colors / fonts**: Edit `style.css` — all colors are CSS variables at the top
- **Admin password**: Set `ADMIN_PASSWORD` in Streamlit secrets or as an environment variable
- **App title / branding**: Change "TalentHub" in `app.py` header and `style.css` `.logo-text`
- **Default profiles**: Edit the `default` list in `load_profiles()` in `app.py`

---

## 📱 Mobile Support

The app is fully responsive. Cards stack vertically on mobile, and the sidebar collapses automatically.
