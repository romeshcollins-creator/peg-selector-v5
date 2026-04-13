import streamlit as st
import pandas as pd

# -----------------------------
# App configuration
# -----------------------------
st.set_page_config(
    page_title="PEG Selector — Interactive Prototype",
    layout="wide"
)

st.title("PEG Selector — Interactive Prototype")
st.write("Select PEG properties to filter products.")

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("peg_products_v2.csv")
df.columns = df.columns.str.strip()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filter PEG Properties")

# Molecular Weight range
mw_min = int(df["Molecular Weight (kDa)"].min())
mw_max = int(df["Molecular Weight (kDa)"].max())

# -----------------------------
# Initialize session state
# -----------------------------
if "mw_range" not in st.session_state:
    st.session_state.mw_range = (mw_min, mw_max)

if "selected_fg" not in st.session_state:
    st.session_state.selected_fg = []

if "selected_arch" not in st.session_state:
    st.session_state.selected_arch = []

if "selected_app" not in st.session_state:
    st.session_state.selected_app = []

if "selected_sol" not in st.session_state:
    st.session_state.selected_sol = []

if "selected_partner" not in st.session_state:
    st.session_state.selected_partner = []

# -----------------------------
# Reset button
# -----------------------------
if st.sidebar.button("Reset Filters"):
    st.session_state.mw_range = (mw_min, mw_max)
    st.session_state.selected_fg = []
    st.session_state.selected_arch = []
    st.session_state.selected_app = []
    st.session_state.selected_sol = []
    st.session_state.selected_partner = []

# -----------------------------
# Sidebar inputs
# -----------------------------
mw_range = st.sidebar.slider(
    "Molecular Weight (kDa)",
    min_value=mw_min,
    max_value=mw_max,
    value=st.session_state.mw_range,
    key="mw_range"
)

selected_fg = st.sidebar.multiselect(
    "Functional Group / Reactivity",
    sorted(df["Functional Group / Reactivity"].dropna().unique()),
    default=st.session_state.selected_fg,
    key="selected_fg"
)

selected_arch = st.sidebar.multiselect(
    "Polymer Architecture",
    sorted(df["Polymer Architecture"].dropna().unique()),
    default=st.session_state.selected_arch,
    key="selected_arch"
)

selected_app = st.sidebar.multiselect(
    "Intended Application",
    sorted(df["Intended Application"].dropna().unique()),
    default=st.session_state.selected_app,
    key="selected_app"
)

selected_sol = st.sidebar.multiselect(
    "Solubility",
    sorted(df["Solubility"].dropna().unique()),
    default=st.session_state.selected_sol,
    key="selected_sol"
)

selected_partner = st.sidebar.multiselect(
    "Commercial Partner",
    sorted(df["Commercial Partner"].dropna().unique()),
    default=st.session_state.selected_partner,
    key="selected_partner"
)

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df[
    (df["Molecular Weight (kDa)"].between(*mw_range)) &
    ((df["Functional Group / Reactivity"].isin(selected_fg)) if selected_fg else True) &
    ((df["Polymer Architecture"].isin(selected_arch)) if selected_arch else True) &
    ((df["Intended Application"].isin(selected_app)) if selected_app else True) &
    ((df["Solubility"].isin(selected_sol)) if selected_sol else True) &
    ((df["Commercial Partner"].isin(selected_partner)) if selected_partner else True)
]

st.subheader(f"Filtered Results ({len(filtered_df)} PEGs)")

# -----------------------------
# Display results
# -----------------------------
for _, row in filtered_df.iterrows():
    with st.expander(row["Product Name"]):

        st.markdown(
            f"**MW (kDa):** {row['Molecular Weight (kDa)']} &nbsp;|&nbsp; "
            f"**Functional Group:** {row['Functional Group / Reactivity']} &nbsp;|&nbsp; "
            f"**Architecture:** {row['Polymer Architecture']}"
        )

        st.markdown(
            f"**Application:** {row['Intended Application']} &nbsp;|&nbsp; "
            f"**PDI:** {row['Polydispersity Index (PDI)']} &nbsp;|&nbsp; "
            f"**Solubility:** {row['Solubility']}"
        )

        st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
        st.markdown(f"🔗 [Vendor Product Page]({row['Product Page']})")