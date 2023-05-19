import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
import calendar
from st_aggrid import AgGrid, ColumnsAutoSizeMode
from streamlit_echarts import st_echarts, JsCode
import json

with st.sidebar:
    st.write("hello")
    
options1 = {
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {
        "data": ["Direct", "Mail Ad", "Affiliate Ad", "Video Ad", "Search Engine"]
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": {"type": "value"},
    "yAxis": {
        "type": "category",
        "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    },
    "series": [
        {
            "name": "Direct",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [320, 302, 301, 334, 390, 330, 320],
        },
        {
            "name": "Mail Ad",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [120, 132, 101, 134, 90, 230, 210],
        },
        {
            "name": "Affiliate Ad",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [220, 182, 191, 234, 290, 330, 310],
        },
        {
            "name": "Video Ad",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [150, 212, 201, 154, 190, 330, 410],
        },
        {
            "name": "Search Engine",
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [820, 832, 901, 934, 1290, 1330, 1320],
        },
    ],
}

st_echarts(options=options1, height="500px")

options2 = {
    "title": {"text": "Project"},
    "legend": {"data": ["Allocated Budget", "Actual Spending"]},
    "radar": {
        "indicator": [
            {"name": "Sales", "max": 6500},
            {"name": "Administration", "max": 16000},
            {"name": "Information Technology", "max": 30000},
            {"name": "Customer Support", "max": 38000},
            {"name": "Development", "max": 52000},
            {"name": "Marketing", "max": 25000},
        ]
    },
    "series": [
        {
            "name": "Budget vs spending",
            "type": "radar",
            "data": [
                {
                    "value": [4200, 3000, 20000, 35000, 50000, 18000],
                    "name": "Allocated Budget",
                },
                {
                    "value": [5000, 14000, 28000, 26000, 42000, 21000],
                    "name": "Actual Spending",
                },
            ],
        }
    ],
}
st_echarts(options2, height="500px")

with open("./life-expectancy.json") as f:
    raw_data = json.load(f)
countries = [
    "Finland",
    "France",
    "Germany",
    "Iceland",
    "Norway",
    "Poland",
    "Russia",
    "United Kingdom",
]

datasetWithFilters = [
    {
        "id": f"dataset_{country}",
        "fromDatasetId": "dataset_raw",
        "transform": {
            "type": "filter",
            "config": {
                "and": [
                    {"dimension": "Year", "gte": 1950},
                    {"dimension": "Country", "=": country},
                ]
            },
        },
    }
    for country in countries
]

seriesList = [
    {
        "type": "line",
        "datasetId": f"dataset_{country}",
        "showSymbol": False,
        "name": country,
        "endLabel": {
            "show": True,
            "formatter": st_echarts.JsCode(
                "function (params) { return params.value[3] + ': ' + params.value[0];}"
            ).js_code,
        },
        "labelLayout": {"moveOverlap": "shiftY"},
        "emphasis": {"focus": "series"},
        "encode": {
            "x": "Year",
            "y": "Income",
            "label": ["Country", "Income"],
            "itemName": "Year",
            "tooltip": ["Income"],
        },
    }
    for country in countries
]

options3 = {
    "animationDuration": 100,
    "dataset": [{"id": "dataset_raw", "source": raw_data}] + datasetWithFilters,
    "title": {"text": "Income in Europe since 1950"},
    "tooltip": {"order": "valueDesc", "trigger": "axis"},
    "xAxis": {"type": "category", "nameLocation": "middle"},
    "yAxis": {"name": "Income"},
    "grid": {"right": 140},
    "series": seriesList,
}
st_echarts(options3, height="600px")
    
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
