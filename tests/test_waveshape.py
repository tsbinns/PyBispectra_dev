"""Tests for wave shape tools."""

import os

import pytest
import numpy as np
from numpy.random import RandomState

from pybispectra.waveshape import WaveShape
from pybispectra.utils import ResultsWaveShape, compute_fft
from pybispectra.utils._utils import _generate_data


def test_error_catch() -> None:
    """Check that WaveShape class catches errors."""
    n_chans = 3
    n_epochs = 5
    n_times = 100
    sampling_freq = 50
    data = _generate_data(n_epochs, n_chans, n_times)
    indices = ([0, 1, 2], [0, 1, 2])

    coeffs, freqs = compute_fft(data, sampling_freq)

    # initialisation
    with pytest.raises(TypeError, match="`data` must be a NumPy array."):
        WaveShape(coeffs.tolist(), freqs, sampling_freq)
    with pytest.raises(ValueError, match="`data` must be a 3D array."):
        WaveShape(np.random.randn(2, 2), freqs, sampling_freq)

    with pytest.raises(TypeError, match="`freqs` must be a NumPy array."):
        WaveShape(coeffs, freqs.tolist(), sampling_freq)
    with pytest.raises(ValueError, match="`freqs` must be a 1D array."):
        WaveShape(coeffs, np.random.randn(2, 2), sampling_freq)

    with pytest.raises(
        ValueError,
        match=(
            "`data` and `freqs` must contain the same number of frequencies."
        ),
    ):
        WaveShape(coeffs, freqs[:-1], sampling_freq)

    with pytest.raises(ValueError, match="Entries of `freqs` must be >= 0."):
        WaveShape(coeffs, freqs * -1, sampling_freq)
    with pytest.raises(
        ValueError,
        match=(
            "Entries of `freqs` corresponding to positive frequencies must be "
            "in ascending order."
        ),
    ):
        WaveShape(coeffs, freqs[::-1], sampling_freq)

    with pytest.raises(TypeError, match="`verbose` must be a bool."):
        WaveShape(coeffs, freqs, sampling_freq, "verbose")

    # compute
    waveshape = WaveShape(coeffs, freqs, sampling_freq)

    with pytest.raises(TypeError, match="`indices` must be a tuple."):
        waveshape.compute(indices=list(indices))
    with pytest.raises(TypeError, match="Entries of `indices` must be ints."):
        waveshape.compute(indices=(0.0, 1.0))
    with pytest.raises(
        ValueError,
        match=(
            "`indices` contains indices for channels not present in the data."
        ),
    ):
        waveshape.compute(indices=(0, 99))

    with pytest.raises(
        TypeError, match="`f1s` and `f2s` must be NumPy arrays."
    ):
        waveshape.compute(f1s=freqs.tolist())
    with pytest.raises(
        TypeError, match="`f1s` and `f2s` must be NumPy arrays."
    ):
        waveshape.compute(f2s=freqs.tolist())
    with pytest.raises(ValueError, match="`f1s` and `f2s` must be 1D arrays."):
        waveshape.compute(f1s=np.random.rand(2, 2))
    with pytest.raises(ValueError, match="`f1s` and `f2s` must be 1D arrays."):
        waveshape.compute(f2s=np.random.rand(2, 2))
    with pytest.raises(
        ValueError,
        match=(
            "All frequencies in `f1s` and `f2s` must be present in the data."
        ),
    ):
        waveshape.compute(f1s=freqs * -1)
    with pytest.raises(
        ValueError,
        match=(
            "All frequencies in `f1s` and `f2s` must be present in the data."
        ),
    ):
        waveshape.compute(f2s=freqs * -1)
    with pytest.raises(
        ValueError, match="Entries of `f1s` must be in ascending order."
    ):
        waveshape.compute(f1s=freqs[::-1])
    with pytest.raises(
        ValueError, match="Entries of `f2s` must be in ascending order."
    ):
        waveshape.compute(f2s=freqs[::-1])

    with pytest.raises(TypeError, match="`n_jobs` must be an integer."):
        waveshape.compute(n_jobs=0.5)
    with pytest.raises(ValueError, match="`n_jobs` must be >= 1 or -1."):
        waveshape.compute(n_jobs=0)


def test_waveshape_runs() -> None:
    """Test that WaveShape runs correctly."""
    n_chans = 3
    sampling_freq = 50
    data = _generate_data(5, n_chans, 100)

    fft, freqs = compute_fft(data=data, sampling_freq=sampling_freq)

    # check it runs with correct inputs
    waveshape = WaveShape(data=fft, freqs=freqs, sampling_freq=sampling_freq)
    waveshape.compute()

    # check the returned results have the correct shape
    assert waveshape.results.shape == (n_chans, len(freqs), len(freqs))

    # check the returned results are of the correct type
    assert waveshape.results.name == "Wave Shape"
    assert isinstance(waveshape.results, ResultsWaveShape)


def test_waveshape_results():
    """Test that WaveShape returns the correct results.

    Simulated data with 10 Hz (plus harmonics) wave shape features is used.
    Wave shape features include a ramp up sawtooth, ramp down sawtooth,
    peak-dominant signal, and a trough-dominant signal.
    """
    # tolerance for "closeness"
    close_atol = 0.1

    # identify frequencies of wave shape features (~10 Hz and harmonics)
    focal_freqs = np.array([10, 20, 30])
    all_freqs = np.arange(0, 36)

    # test that genuine PAC is detected
    # load simulated data with bivariate PAC interactions
    data_sawtooths = np.load(
        os.path.join(
            "..", "examples", "data", "sim_data_waveshape_sawtooths.npy"
        )
    )
    data_peaks_troughs = np.load(
        os.path.join(
            "..", "examples", "data", "sim_data_waveshape_peaks_troughs.npy"
        )
    )
    sampling_freq = 1000  # sampling frequency in Hz

    # add noise for numerical stability
    random = RandomState(44)
    snr = 0.25
    datasets = [data_sawtooths, data_peaks_troughs]
    for data_idx, data in enumerate(datasets):
        datasets[data_idx] = snr * data + (1 - snr) * random.rand(*data.shape)
    data_sawtooths = datasets[0]
    data_peaks_troughs = datasets[1]

    # compute FFT
    coeffs_sawtooths, freqs = compute_fft(
        data=data_sawtooths,
        sampling_freq=sampling_freq,
        n_points=sampling_freq,
    )
    coeffs_peaks_troughs, freqs = compute_fft(
        data=data_peaks_troughs,
        sampling_freq=sampling_freq,
        n_points=sampling_freq,
    )

    # sawtooth waves
    waveshape_sawtooths = WaveShape(
        data=coeffs_sawtooths, freqs=freqs, sampling_freq=sampling_freq
    )
    waveshape_sawtooths.compute(f1s=all_freqs, f2s=all_freqs)
    results_sawtooths = waveshape_sawtooths.results.get_results()

    # peaks and troughs
    waveshape_peaks_troughs = WaveShape(
        data=coeffs_peaks_troughs, freqs=freqs, sampling_freq=sampling_freq
    )
    waveshape_peaks_troughs.compute(f1s=all_freqs, f2s=all_freqs)
    results_peaks_troughs = waveshape_peaks_troughs.results.get_results()

    # check that sawtooth features are detected
    for results, real_val, imag_val, phase in zip(
        results_sawtooths, [0, 0], [1, -1], [0.5, 1.5]
    ):
        assert np.isclose(
            np.nanmean(np.real(results[np.ix_(focal_freqs, focal_freqs)])),
            real_val,
            atol=close_atol,
        )
        assert np.isclose(
            np.nanmean(np.imag(results[np.ix_(focal_freqs, focal_freqs)])),
            imag_val,
            atol=close_atol,
        )
        # normalise phase to [0, 2) in units of pi
        phases = np.angle(results[np.ix_(focal_freqs, focal_freqs)])
        phases[phases < 0] += 2 * np.pi
        phases /= np.pi
        assert np.isclose(
            np.nanmean(phases),
            phase,
            atol=close_atol,
        )

    # check that peak/trough features are detected
    for results, real_val, imag_val, phase in zip(
        results_peaks_troughs, [1, -1], [0, 0], [0, 1]
    ):
        assert np.isclose(
            np.nanmean(np.real(results[np.ix_(focal_freqs, focal_freqs)])),
            real_val,
            atol=close_atol,
        )
        assert np.isclose(
            np.nanmean(np.imag(results[np.ix_(focal_freqs, focal_freqs)])),
            imag_val,
            atol=close_atol,
        )
        # normalise phase to [0, 2) in units of pi
        # take abs value of angle to account for phase wrapping (at 0, 2 pi)
        phases = np.abs(np.angle(results[np.ix_(focal_freqs, focal_freqs)]))
        phases[phases < 0] += 2 * np.pi
        phases /= np.pi
        assert np.isclose(
            np.nanmean(phases),
            phase,
            atol=close_atol,
        )