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
    "Duration (s):", value=10, step=1, key="duration_generate"
)
col2.write("**Upload signal**")
fs_upload = col2.number_input("Sampling frequency (Hz):", value=100, key="fs_upload")
uploaded_file = col2.file_uploader("Choose a csv file")
if uploaded_file:
    button_load = col2.button("(Re)load")
else:
    button_load = None

if col1.button("(Re)generate"):
    # Regenerate random data.
    fs = fs_generate
    eeg = generate_eeg(
        fs=fs_generate,
        duration=duration_generate,
        seed=np.random.randint(1e3),
    )

elif button_load and uploaded_file:
    # Load data using pandas.
    df = pd.read_csv(uploaded_file, header=None)
    fs = fs_upload
    eeg = np.asarray(df.values).squeeze()
    if eeg.ndim != 1:
        raise ValueError(f"`Loaded data should be 1D. Got data shape {eeg.shape}.")

else:
    # Extract or generate data if there is or is not data in session state.
    if "fs" not in st.session_state:
        fs = fs_generate
    else:
        fs = st.session_state["fs"]
    if "eeg" not in st.session_state:
        eeg = generate_eeg(
            fs=fs_generate, duration=duration_generate, seed=np.random.randint(1e3)
        )
    else:
        eeg = st.session_state["eeg"]

# Check for large data sizes.
if len(eeg) > 1e6:
    # Limit data size.
    st.warning(f"Limited the data size to {1e6} samples.")
    eeg = eeg[:1e6]

# Update variables in session state.
st.session_state.fs = fs
st.session_state.eeg = eeg

# Plot raw EEG.
if eeg is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Sampling rate", value=f"{fs} Hz")
    col2.metric(label="EEG duration", value=f"{len(eeg) / fs} s")
    col3.metric(label="\# samples", value=f"{len(eeg):,}")
    fig_raw = plot_time_series_ply(signal=eeg, fs=fs)
    st.plotly_chart(fig_raw, use_container_width=True)

st.image(image="assets/kuleuven.png", width=200)
