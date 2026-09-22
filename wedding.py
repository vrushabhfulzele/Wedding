import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Indian Wedding Cost Analysis",
    page_icon="💍",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💍 Indian Wedding Cost Analysis Dashboard")
st.markdown(
    "Explore wedding costs based on **Wedding Type, Place, Decoration, "
    "Entertainment, Gifts and Invitations**."
)

st.divider()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("../Datasets/Indian_Weddings_.csv")

    # Remove unnecessary index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)

    # Rename columns
    df = df.rename(columns={
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
    })

    # Clean categorical columns
    categorical_columns = [
        "Wedding_Type",
        "Place",
        "Decor_Category",
        "Entertainment_Category",
        "Giftstypes",
        "Cardstypes"
    ]

    for col in categorical_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("/", "", regex=False)
                .str.strip()
            )

    # Clean CostofType
    if "CostofType" in df.columns:
        df["CostofType"] = (
            df["CostofType"]
            .astype(str)
            .str.replace("e+", "", regex=False)
            .str.strip()
        )

        df["CostofType"] = pd.to_numeric(
            df["CostofType"],
            errors="coerce"
        )

    # Convert numeric columns
    numeric_columns = [
        "CostofType",
        "Decor",
        "Entertainment",
        "Gifts",
        "Invitations_Cards"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


# =========================================================
# CHECK DATA
# =========================================================

if df.empty:
    st.error("The dataset is empty.")
    st.stop()


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")

# Wedding Type
wedding_options = sorted(
    df["Wedding_Type"].dropna().unique()
)

selected_wedding = st.sidebar.selectbox(
    "Select Wedding Type",
    ["All"] + wedding_options
)

# Apply Wedding Type filter
filtered_df = df.copy()

if selected_wedding != "All":
    filtered_df = filtered_df[
        filtered_df["Wedding_Type"] == selected_wedding
    ]


# Place
place_options = sorted(
    filtered_df["Place"].dropna().unique()
)

selected_place = st.sidebar.selectbox(
    "Select Place",
    ["All"] + place_options
)

if selected_place != "All":
    filtered_df = filtered_df[
        filtered_df["Place"] == selected_place
    ]


# Decor Category
decor_options = sorted(
    filtered_df["Decor_Category"].dropna().unique()
)

selected_decor = st.sidebar.selectbox(
    "Select Decor Category",
    ["All"] + decor_options
)

if selected_decor != "All":
    filtered_df = filtered_df[
        filtered_df["Decor_Category"] == selected_decor
    ]


st.sidebar.divider()

st.sidebar.info(
    f"Showing **{len(filtered_df)}** records"
)


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📊 Wedding Cost Overview")

col1, col2, col3, col4 = st.columns(4)

avg_wedding_cost = filtered_df["CostofType"].mean()
avg_decor = filtered_df["Decor"].mean()
avg_entertainment = filtered_df["Entertainment"].mean()
avg_gifts = filtered_df["Gifts"].mean()

col1.metric(
    "Average Wedding Cost",
    f"{avg_wedding_cost:,.2f}"
    if pd.notna(avg_wedding_cost)
    else "N/A"
)

col2.metric(
    "Average Decor Cost",
    f"{avg_decor:,.2f}"
    if pd.notna(avg_decor)
    else "N/A"
)

col3.metric(
    "Average Entertainment",
    f"{avg_entertainment:,.2f}"
    if pd.notna(avg_entertainment)
    else "N/A"
)

col4.metric(
    "Average Gifts",
    f"{avg_gifts:,.2f}"
    if pd.notna(avg_gifts)
    else "N/A"
)


st.divider()


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("📋 View Filtered Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# WEDDING TYPE ANALYSIS
# =========================================================

st.subheader("💰 Average Wedding Cost by Wedding Type")

wedding_cost = (
    df.groupby("Wedding_Type", as_index=False)["CostofType"]
    .mean()
    .sort_values("CostofType", ascending=False)
)

fig_wedding = px.bar(
    wedding_cost,
    x="Wedding_Type",
    y="CostofType",
    text_auto=".2f",
    title="Average Wedding Cost"
)

fig_wedding.update_layout(
    xaxis_title="Wedding Type",
    yaxis_title="Average Cost"
)

st.plotly_chart(
    fig_wedding,
    use_container_width=True
)


# =========================================================
# PLACE ANALYSIS
# =========================================================

st.subheader("📍 Average Wedding Cost by Place")

place_cost = (
    df.groupby("Place", as_index=False)["CostofType"]
    .mean()
    .sort_values("CostofType", ascending=False)
)

fig_place = px.bar(
    place_cost,
    x="Place",
    y="CostofType",
    text_auto=".2f",
    title="Average Wedding Cost by Place"
)

fig_place.update_layout(
    xaxis_title="Place",
    yaxis_title="Average Cost"
)

st.plotly_chart(
    fig_place,
    use_container_width=True
)


# =========================================================
# DECOR ANALYSIS
# =========================================================

st.subheader("🌸 Decoration Analysis")

decor_cost = (
    filtered_df
    .groupby("Decor_Category", as_index=False)["Decor"]
    .mean()
    .sort_values("Decor", ascending=False)
)

fig_decor = px.bar(
    decor_cost,
    x="Decor_Category",
    y="Decor",
    text_auto=".2f",
    title="Average Decoration Cost by Category"
)

fig_decor.update_layout(
    xaxis_title="Decoration Category",
    yaxis_title="Average Decoration Cost"
)

st.plotly_chart(
    fig_decor,
    use_container_width=True
)


# =========================================================
# ENTERTAINMENT ANALYSIS
# =========================================================

st.subheader("🎵 Entertainment Analysis")

entertainment_cost = (
    filtered_df
    .groupby(
        "Entertainment_Category",
        as_index=False
    )["Entertainment"]
    .mean()
    .sort_values(
        "Entertainment",
        ascending=False
    )
)

fig_entertainment = px.bar(
    entertainment_cost,
    x="Entertainment_Category",
    y="Entertainment",
    text_auto=".2f",
    title="Average Entertainment Cost"
)

fig_entertainment.update_layout(
    xaxis_title="Entertainment Category",
    yaxis_title="Average Entertainment Cost"
)

st.plotly_chart(
    fig_entertainment,
    use_container_width=True
)


# =========================================================
# GIFTS ANALYSIS
# =========================================================

st.subheader("🎁 Gifts Analysis")

gift_cost = (
    filtered_df
    .groupby("Giftstypes", as_index=False)["Gifts"]
    .mean()
    .sort_values(
        "Gifts",
        ascending=False
    )
)

fig_gifts = px.bar(
    gift_cost,
    x="Giftstypes",
    y="Gifts",
    text_auto=".2f",
    title="Average Gift Cost by Type"
)

fig_gifts.update_layout(
    xaxis_title="Gift Type",
    yaxis_title="Average Gift Cost"
)

st.plotly_chart(
    fig_gifts,
    use_container_width=True
)


# =========================================================
# INVITATION / CARD ANALYSIS
# =========================================================

st.subheader("💌 Invitation & Card Analysis")

card_cost = (
    filtered_df
    .groupby("Cardstypes", as_index=False)["Invitations_Cards"]
    .mean()
    .sort_values(
        "Invitations_Cards",
        ascending=False
    )
)

fig_cards = px.bar(
    card_cost,
    x="Cardstypes",
    y="Invitations_Cards",
    text_auto=".2f",
    title="Average Invitation/Card Cost"
)

fig_cards.update_layout(
    xaxis_title="Card Type",
    yaxis_title="Average Cost"
)

st.plotly_chart(
    fig_cards,
    use_container_width=True
)


# =========================================================
# SELECTED FILTER ANALYSIS
# =========================================================

st.divider()

st.subheader("🎯 Selected Wedding Combination Analysis")

if (
    selected_wedding != "All"
    and selected_place != "All"
    and selected_decor != "All"
):

    st.write(
        f"""
        **Wedding Type:** {selected_wedding}  
        **Place:** {selected_place}  
        **Decor Category:** {selected_decor}
        """
    )

    selected_entertainment = (
        filtered_df
        .groupby(
            "Entertainment_Category",
            as_index=False
        )["Entertainment"]
        .mean()
        .sort_values(
            "Entertainment",
            ascending=False
        )
    )

    if not selected_entertainment.empty:

        fig_selected = px.bar(
            selected_entertainment,
            x="Entertainment_Category",
            y="Entertainment",
            text_auto=".2f",
            title="Entertainment Cost for Selected Combination"
        )

        fig_selected.update_layout(
            xaxis_title="Entertainment Category",
            yaxis_title="Average Entertainment Cost"
        )

        st.plotly_chart(
            fig_selected,
            use_container_width=True
        )

    else:
        st.warning(
            "No entertainment data available for the selected combination."
        )

else:

    st.info(
        "Select a Wedding Type, Place and Decor Category "
        "from the sidebar to see the detailed combination analysis."
    )


# =========================================================
# PIVOT TABLE
# =========================================================

st.divider()

st.subheader("📌 Wedding Type × Place Cost Analysis")

pivot_table = pd.pivot_table(
    df,
    index="Place",
    columns="Wedding_Type",
    values="CostofType",
    aggfunc="mean",
    margins=True
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
    "Indian Wedding Cost Analysis | Built with Python, Pandas, Plotly & Streamlit"
)
