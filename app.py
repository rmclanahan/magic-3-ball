import time
import random
import pandas as pd
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Magic 3 Ball — Fun Teaching Ideas",
    page_icon="🎱",
    layout="wide",
)


# -----------------------------
# Constants / Links
# -----------------------------
SHEET_ID = "1bFxAg0LqkC22Uc8FQxWoTNtJ8k-GBDy715E6YHy8r3I"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1bFxAg0LqkC22Uc8FQxWoTNtJ8k-GBDy715E6YHy8r3I/edit?usp=sharing"
# Public CSV export of the *first sheet/tab*. If you later need a specific tab, we can add gid=...
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

ENG_UNLEASHED_URL = "https://engineeringunleashed.com/card/36"
TEAM_CRESCENDO_URL = "https://docs.google.com/document/d/1SXUH7tqaHU8ixkpBiJlWOCNtG9jXeYC5198PSwxWrQY/edit?usp=sharing"


# -----------------------------
# Styling (simple, modern, readable)
# -----------------------------
st.markdown(
    """
<style>
/* Tighten the top padding a bit */
.block-container { padding-top: 2.2rem; max-width: 1100px; }

/* Hero */
.hero {
  padding: 1.25rem 1.25rem 1rem 1.25rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  margin-bottom: 1.2rem;
}
.hero h1 { margin: 0 0 0.35rem 0; font-size: 2.1rem; }
.hero p  { margin: 0; opacity: 0.85; font-size: 1.05rem; line-height: 1.45; }

/* Big button */
div.stButton > button {
  width: 100%;
  padding: 0.95rem 1rem;
  font-size: 1.05rem;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.18);
}

/* Cards */
.card {
  border-radius: 18px;
  padding: 1.05rem 1.1rem;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  box-shadow: 0 6px 18px rgba(0,0,0,0.18);
  height: 100%;
}
.badge {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  font-size: 0.82rem;
  border: 1px solid rgba(255,255,255,0.16);
  opacity: 0.9;
  margin-bottom: 0.55rem;
}
.card h3 {
  margin: 0.2rem 0 0.55rem 0;
  font-size: 1.22rem;
  line-height: 1.25;
}
.card p {
  margin: 0;
  opacity: 0.92;
  line-height: 1.45;
  font-size: 1.0rem;
}

/* Footer links area */
.footer {
  margin-top: 1.3rem;
  padding: 1rem 1.1rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.02);
}
.footer-title {
  font-weight: 600;
  margin-bottom: 0.75rem;
  opacity: 0.92;
}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Data loading (cached)
# -----------------------------
@st.cache_data(ttl=60 * 30)  # refresh every 30 minutes
def load_activities(csv_url: str) -> pd.DataFrame:
    """
    Loads the public Google Sheet as CSV.
    Sheet has NO header row:
      col 0 = activity name
      col 1 = concept (1–2 sentences)
    """
    df = pd.read_csv(csv_url, header=None, dtype=str, keep_default_na=False)
    # Ensure at least 2 columns
    if df.shape[1] < 2:
        raise ValueError("Sheet must have at least 2 columns (name, concept).")
    # Keep only first two columns in case there are extras
    df = df.iloc[:, :2].copy()
    df.columns = ["name", "concept"]

    # Drop completely empty rows (just in case)
    df = df[(df["name"].str.strip() != "") | (df["concept"].str.strip() != "")]
    df = df.reset_index(drop=True)

    if len(df) == 0:
        raise ValueError("Sheet appears empty.")
    return df


def draw_three(n: int) -> list[int]:
    """Returns 3 unique 1-based indices from 1..n."""
    if n < 3:
        raise ValueError("Need at least 3 activities to draw from.")
    return sorted(random.sample(range(1, n + 1), 3))


# -----------------------------
# App UI
# -----------------------------
st.markdown(
    """
<div class="hero">
  <h1>🎱 Magic 3 Ball of Fun Teaching Ideas</h1>
  <p>
    Click the button to get <b>three</b> engagement activities—fast, playful, and ready to use.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# Try to load data; show a friendly fallback if it fails
df = None
try:
    df = load_activities(SHEET_CSV_URL)
except Exception:
    st.error(
        "I couldn’t load the activity list right now. Please refresh and try again.\n\n"
        "If it keeps happening, open the full sheet using the link below."
    )

# Main interaction
colA, colB = st.columns([1.2, 1])
with colA:
    clicked = st.button("✨ Ask the Magic 3 Ball", disabled=(df is None))

with colB:
    st.caption("Tip: click again for a fresh set of 3 ideas.")

st.divider()

if df is not None:
    if "last_draw" not in st.session_state:
        st.session_state.last_draw = None

    if clicked:
        with st.spinner("Shaking the Magic 3 Ball..."):
            time.sleep(0.6)  # tiny “magic” pause
        st.session_state.last_draw = draw_three(len(df))

    if st.session_state.last_draw:
        nums = st.session_state.last_draw

        c1, c2, c3 = st.columns(3)
        cols = [c1, c2, c3]

        for i, n in enumerate(nums):
            row = df.iloc[n - 1]
            name = str(row["name"]).strip()
            concept = str(row["concept"]).strip()

            cols[i].markdown(
                f"""
<div class="card">
  <div class="badge">#{n} of {len(df)}</div>
  <h3>{name if name else "Untitled activity"}</h3>
  <p>{concept if concept else "No description provided in the sheet."}</p>
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("Click **Ask the Magic 3 Ball** to get your first 3 ideas.")

# Footer links
st.markdown(
    """
<div class="footer">
  <div class="footer-title">More resources</div>
</div>
""",
    unsafe_allow_html=True,
)

l1, l2, l3 = st.columns(3)
with l1:
    st.link_button("📚 View the full list (Google Sheet)", SHEET_URL, use_container_width=True)
with l2:
    st.link_button("🧠 Methodology (Engineering Unleashed)", ENG_UNLEASHED_URL, use_container_width=True)
with l3:
    st.link_button("🎓 Request Team Crescendo faculty development", TEAM_CRESCENDO_URL, use_container_width=True)
