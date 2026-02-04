import time
import random
import pandas as pd
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Magic 3 Ball — Fun Teaching Ideas",
    page_icon="🔮",
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
# Styling
# -----------------------------
st.markdown(
    """
<style>
/* Page width/padding */
.block-container { padding-top: 2.2rem; max-width: 1120px; }

/* Hero */
.hero {
  padding: 1.25rem 1.35rem 1.1rem 1.35rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  margin-bottom: 1.1rem;
}
.hero h1 { margin: 0 0 0.45rem 0; font-size: 2.15rem; }
.hero p  { margin: 0; opacity: 0.86; font-size: 1.05rem; line-height: 1.45; }

/* Centered CTA */
.cta-wrap { display: flex; justify-content: center; margin: 0.6rem 0 0.3rem 0; }

/* Big main button */
div.stButton > button {
  width: min(720px, 100%);
  padding: 1.15rem 1.25rem;
  font-size: 1.18rem;
  font-weight: 700;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.18);
}

/* Cards for the 3 ideas */
.card {
  border-radius: 18px;
  padding: 1.1rem 1.1rem 1.05rem 1.1rem;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  box-shadow: 0 6px 18px rgba(0,0,0,0.18);
  height: 100%;
}
.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  margin-bottom: 0.6rem;
  border: 1px solid rgba(255,255,255,0.16);
  opacity: 0.92;
}
.card h3 { margin: 0.2rem 0 0.55rem 0; font-size: 1.22rem; line-height: 1.25; }
.card p  { margin: 0; line-height: 1.45; opacity: 0.93; }

/* Resources panel that "pops" */
.resources {
  margin-top: 1.35rem;
  padding: 1.05rem 1.1rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.12);
  background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
  box-shadow: 0 10px 26px rgba(0,0,0,0.16);
}
.resources-top {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
}
.resources-title {
  font-weight: 750;
  font-size: 1.05rem;
  letter-spacing: 0.2px;
}
.resources-hint {
  opacity: 0.75;
  font-size: 0.92rem;
}

/* Make link_buttons feel more like "chips/cards" */
div[data-testid="stLinkButton"] a {
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  padding: 0.95rem 1rem !important;
  font-weight: 650 !important;
  text-align: center !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Data loading (cached)
# -----------------------------
@st.cache_data(ttl=60 * 30)
def load_activities(csv_url: str) -> pd.DataFrame:
    df = pd.read_csv(csv_url, header=None, dtype=str, keep_default_na=False)

    if df.shape[1] < 2:
        raise ValueError("Sheet must have at least two columns (name, concept).")

    df = df.iloc[:, :2].copy()
    df.columns = ["name", "concept"]

    df = df[(df["name"].str.strip() != "") | (df["concept"].str.strip() != "")]
    df.reset_index(drop=True, inplace=True)

    if len(df) < 3:
        raise ValueError("Need at least 3 activities to draw from.")

    return df


def draw_three(n: int) -> list[int]:
    return sorted(random.sample(range(1, n + 1), 3))


# -----------------------------
# UI
# -----------------------------
st.markdown(
    """
<div class="hero">
  <h1>Magic 3 Ball of Fun Teaching Ideas</h1>
  <p>Click once to get <b>three</b> engagement activities—fast, playful, and ready to use.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Load data with friendly fallback
df = None
try:
    df = load_activities(SHEET_CSV_URL)
except Exception:
    st.error(
        "I couldn’t load the activity list right now. Please refresh and try again.\n\n"
        "If it keeps happening, use the link below to open the full sheet."
    )

# Centered main CTA
st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
clicked = st.button("✨ Ask the Magic 3 Ball", disabled=(df is None))
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Tip: click again for a fresh set of three ideas.")
st.divider()

# Results
if df is not None:
    if "last_draw" not in st.session_state:
        st.session_state.last_draw = None

    if clicked:
        with st.spinner("Choosing your ideas..."):
            time.sleep(0.6)
        st.session_state.last_draw = draw_three(len(df))

    if st.session_state.last_draw:
        cols = st.columns(3)
        for col, n in zip(cols, st.session_state.last_draw):
            row = df.iloc[n - 1]
            name = str(row["name"]).strip()
            concept = str(row["concept"]).strip()

            col.markdown(
                f"""
<div class="card">
  <div class="badge">#{n} of {len(df)}</div>
  <h3>{name if name else "Untitled activity"}</h3>
  <p>{concept if concept else "No description provided."}</p>
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("Click **Ask the Magic 3 Ball** to get your first three ideas.")

# References / Resources panel that pops
st.markdown(
    """
<div class="resources">
  <div class="resources-top">
    <div class="resources-title">Resources</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

r1, r2, r3 = st.columns(3)
with r1:
    st.link_button("Full list (Google Sheet)", SHEET_URL, use_container_width=True)
with r2:
    st.link_button("Methodology (Engineering Unleashed)", ENG_UNLEASHED_URL, use_container_width=True)
with r3:
    st.link_button("Team Crescendo (Complimentary on-campus faculty development)", TEAM_CRESCENDO_URL, use_container_width=True)
