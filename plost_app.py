import streamlit as st
import pandas as pd
import plost

# Title of the app
st.title("Sample Plost Bar Chart")

# Create a DataFrame (required by plost)
data = pd.DataFrame({
    'fruit': ['Apples', 'Bananas', 'Cherries'],
    'count': [10, 20, 15]
})

# Render the bar chart using plost
plost.bar_chart(
    data=data,
    bar='fruit',
    value='count',
    title='Fruit Count'
)
