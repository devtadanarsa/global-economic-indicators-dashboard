import streamlit as st
import pandas as pd

from charts.interest_rate import interest_rate_chart
from charts.current_account_balance import current_account_balance_chart
from utils import wide_config, set_background_color, set_chart_style, set_filter_style

# CSS configuration
wide_config()
set_background_color()
set_chart_style()
set_filter_style()

df = pd.read_csv('data/world_bank.csv')

min_year = int(df['year'].min())
max_year = int(df['year'].max())

all_countries = sorted(df['country_name'].unique().tolist())
all_countries.insert(0, "Worldwide")

col1, col2 = st.columns([10,6]) 
with col1:
    selected_countries = st.multiselect("Select Country/Countries", options=["Worldwide"] + all_countries, default=["Worldwide"])
with col2:
    year_range = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

col1, col2 = st.columns(2)
with col1:
    interest_rate_chart(selected_countries=selected_countries, year_range=year_range)
with col2:
    current_account_balance_chart(selected_countries=selected_countries, year_range=year_range)