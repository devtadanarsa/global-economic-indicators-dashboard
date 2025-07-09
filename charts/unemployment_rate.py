import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('D:/SEMESTER 6/Global Economic/word_bank_data_clean.csv')

# Set page config
st.set_page_config(page_title="Economic Dashboard", layout="wide")

# Pastikan kolom tahun bertipe integer dan bersih dari nilai desimal
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['year'] = df['year'].round().astype(int)

# Filter hanya tahun yang valid (misalnya antara 1960-2030)
df = df[(df['year'] >= 1960) & (df['year'] <= 2030)]

# Title
st.markdown("<h1 style='color:white;'>Economic Overview Dashboard</h1>", unsafe_allow_html=True)

# FILTER LAYOUT - 2 KOLOM SEJAJAR
col1, col2 = st.columns([1, 1])

with col1:
    # Multi-select Country selector
    countries = sorted(df['country_name'].unique())
    selected_countries = st.multiselect(
        "📍 Select Countries", 
        countries,
        default=[countries[0]] if countries else [],  # Default pilih negara pertama
        help="Select one or more countries to compare"
    )

with col2:
    # Year range slider
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.slider(
        "📅 Select Year Range", 
        min_value=min_year, 
        max_value=max_year, 
        value=(min_year, max_year),
        step=1,
        help="Select the year range for analysis"
    )

# Validasi jika tidak ada negara yang dipilih
if not selected_countries:
    st.warning("⚠️ Please select at least one country to continue.")
    st.stop()

st.markdown("---")

# Filter data by selected countries and year range
filtered_data = df[
    (df['country_name'].isin(selected_countries)) & 
    (df['year'] >= year_range[0]) & 
    (df['year'] <= year_range[1])
].copy()

# Jika tidak ada data, tampilkan pesan
if filtered_data.empty:
    st.error(f"❌ No data available for selected countries in years {year_range[0]}-{year_range[1]}")
    st.stop()

# METRICS SECTION - GDP per Capita dan Unemployment Rate
st.markdown("### 📊 Key Metrics (Latest Year)")

# Buat metrics untuk setiap negara
num_countries = len(selected_countries)
if num_countries <= 4:
    metric_cols = st.columns(num_countries)
else:
    # Jika lebih dari 4 negara, buat 2 baris
    metric_cols = st.columns(min(4, num_countries))

for i, country in enumerate(selected_countries):
    country_data = filtered_data[filtered_data['country_name'] == country]
    
    if not country_data.empty:
        latest_year_data = country_data[country_data['year'] == country_data['year'].max()]
        
        if not latest_year_data.empty:
            gdp_col = 'GDP per Capita (Current USD)'
            unemp_col = 'Unemployment Rate (%)'
            
            gdp_value = latest_year_data[gdp_col].iloc[0]
            unemp_value = latest_year_data[unemp_col].iloc[0]
            latest_year = int(latest_year_data['year'].iloc[0])
            
            col_index = i % len(metric_cols)
            
            with metric_cols[col_index]:
                st.markdown(f"**{country} ({latest_year})**")
                
                # GDP Metric
                if pd.notna(gdp_value):
                    st.metric(
                        label="💰 GDP per Capita",
                        value=f"${gdp_value:,.0f}"
                    )
                else:
                    st.metric(label="💰 GDP per Capita", value="No data")
                
                # Unemployment Metric
                if pd.notna(unemp_value):
                    st.metric(
                        label="👥 Unemployment Rate",
                        value=f"{unemp_value:.1f}%"
                    )
                else:
                    st.metric(label="👥 Unemployment Rate", value="No data")
                
                st.markdown("---")

st.markdown("---")

# UNEMPLOYMENT RATE TREND CHART
st.markdown("### 📈 Unemployment Rate Trends")

unemp_col = 'Unemployment Rate (%)'
unemp_chart_data = filtered_data.dropna(subset=[unemp_col])

if not unemp_chart_data.empty:
    fig1 = px.line(
        unemp_chart_data,
        x='year',
        y=unemp_col,
        color='country_name',
        title=f"Unemployment Rate Comparison ({year_range[0]}–{year_range[1]})",
        markers=True,
        line_shape='linear'
    )
    
    # Styling untuk unemployment chart
    fig1.update_traces(
        mode="lines+markers",
        marker=dict(size=8),
        line=dict(width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Unemployment Rate: %{y:.2f}%<extra></extra>'
    )
    
    fig1.update_layout(
        hovermode='x unified',
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
        xaxis_title="Year",
        yaxis_title="Unemployment Rate (%)",
        legend_title="Country",
        xaxis=dict(
            color="white",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            range=[year_range[0] - 0.5, year_range[1] + 0.5],
            dtick=1 if (year_range[1] - year_range[0]) <= 15 else 2
        ),
        yaxis=dict(
            color="white",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning(f"⚠️ No unemployment data available for selected countries in the year range.")

# GDP PER CAPITA TREND CHART
st.markdown("### 💹 GDP per Capita Trends")

gdp_col = 'GDP per Capita (Current USD)'
gdp_chart_data = filtered_data.dropna(subset=[gdp_col])

if not gdp_chart_data.empty:
    fig2 = px.line(
        gdp_chart_data,
        x='year',
        y=gdp_col,
        color='country_name',
        title=f"GDP per Capita Comparison ({year_range[0]}–{year_range[1]})",
        markers=True,
        line_shape='linear'
    )
    
    # Styling untuk GDP chart
    fig2.update_traces(
        mode="lines+markers",
        marker=dict(size=8),
        line=dict(width=3),
        hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>GDP per Capita: $%{y:,.0f}<extra></extra>'
    )
    
    fig2.update_layout(
        hovermode='x unified',
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
        xaxis_title="Year",
        yaxis_title="GDP per Capita (USD)",
        legend_title="Country",
        xaxis=dict(
            color="white",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            range=[year_range[0] - 0.5, year_range[1] + 0.5],
            dtick=1 if (year_range[1] - year_range[0]) <= 15 else 2
        ),
        yaxis=dict(
            color="white",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning(f"⚠️ No GDP data available for selected countries in the year range.")

# COMPARATIVE ANALYSIS
if len(selected_countries) > 1:
    st.markdown("### 🔍 Comparative Analysis")
    
    col_analysis1, col_analysis2 = st.columns(2)
    
    with col_analysis1:
        st.markdown("**📊 Average Statistics**")
        
        for country in selected_countries:
            country_data = filtered_data[filtered_data['country_name'] == country]
            
            if not country_data.empty:
                avg_gdp = country_data[gdp_col].mean()
                avg_unemp = country_data[unemp_col].mean()
                
                st.write(f"**{country}:**")
                st.write(f"• Avg GDP per Capita: ${avg_gdp:,.0f}" if pd.notna(avg_gdp) else "• Avg GDP per Capita: No data")
                st.write(f"• Avg Unemployment: {avg_unemp:.2f}%" if pd.notna(avg_unemp) else "• Avg Unemployment: No data")
                st.write("---")
    
    with col_analysis2:
        st.markdown("**📈 Growth Analysis**")
        
        for country in selected_countries:
            country_data = filtered_data[filtered_data['country_name'] == country].sort_values('year')
            
            if len(country_data) > 1:
                first_year_gdp = country_data[gdp_col].iloc[0]
                last_year_gdp = country_data[gdp_col].iloc[-1]
                
                if pd.notna(first_year_gdp) and pd.notna(last_year_gdp) and first_year_gdp > 0:
                    growth_rate = ((last_year_gdp - first_year_gdp) / first_year_gdp) * 100
                    
                    st.write(f"**{country}:**")
                    st.write(f"• GDP Growth: {growth_rate:+.1f}%")
                    st.write(f"• Period: {country_data['year'].iloc[0]} - {country_data['year'].iloc[-1]}")
                    st.write("---")