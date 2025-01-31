import numpy as np
import plotly.graph_objects as go


def plot_time_series_ply(signal, fs, label=None, t0=0, x_label="Time (s)", y_label="Signal", fig=None):
    """
    Plot single time series signal in plotly.

    Args:
        signal (array-like): signal.
        fs (float): samplng frequency (Hz).
        label (str, optional): name for the time series.
        t0 (int, optional): time offset (seconds).
        x_label (str, optional): xlabel.
        y_label (str, optional): ylabel.
    """
    signal = np.asarray(signal)
    if signal.ndim != 1:
        raise ValueError(
            f"`signal` should be 1D, but got an array with shape {signal.shape}."
        )
    time = np.arange(len(signal)) / fs + t0

    if fig is None:
        fig = go.Figure()
        
    fig.add_trace(
        go.Scatter(
            x=time,
            y=signal,
            mode="lines",
            name=label,
        )
    )
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        margin=dict(t=20, b=20, l=0, r=0),  # Reduce the margins
    )

    return fig
