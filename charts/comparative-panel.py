import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparative Panel", layout="wide")
st.title("Comparative Panel")

@st.cache_data
def load_data():
    df = pd.read_csv("world_bank_data_2025.csv")
    return df

data = load_data()
countries = sorted(data["country_name"].unique())
years = sorted(data["year"].unique())

# Fungsi format angka T, B, M
def format_number(val):
    if pd.isna(val):
        return "N/A"
    elif val >= 1e12:
        return f"{val / 1e12:.2f} T"
    elif val >= 1e9:
        return f"{val / 1e9:.2f} B"
    elif val >= 1e6:
        return f"{val / 1e6:.2f} M"
    else:
        return f"{val:,.0f}"

# Fungsi buat bar indikator (dengan label & nilai % di sisi kanan)
def render_bar(value, max_value=100, label=""):
    if pd.isna(value):
        value_text = "N/A"
        bar_width = 0
        over = False
    else:
        value_text = f"{value:.2f}%"
        over = value > max_value
        bar_width = min(value / max_value, 1.0) * 100

    bar_color = "#f28e69" if over else "#69b3f2"
    max_label = f"Max: {max_value:.0f}%" + (" <span title='Exceeds scale'>⚠️</span>" if over else "")

    return f"""
        <div style="margin-bottom:16px">
            <div style='display: flex; justify-content: space-between; font-size:0.85rem; margin-bottom:4px;'>
                <span>{label}</span>
                <span>{value_text}</span>
            </div>
            <div style="background-color:#e0e0e0;width:100%;height:12px;border-radius:4px;overflow:hidden;">
                <div style="background-color:{bar_color};width:{bar_width}%;height:100%"></div>
            </div>
            <div style='display: flex; justify-content: space-between; font-size:0.75rem; color: #888; margin-top:2px'>
                <span>0%</span>
                <span>{max_label}</span>
            </div>
        </div>
    """

# Dua panel perbandingan
for i in range(1, 3):
    st.markdown(f"### Panel {i}")

    col1, col2 = st.columns([2, 1])
    with col1:
        country = st.selectbox(f"Select Country {i}", countries, key=f"country_{i}")
    with col2:
        year = st.selectbox(f"Select Year {i}", years, key=f"year_{i}")

    row = data[(data["country_name"] == country) & (data["year"] == year)]
    if row.empty:
        st.warning("Data not found for this selection.")
        continue
    row = row.iloc[0]

    # Ambil nilai indikator
    gdp = row["GDP (Current USD)"]
    gdp_growth = row["GDP Growth (% Annual)"]
    tax_rev = row["Tax Revenue (% of GDP)"]
    pub_debt = row["Public Debt (% of GDP)"]

    # Tampilkan GDP dan bar indikator lainnya
    st.markdown(f"**GDP:** {format_number(gdp)} USD", unsafe_allow_html=True)
    st.markdown(render_bar(gdp_growth, max_value=15, label="GDP Growth (% Annual)"), unsafe_allow_html=True)
    st.markdown(render_bar(tax_rev, max_value=50, label="Tax Revenue (% of GDP)"), unsafe_allow_html=True)
    st.markdown(render_bar(pub_debt, max_value=200, label="Public Debt (% of GDP)"), unsafe_allow_html=True)

    st.markdown("---")
