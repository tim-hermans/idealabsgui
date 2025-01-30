"""
Basic example that loads a dataframe and plots it.
To run this app:
streamlit run main.py
"""
import plotly.express as px
import streamlit as st
import pandas as pd

# Insert a title.
st.title("Data visualization")

# Insert some text.
st.write("Upload your data file below:")

# File uploader widget.
uploaded_file = st.file_uploader("Choose a csv file")

# Display uploaded data if a file was chosen.
if uploaded_file:
    # Load data using pandas.
    df = pd.read_csv(uploaded_file)

    # Preview the data.
    st.write("Data preview:", df.head())

    # Define signal column to plot.
    y_col = 'ECG'

    # # Select column to plot (exlude the time column).
    # y_col = st.selectbox(label="Select a signal to plot:", options=df.columns[1:])

    # Select multiple columns to plot (y_col is a list).
    y_col = st.multiselect(label="Select signals to plot:", options=df.columns[1:])

    # Simple plot using streamlits built-in plotting module.
    st.line_chart(x='Time (s)', y=y_col, data=df)

    # Plot using plotly.
    st.write('Plotly:')
    fig_ply = px.line(data_frame=df, x='Time (s)', y=y_col)
    st.plotly_chart(fig_ply)
