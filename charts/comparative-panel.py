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

# Fungsi buat bar indikator
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

# Ambil semua indikator numerik (kecuali country & year)
indicator_columns = [col for col in data.columns if col not in ["country_name", "year"] and pd.api.types.is_numeric_dtype(data[col])]

# User pilih indikator yang ingin ditampilkan
selected_indicators = st.multiselect(
    "Pilih indikator yang ingin ditampilkan",
    indicator_columns,
    default=["GDP (Current USD)", "GDP Growth (% Annual)", "Tax Revenue (% of GDP)", "Public Debt (% of GDP)"]
)

# Pilih jumlah panel
num_panels = st.number_input("Jumlah panel perbandingan", min_value=2, max_value=4, value=2, step=1)

# Tentukan mana indikator angka dan mana yang bar (% / rasio)
def is_numeric_only(col):
    return "USD" in col or "Income" in col or ("GDP" in col and "%" not in col)

# Siapkan max_value per kolom berdasarkan data
max_dict = {}
for col in selected_indicators:
    max_val = data[col].max()
    if "growth" in col.lower():
        max_dict[col] = 15
    elif "tax" in col.lower():
        max_dict[col] = 50
    elif "debt" in col.lower():
        max_dict[col] = 200
    elif "%" in col:
        max_dict[col] = min(100, max_val + 10)
    else:
        max_dict[col] = max_val + (0.1 * max_val)

# Fungsi render tiap panel
def render_panel(panel, i):
    with panel:
        st.markdown(f"### Panel {i}")

        col1, col2 = st.columns([2, 1])
        with col1:
            country = st.selectbox(f"Select Country {i}", countries, key=f"country_{i}")
        with col2:
            year = st.selectbox(f"Select Year {i}", years, key=f"year_{i}")

        row = data[(data["country_name"] == country) & (data["year"] == year)]
        if row.empty:
            st.warning("Data not found for this selection.")
            return
        row = row.iloc[0]

        # Tampilkan indikator angka dulu
        for col in selected_indicators:
            if is_numeric_only(col):
                val = row[col]
                st.markdown(f"**{col}:** {format_number(val)}", unsafe_allow_html=True)

        # Lalu tampilkan bar indikator
        for col in selected_indicators:
            if not is_numeric_only(col):
                val = row[col]
                max_val = max_dict.get(col, 100)
                st.markdown(render_bar(val, label=col, max_value=max_val), unsafe_allow_html=True)

# Buat kolom panel dinamis & render
panels = st.columns(num_panels)
for i in range(num_panels):
    render_panel(panels[i], i + 1)
