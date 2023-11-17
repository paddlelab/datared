import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
import plotly.express as px


result_df = pd.read_csv('overall.csv')

# Initialize a scaler
scaler = MinMaxScaler()

# Normalize the columns
result_df[['Average Latency', 'Average Distance', 'International Data Exchange', 'GAFAM Data Exchange', 'Proportion Data Shared']] = scaler.fit_transform(result_df[['Average Latency', 'Average Distance', 'International Data Exchange', 'GAFAM Data Exchange', 'Proportion Data Shared']])

# Create a color mapping for 'Country/Province'
unique_countries = result_df['Country/Province'].unique()
colors = px.colors.qualitative.Plotly
color_mapping = dict(zip(unique_countries, colors[:len(unique_countries)]))

# Define the data for the radar chart
data = [
    go.Scatterpolar(
        r=result_df.loc[i, ['Average Latency', 'Average Distance', 'International Data Exchange', 'GAFAM Data Exchange', 'Proportion Data Shared']],
        theta=['Average Latency', 'Average Distance', 'International Data Exchange', 'GAFAM Data Exchange', 'Proportion Data Shared'],
        fill='toself',
        name=f"{result_df.loc[i, 'Country/Province']} - {result_df.loc[i, 'Session']}",  # concatenate 'Country/Province' and 'Session'
        line=dict(color=color_mapping[result_df.loc[i, 'Country/Province']])
    ) for i in range(len(result_df))
]

# Define the layout for the radar chart
layout = go.Layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            showticklabels=False,
            range=[0, 1]
        )
    ),
    showlegend=True
)

# Create the figure
fig = go.Figure(data=data, layout=layout)

# Update the layout
fig.update_layout(,
    autosize=False,
    width=800,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)

# Create a container for the chart
with st.beta_container():
    st.markdown("<h1 style='text-align: center; color: black;'>RED Data Profiles</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig)
