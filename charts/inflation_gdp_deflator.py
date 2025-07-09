import streamlit as st
import pandas as pd
import altair as alt

# ——————————————————————————————————————————————
# 0) Page config: wide layout
# ——————————————————————————————————————————————
st.set_page_config(
    page_title="Dashboard Indikator Ekonomi",
    layout="wide",
)

# ——————————————————————————————————————————————
# 1) Load & cache data
# ——————————————————————————————————————————————
@st.cache_data
def load_data():
    df = pd.read_csv("world_bank_data_2025.csv")
    df["year"] = df["year"].astype(int)
    return df

df = load_data()

# ——————————————————————————————————————————————
# 2) Top Filters (container penuh di atas)
# ——————————————————————————————————————————————
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_countries = st.multiselect(
            "🔍 Pilih Negara",
            options=sorted(df["country_name"].unique()),
            default=sorted(df["country_name"].unique())[:3],
            help="Tahan Ctrl (Windows) atau Cmd (Mac) untuk pilih beberapa"
        )
    with col2:
        min_year = int(df["year"].min())
        max_year = int(df["year"].max())
        selected_years = st.slider(
            "⏳ Pilih Rentang Tahun",
            min_year,
            max_year,
            (min_year, max_year),
        )

# filter data
filtered = df[
    df["country_name"].isin(selected_countries) &
    df["year"].between(selected_years[0], selected_years[1])
]

st.title("🌍 Dashboard Indikator Ekonomi")

if filtered.empty:
    st.warning("⚠️ Tidak ada data untuk pilihan Anda.")
    st.stop()

# helper untuk styling axis
axis_x = alt.Axis(labelAngle=0, titleFontSize=14, labelFontSize=12, grid=False)
axis_y = alt.Axis(titleFontSize=14, labelFontSize=12, grid=True, gridOpacity=0.2)

st.subheader("📈 Inflasi")

st.markdown("**GDP Deflator (%)**")
chart_def = (
    alt.Chart(filtered)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X("year:O", title="Tahun", axis=axis_x),
        y=alt.Y("Inflation (GDP Deflator, %):Q", title="Inflasi (%)", axis=axis_y),
        color=alt.Color("country_name:N", title="Negara"),
        tooltip=["country_name", "year", "Inflation (GDP Deflator, %)"]
    )
    .properties(height=450)
    .configure_view(strokeWidth=0)
)
st.altair_chart(chart_def, use_container_width=True)