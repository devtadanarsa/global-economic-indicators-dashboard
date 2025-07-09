import streamlit as st
import pandas as pd

def wide_config():
    return st.set_page_config(layout="wide")

def set_background_color():
    return st.markdown(
    """
    <style>
    body {
        background-color: #223c55 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #223c55;
    }

    [data-testid="stApp"] {
        background-color: #223c55;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
def set_chart_style():
    st.markdown("""
    <style>
    .stPlotlyChart {
        border-radius: 20px; 
        overflow: hidden;
        background-color: #2a4664;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    .chart-card {
        border-radius: 20px;
        overflow: hidden;
        background-color: #2a4664; /* Match your plot_bgcolor/paper_bgcolor */
        padding: 15px; /* Padding inside the card */
        margin-bottom: 20px; /* Space between cards if you have multiple */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
def set_filter_style():
    return st.markdown("""
        <style>
        label, .stSlider > div > div:first-child {
            color: white !important;
            font-weight: 500;
        }

        .stMultiSelect > div {
            background-color: #1e3a5f !important;
            color: white !important;
            border: 1px solid #3b82f6 !important;  /* blue border */
            border-radius: 8px;
        }

        .css-1wa3eu0-placeholder, .css-1okebmr-indicatorSeparator, .css-1uccc91-singleValue {
            color: white !important;
        }

        .css-12jo7m5 {
            background: white
        }
        </style>
        """, unsafe_allow_html=True)
    
def format_number(val):
    if pd.isna(val):
        return "N/A"
    elif val >= 1e12:
        return f"{val / 1e12:.1f} T"
    elif val >= 1e9:
        return f"{val / 1e9:.1f} B"
    elif val >= 1e6:
        return f"{val / 1e6:.1f} M"
    else:
        return f"{val:,.1f}"