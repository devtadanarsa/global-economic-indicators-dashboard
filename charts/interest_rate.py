import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Optional, List

df = pd.read_csv('data/world_bank.csv')
def interest_rate_chart(selected_countries: List[str], year_range: tuple = (df['year'].min(), df['year'].max())):
    filtered_df = df[
        (df['year'] >= year_range[0]) &
        (df['year'] <= year_range[1])
    ]
    
    fig = go.Figure()

    
    if "Worldwide" in selected_countries:
        worldwide_avg = filtered_df.groupby('year')['Interest Rate (Real, %)'].mean().reset_index()
        fig.add_trace(go.Scatter(
            x=worldwide_avg['year'],
            y=worldwide_avg['Interest Rate (Real, %)'],
            mode='lines+markers',
            name='Worldwide',
            line=dict(width=4),
            marker=dict(size=6),
            hovertemplate="Worldwide<br>Year: %{x}<br>Interest Rate: %{y:.2f}%",
            # legend=dict(title='Countries', font=dict(size=14, color='transparent'))
        ))
        
    for country in selected_countries:
        if country == "Worldwide":
            continue
        country_df = filtered_df[filtered_df['country_name'] == country]
        if not country_df.empty:
            avg_by_year = country_df.groupby('year')['Interest Rate (Real, %)'].mean().reset_index()
            fig.add_trace(go.Scatter(
                x=avg_by_year['year'],
                y=avg_by_year['Interest Rate (Real, %)'],
                mode='lines+markers',
                name=country,
                line=dict(width=3),
                marker=dict(size=5),
                hovertemplate=f"{country}" + "<br>Year: %{x}<br>Interest Rate: %{y:.2f}%",
            ))

    fig.update_layout(
        xaxis=dict(
            gridcolor='#314c6b',
            tickfont=dict(size=15)
        ),
        yaxis=dict(
            gridcolor='#314c6b',
            tickfont=dict(size=15)
        ),
        title={
            'text': 'Interest Rate (%)',
            'x': 0.05,
            'y': 0.90,
            'font': {'size': 28, 'color': 'white', 'family': 'Arial' },
        },
        legend=dict(
            orientation='v',
            x=0.8,
            y=1,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=14, color='white')
        ),
        font=dict(color='white', size=50),
        margin=dict(l=40, r=40, t=100, b=80),
        paper_bgcolor='#2a4664',
        plot_bgcolor='#2a4664',
    )

    # st.plotly_chart(fig, use_container_width=True)
    with st.container():
        # st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) # Example config
        st.markdown('</div>', unsafe_allow_html=True)
