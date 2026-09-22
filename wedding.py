import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Indian Wedding Analysis",
    page_icon="💍",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💍 Indian Wedding Cost 💍")

st.markdown(
    """
    Analyze Indian wedding expenses based on:
    
    - 💒 Wedding Type
    - 📍 Place
    - 🌸 Decoration
    - 🎵 Entertainment
    - 🎁 Gifts
    - 💌 Invitations / Cards
    """
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    # -----------------------------------------------------
    # Get the folder where wedding.py is located
    # -----------------------------------------------------

    BASE_DIR = Path(__file__).resolve().parent

    # -----------------------------------------------------
    # Possible CSV locations
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # If CSV is not found
    # -----------------------------------------------------

    if csv_file is None:

        st.error("❌ Indian_Weddings_.csv was not found.")

        st.write("Streamlit is looking in these locations:")

        for file in possible_files:
            st.code(str(file))

        st.warning(
            """
            Please make sure your GitHub repository contains:

            wedding.py
            Datasets/
                Indian_Weddings_.csv
            """
        )

        st.stop()

    # -----------------------------------------------------
    # Read CSV
    # -----------------------------------------------------

    df = pd.read_csv(csv_file)

    return df


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
# CLEAN TEXT COLUMNS
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
# CLEAN NUMERIC COLUMNS
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
# CHECK DATA
# =========================================================

if df.empty:

    st.error("The CSV file was found, but it contains no data.")

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Filters")


# ---------------------------------------------------------
# Wedding Type
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Place
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Decoration
# ---------------------------------------------------------

decor_categories = sorted(
    filtered_df["Decor_Category"]
    .dropna()
    .unique()
    .tolist()
)


selected_decor = st.sidebar.selectbox(
    "🌸 Decoration Category",
    ["All"] + decor_categories
)


if selected_decor != "All":

    filtered_df = filtered_df[
        filtered_df["Decor_Category"] == selected_decor
    ]


# =========================================================
# SIDEBAR RECORD COUNT
# =========================================================

st.sidebar.divider()

st.sidebar.metric(
    "📊 Records",
    len(filtered_df)
)


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📊 Key Performance Indicators")


col1, col2, col3, col4 = st.columns(4)


avg_wedding_cost = filtered_df["CostofType"].mean()

avg_decor_cost = filtered_df["Decor"].mean()

avg_entertainment_cost = filtered_df["Entertainment"].mean()

avg_gifts_cost = filtered_df["Gifts"].mean()


col1.metric(
    "💰 Avg Wedding Cost",
    f"{avg_wedding_cost:,.2f}"
    if pd.notna(avg_wedding_cost)
    else "N/A"
)


col2.metric(
    "🌸 Avg Decoration",
    f"{avg_decor_cost:,.2f}"
    if pd.notna(avg_decor_cost)
    else "N/A"
)


col3.metric(
    "🎵 Avg Entertainment",
    f"{avg_entertainment_cost:,.2f}"
    if pd.notna(avg_entertainment_cost)
    else "N/A"
)


col4.metric(
    "🎁 Avg Gifts",
    f"{avg_gifts_cost:,.2f}"
    if pd.notna(avg_gifts_cost)
    else "N/A"
)


st.divider()


# =========================================================
# DATA PREVIEW
# =========================================================

st.subheader("📋 Wedding Data")


with st.expander("View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# WEDDING COST BY TYPE
# =========================================================

st.subheader("💰 Average Wedding Cost by Wedding Type")


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
    title="Average Wedding Cost by Wedding Type"
)


fig1.update_layout(
    xaxis_title="Wedding Type",
    yaxis_title="Average Cost"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================================================
# WEDDING COST BY PLACE
# =========================================================

st.subheader("📍 Average Wedding Cost by Place")


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
    title="Average Wedding Cost by Place"
)


fig2.update_layout(
    xaxis_title="Place",
    yaxis_title="Average Cost"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================================================
# DECORATION ANALYSIS
# =========================================================

st.subheader("🌸 Decoration Analysis")


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
        title="Average Decoration Cost"
    )

    fig3.update_layout(
        xaxis_title="Decoration Category",
        yaxis_title="Average Decoration Cost"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:

    st.info("No decoration data available for this selection.")


# =========================================================
# ENTERTAINMENT ANALYSIS
# =========================================================

st.subheader("🎵 Entertainment Analysis")


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
        title="Average Entertainment Cost"
    )

    fig4.update_layout(
        xaxis_title="Entertainment Category",
        yaxis_title="Average Entertainment Cost"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

else:

    st.info(
        "No entertainment data available for this selection."
    )


# =========================================================
# GIFTS ANALYSIS
# =========================================================

st.subheader("🎁 Gift Analysis")


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
        title="Average Gift Cost"
    )

    fig5.update_layout(
        xaxis_title="Gift Type",
        yaxis_title="Average Gift Cost"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

else:

    st.info("No gift data available.")


# =========================================================
# INVITATION ANALYSIS
# =========================================================

st.subheader("💌 Invitation / Card Analysis")


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
        title="Average Invitation / Card Cost"
    )

    fig6.update_layout(
        xaxis_title="Card Type",
        yaxis_title="Average Cost"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

else:

    st.info(
        "No invitation/card data available."
    )


# =========================================================
# SELECTED COMBINATION ANALYSIS
# =========================================================

st.divider()

st.subheader("🎯 Detailed Selection Analysis")


if (
    selected_wedding != "All"
    and selected_place != "All"
    and selected_decor != "All"
):

    st.write(
        f"**Wedding Type:** {selected_wedding}"
    )

    st.write(
        f"**Place:** {selected_place}"
    )

    st.write(
        f"**Decoration:** {selected_decor}"
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
            title="Entertainment Cost for Selected Combination"
        )

        fig7.update_layout(
            xaxis_title="Entertainment Category",
            yaxis_title="Average Entertainment Cost"
        )

        st.plotly_chart(
            fig7,
            use_container_width=True
        )

    else:

        st.info(
            "No entertainment data available for this combination."
        )

else:

    st.info(
        "Select Wedding Type, Place and Decoration Category "
        "from the sidebar to see detailed analysis."
    )


# =========================================================
# PIVOT TABLE
# =========================================================

st.divider()

st.subheader("📌 Wedding Type × Place Cost")


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

st.divider()

st.caption(
    "Indian Wedding Cost Analysis | "
    "Python • Pandas • Plotly • Streamlit"
)
