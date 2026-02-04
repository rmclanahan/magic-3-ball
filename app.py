import time
import random
import pandas as pd
import streamlit as st


# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Magic 3 Ball — Fun Teaching Ideas",
    page_icon="✨",
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
.block-container { padding-top: 2.2rem; max-width: 1100px; }

.hero {
  padding: 1.25rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  margin-bottom: 1.2rem;
}
.hero h1 { margin: 0 0 0.4rem 0; font-size: 2.1rem; }
.hero p  { margin: 0; opacity: 0.85; font-size: 1.05rem; }

.cta-wrap {
  display: flex;
  justify-content: center;
  margin: 0.5rem 0;
}

div.stButton > button {
  width: min(680px, 100%);
  padding: 1.15rem;
  font-size: 1.15rem;
  font-weight: 650;
  border-radius: 16px;
}

.card {
  border-radius: 18px;
  padding: 1.1rem;
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
}
.card h3 { margin: 0.2rem 0 0.55rem 0; font-size: 1.22rem; }
.card p  { margin: 0; line-height: 1.45; }

.footer {
  margin-top: 1.4rem;
  padding: 1rem;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.02);
}
.footer-title {
  font-weight: 600;
  margin-bottom: 0.75rem;
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
        raise ValueError("Sheet must have at least two columns.")

    df = df.iloc[:, :2]
    df.columns = ["name", "concept"]

    df = df[(df["name"].str.strip() != "") | (df["concept"].str.strip() != "")]
    df.reset_index(drop=True, inplace=True)

    if len(df) < 3:
        raise ValueError("Not enough activities in the sheet.")

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
  <p>Click once to get three engagement activities you can use right away.</p>
</div>
""",
    unsafe_allow_html=True,
)

# Safe load with proper try/except
df = None
try:
    df = load_activities(SHEET_CSV_URL)
except Exception:
    st.error(
        "I couldn’t load the activity list right now. "
        "Please refresh the page or open the full sheet below."
    )

# Centered CTA
st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
clicked = st.button("✨ Ask the Magic 3 Ball", disabled=(df is None))
st.markdown("</div>", unsafe_allow_html=True)

st.caption("Click again for a fresh set of three ideas.")
st.divider()

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
            col.markdown(
                f"""
<div class="card">
  <div class="badge">#{n} of {len(df)}</div>
  <h3>{row["name"] or "Untitled activity"}</h3>
  <p>{row["concept"] or "No description provided."}</p>
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("Click **Ask the Magic 3 Ball** to get your first three ideas.")

# Footer
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
    st.link_button("View the full list (Google Sheet)", SHEET_URL, use_container_width=True)
with l2:
    st.link_button("Methodology (Engineering Unleashed)", ENG_UNLEASHED_URL, use_container_width=True)
with l3:
    st.link_button("Request Team Crescendo faculty development", TEAM_CRESCENDO_URL, use_container_width=True)
