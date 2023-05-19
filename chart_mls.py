import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
import calendar
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from streamlit_echarts import st_echarts

options1 = {
    "xAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
    ],
}
st_echarts(options=options1)

with open("USA.json", "r") as f:
    map = Map(
        "USA",
        json.loads(f.read()),
        {
            "Alaska": {"left": -131, "top": 25, "width": 15},
            "Hawaii": {"left": -110, "top": 28, "width": 5},
            "Puerto Rico": {"left": -76, "top": 26, "width": 2},
        },
    )
options2 = {...}
st_echarts(options, map=map)

 
#-- Create three columns
st.title("Project #1 - Key Milestones Chart")
col1, col2 = st.columns([30, 30])
with col1:
    month_choice = st.slider(
        "What month would you like to view?",
        min_value=6,
        max_value=12,
        step=1,
        value=6,
    )   
with col2:
    year_choice = st.slider(
        "What year would you like to view?",
        min_value=2022,
        max_value=2026,
        step=1,
        value=2022,
    )

@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

# -- Apply the year filter given by the user
res = calendar.monthrange(year_choice, month_choice)[1]
date = datetime.date(year_choice,month_choice,res)
df['Status Date']=pd.to_datetime(df['Status Date'], format= '%d/%m/%Y')
df['Baseline']=pd.to_datetime(df['Baseline'], format= '%d/%m/%Y')
df['Forecast']=pd.to_datetime(df['Forecast'], format= '%d/%m/%Y')
df['Actual']=pd.to_datetime(df['Actual'], format= '%d/%m/%Y')
filtered_df = df[df['Status Date'] == pd.to_datetime(date)]


# -- Create the figure in Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(x=filtered_df["Forecast"], y=filtered_df["Milestone No."], name = 'Forecast',
                         line=dict(color='royalblue', width=1),marker_symbol="square"))
fig.update_traces(text=filtered_df["Milestone No."], mode='lines+markers+text')

fig.add_trace(go.Scatter(x=filtered_df["Baseline"], y=filtered_df["Milestone No."], name = 'Baseline',
                         line=dict(color='firebrick', width=1,dash='dot'), marker_symbol="circle"))

fig.add_trace(go.Scatter(x=filtered_df["Actual"], y=filtered_df["Milestone No."], name = 'Actual',
                         line=dict(color='green', width=1,dash='dot'), marker_symbol="diamond"))
#z = filtered_df['Variance']

fig.update_traces(hovertemplate= "Mls No. : %{y} , Date: %{x}")
#fig.update_traces(texttemplate="Mls No. :", selector=dict(type='scatter'))
fig.update_traces(textposition="bottom right")

fig.add_trace(go.Scatter(x=filtered_df["Status Date"], y=filtered_df["Milestone No."], name = 'Status Date',
                         line=dict(color='red', width=1,dash='dot'), mode = 'lines'))

# Edit the layout
fig.update_layout(title='', xaxis_title='Timeline', yaxis_title='Milestone No.')

# -- Input the Plotly chart to the Streamlit interface
st.plotly_chart(fig, use_container_width=True)

AgGrid(filtered_df, height=350, width=70, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS) 
