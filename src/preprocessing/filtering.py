import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import altair as alt


class FilterBase:
    def compute_response():
        raise NotImplementedError

    def plot_filter_response_plt(self, ax=None):
        """Plot the frequency response of the filter."""
        f, h = self.compute_response()

        if ax is None:
            ax = plt.gca()
        ax.plot(f, 20 * np.log10(abs(h)))
        ax.set_title("Filter Frequency Response")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude (dB)")
        ax.set_ylim([-120, 1])
        ax.grid(True)

        return ax

    def plot_filter_response_st(self):
        """Plot the frequency response of the filter using Streamlit's native plotting functions."""
        # f, h = self.compute_response()
        # data = pd.DataFrame(
        #     {"Frequency (Hz)": f, "Magnitude (dB)": 20 * np.log10(abs(h))}
        # )
        # st.line_chart(data.set_index("Frequency (Hz)"))

        st.altair_chart(self.plot_filter_response_alt(), use_container_width=True)

    def plot_filter_response_alt(self):
        """Plot the frequency response of the filter using Altair."""
        f, h = self.compute_response()
        data = pd.DataFrame(
            {"Frequency (Hz)": f, "Magnitude (dB)": 20 * np.log10(abs(h))}
        )

        # Create the Altair plot
        chart = (
            (
                alt.Chart(data)
                .mark_line()
                .encode(x="Frequency (Hz):Q", y="Magnitude (dB):Q")
                .properties(
                    title="Filter Frequency Response",
                    height=400,  # Set a fixed height for the plot
                )
                .configure_axis(grid=True)
                .configure_view(
                    strokeWidth=0  # Removes border around the plot
                )
                .configure_title(fontSize=16)
            )
            .encode(y=alt.Y("Magnitude (dB):Q", scale=alt.Scale(domain=[-120, 1])))
            .interactive()
        )

        return chart

    def plot_filter_response_ply(self):
        """Plot the frequency response of the filter using Plotly."""
        f, h = self.compute_response()
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=f, y=20 * np.log10(abs(h)), mode="lines", name="Magnitude Response"
            )
        )
        fig.update_layout(
            title="FIR Filter Frequency Response",
            xaxis_title="Frequency (Hz)",
            yaxis_title="Magnitude (dB)",
            yaxis=dict(range=[-120, 1]),
        )

        return fig


class FIRFilter(FilterBase):
    def __init__(
        self,
        filter_type,
        cutoff,
        fs,
        num_taps,
        window="hamming",
    ):
        """
        Design FIR filter.

        Args:
            filter_type (str): type of filter ('lowpass', 'highpass', 'bandpass', 'bandstop').
            cutoff (float or list): cutoff frequency in Hz (or frequencies for bandpass/bandstop).
            fs (float): sampling frequency of signal to filter (Hz).
            num_taps (int): number of filter coefficients (choose odd number).
            window (str, optional): window function for filter design.
        """
        # Check input.
        if not isinstance(filter_type, str):
            raise TypeError(f"`file_type` must be a str. Got a {type(filter_type)}.")
        filter_type = filter_type.lower()
        if filter_type not in ["bandpass", "lowpass", "highpass", "bandstop"]:
            raise ValueError(
                f"filter_type must be one of {['bandpass', 'lowpass', 'highpass', 'bandstop']}. Got filter_type={filter_type}."
            )

        self.filter_type = filter_type
        self.cutoff = np.atleast_1d(cutoff)
        self.fs = fs
        self.num_taps = num_taps
        self.window = window

        # Compute filter coefficients.
        self.coefficients = self.design_filter()

    def design_filter(self):
        """Design the FIR filter using the chosen parameters."""
        return signal.firwin(
            numtaps=self.num_taps,
            cutoff=self.cutoff,
            fs=self.fs,
            window=self.window,
            pass_zero=self.filter_type,  # Works with filter_type as input.
        )

    def filter(self, data, **kwargs):
        """Apply the FIR filter to input data."""
        return signal.lfilter(self.coefficients, 1.0, data, **kwargs)

    def filtfilt(self, data, **kwargs):
        """Zero-phase filtering."""
        return signal.filtfilt(self.coefficients, 1.0, data, **kwargs)

    def compute_response(self):
        f, h = signal.freqz(self.coefficients, worN=8000, fs=self.fs)
        return f, h


class IIRFilter(FilterBase):
    def __init__(self, filter_type, cutoff, fs, order, ftype="butter"):
        """
        Design an IIR filter.

        Args:
            filter_type (str): type of filter ('lowpass', 'highpass', 'bandpass', 'bandstop').
            cutoff (float or list): cutoff frequency in Hz (or frequencies for bandpass/bandstop).
            fs (float): sampling frequency of signal to filter (Hz).
            order (int): filter order.
            ftype (str, optional): type of IIR filter ('butter', 'cheby1', 'cheby2', 'ellip', 'bessel').
        """
        self.filter_type = filter_type
        self.cutoff = np.atleast_1d(cutoff)
        self.fs = fs
        self.order = order
        self.ftype = ftype

        # Compute filter coefficients.
        self.sos = self.design_filter()

    def design_filter(self):
        """Design the IIR filter using the chosen parameters."""
        return signal.iirfilter(
            N=self.order,
            Wn=self.cutoff,
            btype=self.filter_type,
            ftype=self.ftype,
            fs=self.fs,
            output="sos",  # Preferred for numerical stability.
        )

    def filter(self, data, **kwargs):
        """Apply the IIR filter to input data."""
        return signal.sosfilt(self.sos, data, **kwargs)

    def filtfilt(self, data, **kwargs):
        """Zero-phase filtering."""
        return signal.sosfiltfilt(self.sos, data, **kwargs)

    def compute_response(self):
        f, h = signal.sosfreqz(self.sos, worN=8000, fs=self.fs)
        return f, h


# Example usage
if __name__ == "__main__":
    fs = 1000  # Sampling frequency in Hz
    cutoff = [100, 300]  # Cutoff frequencies for bandpass filter
    fir_filter = FIRFilter(filter_type="bandpass", cutoff=cutoff, fs=fs, num_taps=101)
    fir_filter.plot_filter_response_plt()

    iir_filter = IIRFilter(filter_type="bandpass", cutoff=cutoff, fs=fs, order=4)
    fig = iir_filter.plot_filter_response_ply()
    fig.show()
