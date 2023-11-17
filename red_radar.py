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
fig.update_layout(
    title='RED Data Profiles',
    autosize=True,
    height=900
)

# Display the radar chart
st.plotly_chart(fig, use_container_width=True)
