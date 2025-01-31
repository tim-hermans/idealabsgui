import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

from src.preprocessing.filtering import FIRFilter, IIRFilter
from src.utils.plotly import plot_time_series_ply
from scipy.signal import welch

st.title("Filtering")

st.write("## Filter design")

# First load data from session state (data is loaded on the Home page).
fs = st.session_state["fs"] if "fs" in st.session_state else None
eeg = st.session_state["eeg"] if "eeg" in st.session_state else None

# Stop execution if the value is not set
if not fs:
    st.warning("Please generate or upload data first.")
    st.stop()  # This will stop the execution here

# Common options.
col1, col2 = st.columns(2, gap="medium")
filter_type = col1.selectbox(
    "Filter type", options=("lowpass", "highpass", "bandpass", "bandstop")
)
if filter_type in ["lowpass", "highpass"]:
    # Only allow one cutoff input.
    cutoff = col2.number_input(
        label="cutoff (Hz)",
        step=1.0,
        value=float(round(fs / 2 / 2)),
        min_value=0.01,
        max_value=float(fs / 2) - 0.01,
    )
elif filter_type in ["bandpass", "bandstop"]:
    # Ask for two inputs.
    col11, col12 = col2.columns(2)
    cutoff_low = col11.number_input(
        label="Low cutoff (Hz)",
        step=1.0,
        value=float(round(fs / 2 / 4)),
        min_value=0.01,
        max_value=float(fs / 2) - 0.01,
    )
    cutoff_high = col12.number_input(
        label="High cutoff (Hz)",
        min_value=cutoff_low + 0.01,
        value=float(round(fs / 2 / 4 * 3)),
        step=1.0,
        max_value=float(fs / 2) - 0.01,
    )
    cutoff = [cutoff_low, cutoff_high]

# Type specific options.
col1, col2 = st.columns(2, gap="medium")

# Select filter type.
which_filter = col1.selectbox(label="FIR/IIR:", options=["FIR", "IIR"])

if which_filter == "FIR":
    col21, col22 = col2.columns(2)
    num_taps = col21.number_input(
        label="Filter length",
        min_value=1,
        max_value=int(4 * fs),
        step=2,
        value=fs // 8 * 2 + 1,
    )
    window = col22.selectbox(
        "Select FIR window",
        options=["hamming", "hann", "boxcar", "blackman", "bartlett"],
    )
    filter_obj = FIRFilter(
        filter_type=filter_type, cutoff=cutoff, fs=fs, num_taps=num_taps, window=window
    )

elif which_filter == "IIR":
    col21, col22 = col2.columns(2)
    order = col21.number_input(label="Filter order", min_value=1, max_value=20, step=1)
    ftype = col22.selectbox(
        "Select IIR type",
        options=["butter", "cheby1", "cheby2", "ellip", "bessel"],
    )
    filter_obj = IIRFilter(
        filter_type=filter_type,
        cutoff=cutoff,
        fs=fs,
        order=order,
        ftype=ftype,
    )
else:
    raise ValueError(f"Invalid `which_filter` {which_filter}.")

# Plot frequency response.
filter_obj.plot_filter_response_st()
# st.plotly_chart(fig_ply, use_container_width=True)

st.write("## Filter test signal")

# Filter eeg.
zero_phase = st.toggle("Zero-phase filter")
if zero_phase:
    # Use filtfilt for zero-phase filtering.
    eeg_filt = filter_obj.filtfilt(eeg)
else:
    # Normal, causal filtering.
    eeg_filt = filter_obj.filter(eeg)

# Plot the test data and filtered.
st.write("**Raw and filtered time series**")
fig_eeg = plot_time_series_ply(signal=eeg, fs=fs, label="Raw")
fig_eeg = plot_time_series_ply(signal=eeg_filt, fs=fs, label="Filtered", fig=fig_eeg)
st.plotly_chart(fig_eeg, use_container_width=True)

# Compute power spetra.
nperseg = max(256, len(eeg) // 8)
feeg, Peeg = welch(eeg, fs=fs, nperseg=nperseg)
feegfilt, Peegfilt = welch(eeg_filt, fs=fs, nperseg=nperseg)

# Convert to DataFrame for Streamlit
df1 = pd.DataFrame(
    {"Frequency (Hz)": feeg, "Power Spectral Density (V²/Hz)": Peeg, "Signal": "Raw"}
)
df2 = pd.DataFrame(
    {
        "Frequency (Hz)": feegfilt,
        "Power Spectral Density (V²/Hz)": Peegfilt,
        "Signal": "Filtered",
    }
)

# Combine both dataframes
df = pd.concat([df1, df2])

# Create Altair chart for interactive visualization
chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="Frequency (Hz):Q",
        y=alt.Y(
            "Power Spectral Density (V²/Hz):Q", scale=alt.Scale(type="log")
        ),  # Log scale for y-axis
        color=alt.Color("Signal:N", sort=["Raw", "Filtered"]),  # Change order here
    )
    .properties(width=700, height=400)
).interactive()

# Display the chart.
st.write("**Raw and filtered power spectra**")
st.altair_chart(chart, use_container_width=True)
