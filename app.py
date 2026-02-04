import time
import random
import pandas as pd
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Magic 3 Ball — Fun Teaching Ideas",
    page_icon="✨",  # removed magic 8 ball vibe
    layout="wide",
)


# -----------------------------
# Constants / Links
# -----------------------------
SHEET_ID = "1bFxAg0LqkC22Uc8FQxWoTNtJ8k-GBDy715E6YHy8r3I"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1bFxAg0LqkC22Uc8FQxWoTNtJ8k-GBDy715E6YHy8r3I/edit?usp=sharing"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

ENG_UNLEASHED_URL = "https://engineeringunleashed.com/card/36"
TEAM_CRESCENDO_URL = "https://docs.google.com/document/d/1SXUH7tqaHU8ixkpBiJlWOCNtG9jXeYC5198PSwxWrQY/edit?usp=sharing"


# -----------------------------
# Styling (simple, modern, readable)
# -----------------------------
st.markdown(
    """
<style>
/* Layout */
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

/* Centered big button container */
.cta-wrap {
  display: flex;
  justify-content: center;
  margin: 0.25rem 0 0.25rem 0;
}

/* Make the Streamlit button visually prominent */
div.stButton > button {
  width: min(680px, 100%);
  padding: 1.1rem 1.25rem;
  font-size: 1.15rem;
  font-weight: 650;
  border-radius: 16px;
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

    if df.shape[1] < 2:
        raise ValueError("Sheet must have at least 2 columns (name, concept).")

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
  <h1>Magic 3 Ball of Fun Teaching Ideas</h1>
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
    df = load_ac_
