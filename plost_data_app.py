import streamlit as st
import pandas as pd
import plost

# Set page config
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Load custom CSS
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar Header
st.sidebar.header('Dashboard version 2')

# --- Data Source Selection ---
st.sidebar.subheader("Data Source")
data_source = st.sidebar.radio("Choose data source:", ("Use default data", "Upload your own"))

# Load data
if data_source == "Upload your own":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            seattle_weather = pd.read_csv(uploaded_file, parse_dates=['date'])
            st.success("Custom data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()
    else:
        st.warning("Please upload a CSV file.")
        st.stop()
else:
    seattle_weather = pd.read_csv(
        'seattle-weather.csv',
        parse_dates=['date']
    )

# --- Date Filter ---
st.sidebar.subheader("Date Filter")
min_date = seattle_weather['date'].min()
max_date = seattle_weather['date'].max()
date_range = st.sidebar.date_input("Select date range:", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range)
    seattle_weather = seattle_weather[(seattle_weather['date'] >= start_date) & (seattle_weather['date'] <= end_date)]

# --- Visualization Controls ---
# Heat map
st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max'))

# Donut chart
st.sidebar.subheader('Donut chart parameter')
donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

# Line chart
st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect("Select data", ['temp_min', 'temp_max'], default=['temp_min', 'temp_max'])
plot_height = st.sidebar.slider("Specify plot height", 200, 500, 250)

# Sidebar Footer
st.sidebar.markdown("""
---
Created with ❤️ by [Ezekiel Mbaya](https://www.linkedin.com/in/ezekiel-ibrahim-866a1915b)
""")

# --- Row A: Metrics ---
st.markdown('# Weather Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# --- Load Stocks Dataset (for Donut) ---
stocks = pd.read_csv('stocks_toy.csv')

# --- Row B: Visualizations ---
c1, c2 = st.columns((7, 3))

with c1:
    st.markdown('### Heatmap')
    plost.time_hist(
        data=seattle_weather,
        date='date',
        x_unit='week',
        y_unit='day',
        color=time_hist_color,
        aggregate='median',
        legend=None,
        height=345,
        use_container_width=True
    )

with c2:
    st.markdown('### Donut Chart')
    plost.donut_chart(
        data=stocks,
        theta=donut_theta,
        color='company',
        legend='bottom',
        use_container_width=True
    )

# --- Row C: Line Chart ---
st.markdown('### Line Chart')

# Ensure 'date' is the index for line_chart
line_df = seattle_weather.set_index('date')[plot_data]
st.line_chart(line_df, height=plot_height)
