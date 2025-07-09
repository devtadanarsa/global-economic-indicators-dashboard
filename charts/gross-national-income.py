import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gross National Income", layout="wide")
st.title("Gross National Income (GNI)")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("charts/world_bank_data_2025.csv")
    return df

data = load_data()

# Multi-pilih negara & rentang tahun
col_country, col_year = st.columns([2, 3])
with col_country:
    countries = sorted(data["country_name"].unique())
    selected_countries = st.multiselect(
        "Select Countries",
        countries,
        default=["Japan"] if "Japan" in countries else [countries[0]]
    )

with col_year:
    years = sorted(data["year"].unique())
    year_range = st.slider(
        "Select Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(2010, 2023),
        step=1
    )
    start_year, end_year = year_range

# Filter data sesuai pilihan
df_filtered = data[
    (data["country_name"].isin(selected_countries)) &
    (data["year"] >= start_year) &
    (data["year"] <= end_year)
].copy()

# Grafik GNI time-series untuk tiap negara
st.subheader(f"GNI Trend ({start_year}–{end_year})")

fig_gni = px.line(
    df_filtered.sort_values("year"),
    x="year",
    y="Gross National Income (USD)",
    color="country_name",
    markers=True,
    labels={
        "Gross National Income (USD)": "GNI (USD)",
        "country_name": "Country",
        "year": "Year"
    }
)

fig_gni.update_layout(yaxis_tickformat=",", legend_title="Country")
st.plotly_chart(fig_gni, use_container_width=True)
