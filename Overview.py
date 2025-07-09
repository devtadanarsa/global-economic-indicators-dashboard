import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils import format_number

st.set_page_config(page_title="Economic Overview Dashboard", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #1e2f44;
            color: #FFFFFF;
        }
        .block-container {
            padding: 2rem 4rem;
        }
        h1, h2, h3, h4, h5 {
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)

# ======================================
# Load Data
# ======================================
df = pd.read_csv('data/world_bank_data.csv')
countries = ["Worldwide"] + sorted(df['country_name'].unique())
years = [year for year in sorted(df['year'].unique()) if year <= 2023]

# ======================================
# Sidebar Filters and Title
# ======================================
st.title("Economic Overview Dashboard")
st.sidebar.header("Filter")
country = st.sidebar.selectbox("Country", countries)
year_range = st.sidebar.slider("Year Range", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# ======================================
#  Filter Data
# ======================================
if country == "Worldwide":
    filtered = df[df['year'] == year_range[1]].groupby('year').mean(numeric_only=True).reset_index()
    filtered_range = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])].groupby('year').mean(numeric_only=True).reset_index()
else:
    filtered = df[(df['country_name'] == country) & (df['year'] == year_range[1])]
    filtered_range = df[(df['country_name'] == country) & (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# ======================================
#  Metrics Row
# ======================================
col1, col2, col3 = st.columns(3)
def safe_get_value(df, col, fallback=np.nan):
    return df[col].values[0] if not df.empty and col in df.columns else fallback


latest_year = year_range[1]
previous_year = latest_year - 1

if country == "Worldwide":
    filtered_latest = df[df['year'] == latest_year].mean(numeric_only=True)
    filtered_prev = df[df['year'] == previous_year].mean(numeric_only=True)

    gdp = filtered_latest['GDP (Current USD)']
    gdp_per_capita = filtered_latest['GDP per Capita (Current USD)']
    gni = filtered_latest['Gross National Income (USD)']

    prev_gdp = filtered_prev['GDP (Current USD)']
    prev_gdp_per_capita = filtered_prev['GDP per Capita (Current USD)']
    prev_gni = filtered_prev['Gross National Income (USD)']
else:
    filtered_latest = df[(df['country_name'] == country) & (df['year'] == latest_year)]
    filtered_prev = df[(df['country_name'] == country) & (df['year'] == previous_year)]

    gdp = filtered_latest['GDP (Current USD)'].iloc[0] if not filtered_latest.empty else np.nan
    gdp_per_capita = filtered_latest['GDP per Capita (Current USD)'].iloc[0] if not filtered_latest.empty else np.nan
    gni = filtered_latest['Gross National Income (USD)'].iloc[0] if not filtered_latest.empty else np.nan

    prev_gdp = safe_get_value(filtered_prev, 'GDP (Current USD)')
    prev_gdp_per_capita = safe_get_value(filtered_prev, 'GDP per Capita (Current USD)')
    prev_gni = safe_get_value(filtered_prev, 'Gross National Income (USD)')

gdp_growth = ((gdp - prev_gdp) / prev_gdp * 100) if not pd.isna(prev_gdp) and prev_gdp != 0 else None
gdp_pc_growth = ((gdp_per_capita - prev_gdp_per_capita) / prev_gdp_per_capita * 100) if not pd.isna(prev_gdp_per_capita) and prev_gdp_per_capita != 0 else None
gni_growth = ((gni - prev_gni) / prev_gni * 100) if not pd.isna(prev_gni) and prev_gni != 0 else None


col1, col2, col3 = st.columns(3)
col1.metric(f"GDP in {year_range[1]}", f"{format_number(gdp)} USD", f"{gdp_growth:.2f}% from last year" if gdp_growth is not None else "N/A")
col2.metric(f"GDP per Capita in {year_range[1]}", f"{format_number(gdp_per_capita)} USD", f"{gdp_pc_growth:.2f}% from last year" if gdp_pc_growth is not None else "N/A")
col3.metric(f"Gross National Income in {year_range[1]}", f"{format_number(gni)} USD", f"{gni_growth:.2f}% from last year" if gni_growth is not None else "N/A")


# ======================================
#  Charts Grid
# ======================================
grid1_col1, grid1_col2 = st.columns(2)
fig_gdp = px.line(
    filtered_range,
    x='year',
    y='GDP per Capita (Current USD)',
    labels={'GDP (Current USD)': 'Inflation'},
    title='GDP Per Capita'
)
fig_gdp.update_traces(
    hovertemplate='<b>Year:</b> %{x}<br><b>GDP Per Capita:</b> %{y}<extra></extra>',
    line=dict(width=4)
)
fig_gdp.update_layout(
    title=dict(
        text='GDP Per Capita Trend',
        font=dict(size=28)
    ),
    xaxis_title="Year",
)
grid1_col1.plotly_chart(fig_gdp, use_container_width=True)

# Inflation Chart
fig_inflation = px.line(
    filtered_range,
    x='year',
    y='Inflation (CPI %)',
    labels={'Inflation (CPI %)': 'Inflation'},
    title='Inflation Rate Trend'
)
fig_inflation.update_traces(
    hovertemplate='<b>Year:</b> %{x}<br><b>Inflation:</b> %{y:.2f}%<extra></extra>',
    line=dict(width=4)
)
fig_inflation.update_layout(
    title=dict(
        text='Inflation Rate',
        font=dict(size=28)
    ),
    xaxis_title="Year",
)
grid1_col2.plotly_chart(fig_inflation, use_container_width=True)

# Revenue vs Expense Bar Chart
grid2_col1, grid2_col2 = st.columns(2)

fig_rev_exp = go.Figure()

fig_rev_exp.add_trace(go.Bar(
    x=filtered_range['year'],
    y=filtered_range['Government Revenue (% of GDP)'],
    name='Revenue',
    hovertemplate='<b>Year:</b> %{x}<br><b>Revenue:</b> %{y:.2f}% of GDP<extra></extra>'
))
fig_rev_exp.add_trace(go.Bar(
    x=filtered_range['year'],
    y=filtered_range['Government Expense (% of GDP)'],
    name='Expense',
    hovertemplate='<b>Year:</b> %{x}<br><b>Expense:</b> %{y:.2f}% of GDP<extra></extra>'
))
fig_rev_exp.update_layout(
    barmode='group',
    title=dict(
        text='Government Revenue vs Expense',
        font=dict(size=28)
    ),
    xaxis_title="Year",
    yaxis_title='% of GDP',
)
grid2_col1.plotly_chart(fig_rev_exp, use_container_width=True)

# Unemployment Chart
fig_unemployment = px.bar(
    filtered_range,
    x='year',
    y='Unemployment Rate (%)',
    labels={'Unemployment Rate (%)': 'Unemployment (%)'},
    title='Unemployment Rate Trend'
)
fig_unemployment.update_traces(
    hovertemplate='<b>Year:</b> %{x}<br><b>Unemployment:</b> %{y:.2f}%<extra></extra>'
)
fig_unemployment.update_layout(
    title=dict(
        text='Unemployment Rate',
        font=dict(size=28)
    ),
    xaxis_title="Year",
)
grid2_col2.plotly_chart(fig_unemployment, use_container_width=True)

# Interest Rate & Current Account Balance
grid3_col1, grid3_col2 = st.columns(2)

fig_ir = px.line(
    filtered_range,
    x='year',
    y='Interest Rate (Real, %)',
    labels={'Interest Rate (Real, %)': 'Interest Rate (%)'},
    title='Interest Rate'
)
fig_ir.update_traces(
    hovertemplate='<b>Year:</b> %{x}<br><b>Interest Rate:</b> %{y:.2f}%<extra></extra>',
    line=dict(width=4)
)
fig_ir.update_layout(
    title=dict(
        text='Interest Rate',
        font=dict(size=28)
    ),
    xaxis_title="Year",
)
grid3_col1.plotly_chart(fig_ir, use_container_width=True)

fig_cab = px.line(
    filtered_range,
    x='year',
    y='Current Account Balance (% GDP)',
    labels={'Current Account Balance (% GDP)': 'Current Account Balance (% of GDP)'},
    title='Current Account Balance Trend'
)
fig_cab.update_traces(
    hovertemplate='<b>Year:</b> %{x}<br><b>Current Account Balance:</b> %{y:.2f}% of GDP<extra></extra>',
    line=dict(width=4)
)
fig_cab.update_layout(
    title=dict(
        text='Current Account Balance',
        font=dict(size=28)
    ),
    xaxis_title="Year",
)
grid3_col2.plotly_chart(fig_cab, use_container_width=True)