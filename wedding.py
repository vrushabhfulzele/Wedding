import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Indian Wedding Analytics",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ----------------------------------------------------
       MAIN BACKGROUND
    ---------------------------------------------------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #fff0f6 45%,
            #f8f0ff 100%
        );
    }


    /* ----------------------------------------------------
       MAIN CONTENT
    ---------------------------------------------------- */

    .main {
        padding-top: 1rem;
    }


    /* ----------------------------------------------------
       HEADER
    ---------------------------------------------------- */

    .main-header {
        background: linear-gradient(
            135deg,
            #8e2de2,
            #c2185b,
            #ff4081
        );

        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;

        box-shadow:
            0px 8px 25px rgba(142, 45, 226, 0.25);

        margin-bottom: 25px;
    }


    .main-header h1 {
        font-size: 42px;
        margin-bottom: 8px;
        font-weight: 800;
    }


    .main-header p {
        font-size: 18px;
        margin: 0;
        opacity: 0.95;
    }


    /* ----------------------------------------------------
       SECTION HEADERS
    ---------------------------------------------------- */

    .section-header {
        background: linear-gradient(
            90deg,
            #8e2de2,
            #c2185b
        );

        color: white;

        padding: 12px 20px;

        border-radius: 12px;

        font-size: 22px;

        font-weight: 700;

        margin-top: 25px;
        margin-bottom: 18px;

        box-shadow:
            0px 4px 12px rgba(194, 24, 91, 0.18);
    }


    /* ----------------------------------------------------
       KPI CARDS
    ---------------------------------------------------- */

    .metric-card {

        padding: 20px;

        border-radius: 18px;

        background: white;

        text-align: center;

        min-height: 130px;

        box-shadow:
            0px 5px 18px rgba(0,0,0,0.08);

        border-left: 5px solid #c2185b;

        transition: transform 0.2s ease;
    }


    .metric-card:hover {
        transform: translateY(-4px);
    }


    .metric-icon {
        font-size: 30px;
    }


    .metric-title {
        font-size: 15px;
        color: #666;
        margin-top: 5px;
    }


    .metric-value {
        font-size: 25px;
        font-weight: 800;
        color: #8e2de2;
        margin-top: 5px;
    }


    /* ----------------------------------------------------
       FILTER CARD
    ---------------------------------------------------- */

    .filter-info {

        background: linear-gradient(
            135deg,
            #fff,
            #fff1f7
        );

        padding: 18px;

        border-radius: 15px;

        border: 1px solid #f3c4d8;

        box-shadow:
            0px 4px 12px rgba(0,0,0,0.05);

        margin-bottom: 15px;
    }


    /* ----------------------------------------------------
       SELECTION CARD
    ---------------------------------------------------- */

    .selection-card {

        background: linear-gradient(
            135deg,
            #8e2de2,
            #c2185b
        );

        color: white;

        padding: 20px;

        border-radius: 18px;

        box-shadow:
            0px 8px 20px rgba(142,45,226,0.20);

        margin-bottom: 20px;
    }


    .selection-card h3 {
        margin-top: 0;
    }


    /* ----------------------------------------------------
       INFO CARD
    ---------------------------------------------------- */

    .info-card {

        background: white;

        padding: 18px;

        border-radius: 15px;

        border: 1px solid #ead9f5;

        box-shadow:
            0px 4px 14px rgba(0,0,0,0.06);

        margin-bottom: 15px;
    }


    /* ----------------------------------------------------
       SIDEBAR
    ---------------------------------------------------- */

    [data-testid="stSidebar"] {

        background: linear-gradient(
            180deg,
            #2b123f 0%,
            #4a174f 45%,
            #6a1b4d 100%
        );
    }


    [data-testid="stSidebar"] * {
        color: white;
    }


    /* ----------------------------------------------------
       SELECTBOX
    ---------------------------------------------------- */

    div[data-baseweb="select"] > div {

        background-color: white !important;

        border-radius: 10px !important;

        border: 2px solid #d81b60 !important;
    }


    div[data-baseweb="select"] span {
        color: #333 !important;
    }


    /* ----------------------------------------------------
       BUTTONS
    ---------------------------------------------------- */

    .stButton > button {

        background: linear-gradient(
            90deg,
            #8e2de2,
            #c2185b
        );

        color: white;

        border: none;

        border-radius: 10px;

        padding: 8px 20px;

        font-weight: 600;
    }


    /* ----------------------------------------------------
       FOOTER
    ---------------------------------------------------- */

    .footer {

        text-align: center;

        padding: 20px;

        color: #777;

        font-size: 14px;

        margin-top: 30px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent

    possible_files = [
        BASE_DIR / "Datasets" / "Indian_Weddings_.csv",
        BASE_DIR / "Indian_Weddings_.csv",
        BASE_DIR / "data" / "Indian_Weddings_.csv",
        BASE_DIR / "dataset" / "Indian_Weddings_.csv"
    ]

    csv_file = None

    for file in possible_files:

        if file.exists():
            csv_file = file
            break

    if csv_file is None:

        st.error("❌ Indian_Weddings_.csv was not found.")

        st.write("Checked locations:")

        for file in possible_files:
            st.code(str(file))

        st.stop()

    return pd.read_csv(csv_file)


df = load_data()


# =========================================================
# REMOVE UNNECESSARY COLUMN
# =========================================================

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


# =========================================================
# RENAME COLUMNS
# =========================================================

rename_columns = {

    "Wedding/Type": "Wedding_Type",

    "Decor/Category": "Decor_Category",

    "Entertainment/Category": "Entertainment_Category",

    "Gifts/Category": "Giftstypes",

    "Cards/Category": "Cardstypes",

    "Cost/of/Type": "CostofType",

    "Clothes/Bride": "Bride_clothes",

    "Clothes/Groom": "Groom_clothes",

    "Gifts(per/piece)": "Gifts",

    "Invitations/Cards": "Invitations_Cards"
}

df = df.rename(columns=rename_columns)


# =========================================================
# CLEAN TEXT DATA
# =========================================================

text_columns = [
    "Wedding_Type",
    "Place",
    "Decor_Category",
    "Entertainment_Category",
    "Giftstypes",
    "Cardstypes"
]


for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace("/", "", regex=False)
            .str.strip()
        )

        df[column] = df[column].replace(
            ["nan", "None", ""],
            np.nan
        )


# =========================================================
# CLEAN NUMERIC DATA
# =========================================================

numeric_columns = [
    "CostofType",
    "Decor",
    "Entertainment",
    "Gifts",
    "Invitations_Cards"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace("e+", "", regex=False)
            .str.strip()
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-header">

    <h1>💍 Indian Wedding Analytics</h1>

    <p>
        Explore wedding costs, decoration, entertainment,
        gifts and invitation expenses
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "<h1 style='text-align:center;'>💍 Wedding Filters</h1>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# Wedding Type
wedding_types = sorted(
    df["Wedding_Type"]
    .dropna()
    .unique()
    .tolist()
)


selected_wedding = st.sidebar.selectbox(
    "💒 Wedding Type",
    ["All"] + wedding_types
)


filtered_df = df.copy()


if selected_wedding != "All":

    filtered_df = filtered_df[
        filtered_df["Wedding_Type"] == selected_wedding
    ]


# Place
places = sorted(
    filtered_df["Place"]
    .dropna()
    .unique()
    .tolist()
)


selected_place = st.sidebar.selectbox(
    "📍 Place",
    ["All"] + places
)


if selected_place != "All":

    filtered_df = filtered_df[
        filtered_df["Place"] == selected_place
    ]


# Decoration
decor_categories = sorted(
    filtered_df["Decor_Category"]
    .dropna()
    .unique()
    .tolist()
)


selected_decor = st.sidebar.selectbox(
    "🌸 Decoration",
    ["All"] + decor_categories
)


if selected_decor != "All":

    filtered_df = filtered_df[
        filtered_df["Decor_Category"] == selected_decor
    ]


# Sidebar information
st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <div class="filter-info">

    <b>📊 Current Records</b>

    <h2>{len(filtered_df)}</h2>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# ACTIVE FILTER DISPLAY
# =========================================================

st.markdown(
    '<div class="section-header">🎯 Current Selection</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="info-card">
        <b>💒 Wedding Type</b>
        <h3>{selected_wedding}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="info-card">
        <b>📍 Place</b>
        <h3>{selected_place}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="info-card">
        <b>🌸 Decoration</b>
        <h3>{selected_decor}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-header">📊 Key Wedding Metrics</div>',
    unsafe_allow_html=True
)


avg_wedding_cost = filtered_df["CostofType"].mean()

avg_decor_cost = filtered_df["Decor"].mean()

avg_entertainment_cost = filtered_df["Entertainment"].mean()

avg_gifts_cost = filtered_df["Gifts"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:

    value = (
        f"{avg_wedding_cost:,.2f}"
        if pd.notna(avg_wedding_cost)
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">💰</div>

            <div class="metric-title">
                Average Wedding Cost
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    value = (
        f"{avg_decor_cost:,.2f}"
        if pd.notna(avg_decor_cost)
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">🌸</div>

            <div class="metric-title">
                Average Decoration
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    value = (
        f"{avg_entertainment_cost:,.2f}"
        if pd.notna(avg_entertainment_cost)
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">🎵</div>

            <div class="metric-title">
                Average Entertainment
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    value = (
        f"{avg_gifts_cost:,.2f"
        if pd.notna(avg_gifts_cost)
        else "N/A"
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-icon">🎁</div>

            <div class="metric-title">
                Average Gifts
            </div>

            <div class="metric-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DATA PREVIEW
# =========================================================

st.markdown(
    '<div class="section-header">📋 Wedding Data</div>',
    unsafe_allow_html=True
)


with st.expander("🔍 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CHART 1 - WEDDING COST
# =========================================================

st.markdown(
    '<div class="section-header">💰 Wedding Cost Analysis</div>',
    unsafe_allow_html=True
)


wedding_cost = (
    df.groupby(
        "Wedding_Type",
        as_index=False
    )["CostofType"]
    .mean()
    .dropna()
    .sort_values(
        "CostofType",
        ascending=False
    )
)


fig1 = px.bar(
    wedding_cost,
    x="Wedding_Type",
    y="CostofType",
    text_auto=".2f",
    title="Average Wedding Cost by Wedding Type",
    color="CostofType",
    color_continuous_scale="Purples"
)


fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Wedding Type",
    yaxis_title="Average Cost",
    coloraxis_showscale=False
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================================================
# CHART 2 - PLACE
# =========================================================

st.markdown(
    '<div class="section-header">📍 Location Analysis</div>',
    unsafe_allow_html=True
)


place_cost = (
    df.groupby(
        "Place",
        as_index=False
    )["CostofType"]
    .mean()
    .dropna()
    .sort_values(
        "CostofType",
        ascending=False
    )
)


fig2 = px.bar(
    place_cost,
    x="Place",
    y="CostofType",
    text_auto=".2f",
    title="Average Wedding Cost by Place",
    color="CostofType",
    color_continuous_scale="RdPu"
)


fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Place",
    yaxis_title="Average Cost",
    coloraxis_showscale=False
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================================================
# TWO COLUMN ANALYSIS
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# DECORATION
# ---------------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-header">🌸 Decoration</div>',
        unsafe_allow_html=True
    )

    decor_cost = (
        filtered_df.groupby(
            "Decor_Category",
            as_index=False
        )["Decor"]
        .mean()
        .dropna()
        .sort_values(
            "Decor",
            ascending=False
        )
    )

    if not decor_cost.empty:

        fig3 = px.bar(
            decor_cost,
            x="Decor_Category",
            y="Decor",
            text_auto=".2f",
            color="Decor",
            color_continuous_scale="Pinkyl"
        )

        fig3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Average Cost",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )


# ---------------------------------------------------------
# ENTERTAINMENT
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-header">🎵 Entertainment</div>',
        unsafe_allow_html=True
    )

    entertainment_cost = (
        filtered_df.groupby(
            "Entertainment_Category",
            as_index=False
        )["Entertainment"]
        .mean()
        .dropna()
        .sort_values(
            "Entertainment",
            ascending=False
        )
    )

    if not entertainment_cost.empty:

        fig4 = px.bar(
            entertainment_cost,
            x="Entertainment_Category",
            y="Entertainment",
            text_auto=".2f",
            color="Entertainment",
            color_continuous_scale="Plasma"
        )

        fig4.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Average Cost",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )


# =========================================================
# GIFTS & INVITATIONS
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# GIFTS
# ---------------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-header">🎁 Gifts</div>',
        unsafe_allow_html=True
    )

    gift_cost = (
        filtered_df.groupby(
            "Giftstypes",
            as_index=False
        )["Gifts"]
        .mean()
        .dropna()
        .sort_values(
            "Gifts",
            ascending=False
        )
    )

    if not gift_cost.empty:

        fig5 = px.bar(
            gift_cost,
            x="Giftstypes",
            y="Gifts",
            text_auto=".2f",
            color="Gifts",
            color_continuous_scale="Oranges"
        )

        fig5.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Gift Type",
            yaxis_title="Average Cost",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )


# ---------------------------------------------------------
# INVITATIONS
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-header">💌 Invitations</div>',
        unsafe_allow_html=True
    )

    card_cost = (
        filtered_df.groupby(
            "Cardstypes",
            as_index=False
        )["Invitations_Cards"]
        .mean()
        .dropna()
        .sort_values(
            "Invitations_Cards",
            ascending=False
        )
    )

    if not card_cost.empty:

        fig6 = px.bar(
            card_cost,
            x="Cardstypes",
            y="Invitations_Cards",
            text_auto=".2f",
            color="Invitations_Cards",
            color_continuous_scale="Magma"
        )

        fig6.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Card Type",
            yaxis_title="Average Cost",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )


# =========================================================
# SELECTED COMBINATION
# =========================================================

st.markdown(
    '<div class="section-header">🎯 Detailed Wedding Analysis</div>',
    unsafe_allow_html=True
)


if (
    selected_wedding != "All"
    and selected_place != "All"
    and selected_decor != "All"
):

    st.markdown(
        f"""
        <div class="selection-card">

        <h3>✨ Selected Wedding</h3>

        <b>💒 Wedding Type:</b> {selected_wedding}
        <br><br>

        <b>📍 Place:</b> {selected_place}
        <br><br>

        <b>🌸 Decoration:</b> {selected_decor}

        </div>
        """,
        unsafe_allow_html=True
    )


    selected_entertainment = (
        filtered_df.groupby(
            "Entertainment_Category",
            as_index=False
        )["Entertainment"]
        .mean()
        .dropna()
        .sort_values(
            "Entertainment",
            ascending=False
        )
    )


    if not selected_entertainment.empty:

        fig7 = px.bar(
            selected_entertainment,
            x="Entertainment_Category",
            y="Entertainment",
            text_auto=".2f",
            color="Entertainment",
            color_continuous_scale="Turbo",
            title="Entertainment Cost for Selected Wedding"
        )

        fig7.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Entertainment Category",
            yaxis_title="Average Cost",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig7,
            use_container_width=True
        )


else:

    st.info(
        "💡 Select a Wedding Type, Place and Decoration Category "
        "from the sidebar to see detailed combination analysis."
    )


# =========================================================
# PIVOT TABLE
# =========================================================

st.markdown(
    '<div class="section-header">📌 Wedding Type × Place Analysis</div>',
    unsafe_allow_html=True
)


pivot_table = pd.pivot_table(
    df,
    index="Place",
    columns="Wedding_Type",
    values="CostofType",
    aggfunc="mean"
)


st.dataframe(
    pivot_table.round(2),
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    💍 <b>Indian Wedding Analytics Dashboard</b>

    <br>

    Built using Python • Pandas • Plotly • Streamlit

    <br><br>

    📊 Data Analysis • Visualization • Interactive Dashboard

</div>
""", unsafe_allow_html=True)
