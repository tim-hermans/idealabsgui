import numpy as np


def generate_eeg(
    fs=250, duration=600, amplitude=75, f_low=0, f_high=20, n_f=50, seed=None
):
    """
    Generate a random toy EEG example.

    Args:
        fs (float, optional): sample frequency in Hz.
        duration (float, optional): duration in seconds.
        amplitude (float, optional): max amplitude of EEG signal.
        f_low (float, optional): minimum frequency to be present in the EEG (in Hz).
        f_high (float, optional): maximum frequency to be present in the EEG (in Hz).
        n_f (int, optional): number of frequencies to add to the EEG.
        seed (int, optional): seed for the random generator.

    Returns:
        signal (np.ndarray): 1D signal array.
    """
    # Seed random generator.
    np.random.seed(seed)

    # Number of samples.
    n_t = duration * fs

    # Frequencies in Hz.
    f_all = np.linspace(f_low + n_f / n_f, f_high, n_f)

    # Power law coefficient.
    k = 2
    weights_all = 1 * f_all ** (-k)
    weights_all[f_all < 1.5] = np.random.rand(np.sum(f_all < 1.5))

    lags_all = np.random.rand(n_f) * 2 * np.pi

    # Frequencies in rad/s.
    w_all = f_all * 2 * np.pi

    t = np.arange(n_t) / fs
    signal = np.zeros(n_t)

    moving_average_length = int(fs / 10)

    for a, w, phi in zip(weights_all, w_all, lags_all):
        random_factor = np.random.rand(n_t)
        random_factor = np.convolve(
            random_factor,
            np.ones(moving_average_length) / moving_average_length,
            mode="same",
        )
        signal += a * np.sin(w * t + phi) * random_factor

    signal *= amplitude
    return signal
