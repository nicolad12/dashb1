import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
import calendar
 
#-- Create three columns
col1, col2, col3 = st.columns([5, 10, 20])
st.title("Key Milestones Time Chart")

month_choice = st.slider(
        "What month would you like to view?",
        min_value=6,
        max_value=12,
        step=1,
        value=6,
    )

year_choice = st.slider(
        "What year would you like to view?",
        min_value=2022,
        max_value=2026,
        step=1,
        value=2022,
    )

df = df = pd.read_excel('https://docs.google.com/spreadsheets/d/1VVjVXYmnDr20f1FjXNYBtglFrPTlJvAu/edit?usp=sharing&ouid=105566543575107705244&rtpof=true&sd=true')
# -- Apply the year filter given by the user
res = calendar.monthrange(year_choice, month_choice)[1]
date = datetime.date(year_choice,month_choice,res)
filtered_df = df[(df['Status Date'] == str(date))]


# -- Create the figure in Plotly
fig = go.Figure()
#fig = px.line(
#    filtered_df,
#    x="Baseline",
#    y="Milestone No.",
#    hover_name="Baseline",
#    markers = True,
#    text = "Milestone No."
#)

fig.add_trace(go.Scatter(x=filtered_df["Forecast"], y=filtered_df["Milestone No."], name = 'Forecast',
                         line=dict(color='royalblue', width=1),marker_symbol="square"))
fig.update_traces(text=filtered_df["Milestone No."], mode='lines+markers+text')

fig.add_trace(go.Scatter(x=filtered_df["Baseline"], y=filtered_df["Milestone No."], name = 'Baseline',
                         line=dict(color='firebrick', width=1,dash='dot'), marker_symbol="circle"))

fig.add_trace(go.Scatter(x=filtered_df["Actual"], y=filtered_df["Milestone No."], name = 'Actual',
                         line=dict(color='green', width=1,dash='dot'), marker_symbol="diamond"))
z = filtered_df['Variance']

fig.update_traces(hovertemplate= "Mls No. : %{y} , Date: %{x}")
#fig.update_traces(texttemplate="Mls No. :", selector=dict(type='scatter'))
fig.update_traces(textposition="bottom right")

fig.add_trace(go.Scatter(x=filtered_df["Status Date"], y=filtered_df["Milestone No."], name = 'Status Date',
                         line=dict(color='red', width=1,dash='dot'), mode = 'lines'))

# Edit the layout
fig.update_layout(title='', xaxis_title='Timeline', yaxis_title='Milestone No.')

# -- Input the Plotly chart to the Streamlit interface
st.plotly_chart(fig, use_container_width=True)
