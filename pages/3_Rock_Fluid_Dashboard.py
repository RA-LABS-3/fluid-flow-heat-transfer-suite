"""
Rock & Fluid Data Dashboard page.

Lets the user upload a CSV of rock/fluid data, view summary statistics,
filter by porosity, and visualize porosity distribution and the
porosity-permeability relationship.

Expects columns named 'porosity_percent' and 'permeability_md'.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rock & Fluid Data Dashboard", layout="wide")

st.title("Rock & Fluid Data Dashboard")
st.write(
    "Upload a CSV of rock/fluid sample data to view summary statistics, "
    "filter by porosity, and explore porosity-permeability trends."
)
st.caption(
    "Expected columns: `porosity_percent` and `permeability_md` "
    "(other columns are fine too and will be shown in the summary)."
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read this file as a CSV: {e}")
        st.stop()

    required_columns = {"porosity_percent", "permeability_md"}
    if not required_columns.issubset(df.columns):
        st.error(
            f"This file is missing required columns: "
            f"{required_columns - set(df.columns)}. "
            f"Found columns: {list(df.columns)}"
        )
        st.stop()

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    st.subheader("Filter by Porosity")
    min_porosity = float(df["porosity_percent"].min())
    max_porosity = float(df["porosity_percent"].max())
    porosity_threshold = st.slider(
        "Show samples with porosity greater than or equal to (%)",
        min_value=min_porosity,
        max_value=max_porosity,
        value=min_porosity,
    )

    filtered_df = df[df["porosity_percent"] >= porosity_threshold]
    st.write(f"Showing {len(filtered_df)} of {len(df)} samples.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Porosity Histogram")
        fig1, ax1 = plt.subplots()
        ax1.hist(filtered_df["porosity_percent"], bins=15, edgecolor="black")
        ax1.set_xlabel("Porosity (%)")
        ax1.set_ylabel("Count")
        ax1.set_title("Porosity Distribution")
        st.pyplot(fig1)

    with col2:
        st.subheader("Porosity vs Permeability")
        fig2, ax2 = plt.subplots()
        ax2.scatter(filtered_df["porosity_percent"], filtered_df["permeability_md"])
        ax2.set_xlabel("Porosity (%)")
        ax2.set_ylabel("Permeability (mD)")
        ax2.set_title("Porosity-Permeability Crossplot")
        ax2.grid(True)
        st.pyplot(fig2)

    st.subheader("Download Filtered Data")
    csv_data = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_data,
        file_name="filtered_rock_fluid_data.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to get started.")