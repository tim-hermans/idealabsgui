"""
Main file for streamlit app.
To run this app:
streamlit run main.py
"""

import streamlit as st
import pandas as pd
import numpy as np

from src.utils.dummy_data import generate_eeg
from src.utils.plotly import plot_time_series_ply

# Insert a title.
st.title("IdeaLabs")

# Write welcome text.
st.write(
    "Welcome to the IdeaLabs interactive learning tool for EEG (pre)processing. Use the navigation bar on the left to learn about different aspectecs related to EEG research."
)

st.write("## Select test data")
st.write("Either generate random data, or upload your own.")

# Generate or load data.
container = st.container(border=True)  # Use a container to add borders.
col1, col2 = container.columns(
    2,
    gap="large",
)
col1.write("**Generate random signal**")
fs_generate = col1.number_input(
    "Sampling frequency (Hz):", value=100, key="fs_generate"
)
duration_generate = col1.number_input(
    "Duration (s):", value=100, step=1, key="duration_generate"
)
col2.write("**Upload signal**")
fs_upload = col2.number_input("Sampling frequency (Hz):", value=100, key="fs_upload")
uploaded_file = col2.file_uploader("Choose a csv file")

# Start with random data.
if "fs" not in st.session_state:
    st.session_state.fs = fs_generate
if "eeg" not in st.session_state:
    st.session_state.eeg = generate_eeg(
        fs=fs_generate, duration=duration_generate, seed=np.random.randint(1e3)
    )

if col1.button("(Re)generate"):
    # Regenerate random data and update variables in session state.
    st.session_state.fs = fs_generate
    st.session_state.eeg = generate_eeg(
        fs=fs_generate,
        duration=duration_generate,
        seed=np.random.randint(1e3),
    )

if uploaded_file:
    # Load data using pandas.
    raise NotImplementedError
    df = pd.read_csv(uploaded_file)
    which_data = "generated"

# Plot raw EEG.
eeg = st.session_state.eeg
fs = st.session_state.fs
if eeg is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="EEG duration", value=f"{len(eeg) / fs} s")
    col2.metric(label="Sampling rate", value=f"{len(eeg) / fs} Hz")
    col3.metric(label="\# samples", value=f"{len(eeg):,}")
    fig_raw = plot_time_series_ply(signal=eeg, fs=fs)
    st.plotly_chart(fig_raw, use_container_width=True)

st.image(image="assets/kuleuven.png", width=200)


# # Insert some text.
# st.write("Upload your data file below:")

# # File uploader widget.
# uploaded_file = st.file_uploader("Choose a csv file")

# # Display uploaded data if a file was chosen.
# if uploaded_file:
#     # Load data using pandas.
#     df = pd.read_csv(uploaded_file)

#     # Preview the data.
#     st.write("Data preview:", df.head())

#     # Define signal column to plot.
#     y_col = "ECG"

#     # # Select column to plot (exlude the time column).
#     # y_col = st.selectbox(label="Select a signal to plot:", options=df.columns[1:])

#     # Select multiple columns to plot (y_col is a list).
#     y_col = st.multiselect(label="Select signals to plot:", options=df.columns[1:])

#     # Simple plot using streamlits built-in plotting module.
#     st.line_chart(x="Time (s)", y=y_col, data=df)

#     # Plot using plotly.
#     st.write("Plotly:")
#     fig_ply = px.line(data_frame=df, x="Time (s)", y=y_col)
#     st.plotly_chart(fig_ply)
