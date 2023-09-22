"""Tests for results classes (plotting tested separately)."""

import matplotlib
import pytest
import numpy as np
from matplotlib import pyplot as plt

from pybispectra.utils import ResultsCFC, ResultsTDE, ResultsWaveShape
from pybispectra.utils._utils import _generate_data


# interactive backends can fail seemingly randomly when using pytest, even if
# plt.show() not called, so stick to non-interactive backend
matplotlib.use("Agg")


def test_plotting_cfc_error_catch() -> None:
    """Test plotting in `ResultsCFC` catches errors."""
    n_cons = 9
    n_f1 = 50
    n_f2 = 50
    data = _generate_data(n_cons, n_f1, n_f2)
    f1s = np.arange(n_f1)
    f2s = np.arange(n_f2)
    name = "test"
    n_unique_chans = 3
    indices = (
        tuple(np.repeat(np.arange(n_unique_chans), n_unique_chans).tolist()),
        tuple(np.tile(np.arange(n_unique_chans), n_unique_chans).tolist()),
    )

    results = ResultsCFC(
        data=data,
        indices=indices,
        f1s=f1s,
        f2s=f2s,
        name=name,
    )

    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(nodes=9)
    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(
            nodes=(float(i) for i in range(n_cons)),
        )
    with pytest.raises(
        ValueError, match="The requested node is not present in the results."
    ):
        results.plot(nodes=(-1,))

    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_rows=0.5)
    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_cols=0.5)

    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_rows=0)
    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_cols=0)

    with pytest.raises(TypeError, match="`f1s` and `f2s` must be tuples."):
        results.plot(f1s=0)
    with pytest.raises(TypeError, match="`f1s` and `f2s` must be tuples."):
        results.plot(f2s=0)

    with pytest.raises(
        ValueError, match="`f1s` and `f2s` must have lengths of 2."
    ):
        results.plot(f1s=(f1s[0], f1s[1], f1s[2]))
    with pytest.raises(
        ValueError, match="`f1s` and `f2s` must have lengths of 2."
    ):
        results.plot(f2s=(f2s[0], f2s[1], f2s[2]))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f1s`.",
    ):
        results.plot(f1s=(20, 10))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f1s`.",
    ):
        results.plot(f1s=(10.1, 10.2))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f2s`.",
    ):
        results.plot(f2s=(20, 10))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f2s`.",
    ):
        results.plot(f2s=(10.1, 10.2))

    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(major_tick_intervals="5")
    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(minor_tick_intervals="1")
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(major_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(minor_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=r"`major_tick_intervals` should be \> `minor_tick_intervals`.",
    ):
        results.plot(major_tick_intervals=5, minor_tick_intervals=7)

    with pytest.raises(
        TypeError, match="`cbar_range` must be a list, tuple, or None."
    ):
        results.plot(cbar_range=np.array([0, 1]))
    with pytest.raises(
        ValueError,
        match=(
            "If `cbar_range` is a list, one entry must be provided for each "
            "node being plotted."
        ),
    ):
        results.plot(cbar_range=[None])
    with pytest.raises(
        ValueError, match="Limits in `cbar_range` must have length of 2."
    ):
        results.plot(cbar_range=(0, 1, 2))
    with pytest.raises(
        ValueError, match="Limits in `cbar_range` must have length of 2."
    ):
        results.plot(cbar_range=[(0, 1, 2) for _ in range(n_cons)])


def test_plotting_cfc_runs() -> None:
    """Test plotting in `ResultsCFC` runs with correct inputs."""
    n_cons = 9
    n_f1 = 50
    n_f2 = 50
    data = _generate_data(n_cons, n_f1, n_f2)
    f1s = np.arange(n_f1)
    f2s = np.arange(n_f2)
    name = "test"
    n_unique_chans = 3
    indices = (
        tuple(np.repeat(np.arange(n_unique_chans), n_unique_chans).tolist()),
        tuple(np.tile(np.arange(n_unique_chans), n_unique_chans).tolist()),
    )

    results = ResultsCFC(
        data=data,
        indices=indices,
        f1s=f1s,
        f2s=f2s,
        name=name,
    )

    figs, axes = results.plot(show=False)
    assert len(figs) == n_cons
    assert len(axes) == n_cons
    plt.close()

    figs, axes = results.plot(n_rows=3, n_cols=3, show=False)
    assert len(figs) == 1
    assert len(axes) == 1
    assert axes[0].size == n_cons
    plt.close()

    figs, axes = results.plot(
        f1s=(f1s[0], f1s[-1]), f2s=(f2s[0], f2s[-1]), show=False
    )
    plt.close()

    # check it works with non-exact frequencies
    figs, axes = results.plot(
        f1s=(10.25, 19.75), f2s=(10.25, 19.75), show=False
    )
    plt.close()


def test_plotting_TDE_error_catch() -> None:
    """Test plotting in `ResultsTDE` catches errors."""
    n_cons = 9
    n_times = 51
    data = _generate_data(n_cons, n_times, 1)[..., 0]
    times = np.arange((n_times - 1) * -0.5, n_times * 0.5)
    name = "test"
    n_unique_chans = 3
    indices = (
        tuple(np.repeat(np.arange(n_unique_chans), n_unique_chans).tolist()),
        tuple(np.tile(np.arange(n_unique_chans), n_unique_chans).tolist()),
    )

    results = ResultsTDE(
        data=data,
        indices=indices,
        times=times,
        name=name,
    )

    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(nodes=9)
    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(nodes=(float(i) for i in range(n_cons)))
    with pytest.raises(
        ValueError, match="The requested node is not present in the results."
    ):
        results.plot(nodes=(-1,))

    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_rows=0.5)
    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_cols=0.5)

    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_rows=0)
    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_cols=0)

    with pytest.raises(TypeError, match="`times` must be a tuple."):
        results.plot(times=0)
    with pytest.raises(ValueError, match="`times` must have length of 2."):
        results.plot(times=(times[0], times[1], times[2]))
    with pytest.raises(
        ValueError,
        match=(
            "At least one entry of `times` is outside the range of the "
            "results."
        ),
    ):
        results.plot(times=(times[0] - 1, times[-1]))
    with pytest.raises(
        ValueError,
        match=(
            "At least one entry of `times` is outside the range of the "
            "results."
        ),
    ):
        results.plot(times=(times[0], times[-1] + 1))
    with pytest.raises(
        ValueError,
        match=("No times are present in the data for the range in `times`."),
    ):
        results.plot(times=(times[-1], times[0]))
    with pytest.raises(
        ValueError,
        match=("No times are present in the data for the range in `times`."),
    ):
        results.plot(times=(0.1, 0.2))

    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(major_tick_intervals="5")
    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(minor_tick_intervals="1")
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(major_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(minor_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=r"`major_tick_intervals` should be \> `minor_tick_intervals`.",
    ):
        results.plot(major_tick_intervals=5, minor_tick_intervals=7)


def test_plotting_tde_runs() -> None:
    """Test plotting in `ResultsTDE` runs with correct inputs."""
    n_cons = 9
    n_times = 51
    data = _generate_data(n_cons, n_times, 1)[..., 0]
    times = np.arange((n_times - 1) * -0.5, n_times * 0.5)
    name = "test"
    n_unique_chans = 3
    indices = (
        tuple(np.repeat(np.arange(n_unique_chans), n_unique_chans).tolist()),
        tuple(np.tile(np.arange(n_unique_chans), n_unique_chans).tolist()),
    )

    results = ResultsTDE(
        data=data,
        indices=indices,
        times=times,
        name=name,
    )

    figs, axes = results.plot(show=False)
    assert len(figs) == n_cons
    assert len(axes) == n_cons
    plt.close()

    figs, axes = results.plot(n_rows=3, n_cols=3, show=False)
    assert len(figs) == 1
    assert len(axes) == 1
    assert axes[0].size == n_cons
    plt.close()

    figs, axes = results.plot(times=(times[0], times[-1]), show=False)
    plt.close()

    if results.tau[0] == times[-1]:
        figs, axes = results.plot(
            nodes=(0,), times=(times[0], results.tau[0] - 1), show=False
        )
    else:
        figs, axes = results.plot(
            nodes=(0,), times=(results.tau[0] + 1, times[-1]), show=False
        )
    plt.close()

    # check it works with non-exact times
    figs, axes = results.plot(
        times=(times[0] + 1e-5, times[-1] - 1e-5),
        show=False,
    )
    plt.close()


def test_plotting_waveshape_error_catch() -> None:
    """Test plotting in `ResultsWaveShape` catches errors."""
    n_chans = 3
    n_f1 = 50
    n_f2 = 50
    data = _generate_data(n_chans, n_f1, n_f2)
    f1s = np.arange(n_f1)
    f2s = np.arange(n_f2)
    name = "test"
    indices = tuple(range(n_chans))

    results = ResultsWaveShape(
        data=data,
        indices=indices,
        f1s=f1s,
        f2s=f2s,
        name=name,
    )

    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(nodes=9)
    with pytest.raises(
        TypeError, match="`nodes` must be a tuple of integers."
    ):
        results.plot(nodes=(float(i) for i in range(n_chans)))
    with pytest.raises(
        ValueError, match="The requested node is not present in the results."
    ):
        results.plot(nodes=(-1,))

    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_rows=0.5)
    with pytest.raises(
        TypeError, match="`n_rows` and `n_cols` must be integers."
    ):
        results.plot(n_cols=0.5)

    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_rows=0)
    with pytest.raises(
        ValueError, match="`n_rows` and `n_cols` must be >= 1."
    ):
        results.plot(n_cols=0)

    with pytest.raises(TypeError, match="`f1s` and `f2s` must be tuples."):
        results.plot(f1s=0)
    with pytest.raises(TypeError, match="`f1s` and `f2s` must be tuples."):
        results.plot(f2s=0)

    with pytest.raises(
        ValueError, match="`f1s` and `f2s` must have lengths of 2."
    ):
        results.plot(f1s=(f1s[0], f1s[1], f1s[2]))
    with pytest.raises(
        ValueError, match="`f1s` and `f2s` must have lengths of 2."
    ):
        results.plot(f2s=(f2s[0], f2s[1], f2s[2]))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f1s`.",
    ):
        results.plot(f1s=(20, 10))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f1s`.",
    ):
        results.plot(f1s=(10.1, 10.2))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f2s`.",
    ):
        results.plot(f2s=(20, 10))
    with pytest.raises(
        ValueError,
        match="No frequencies are present in the data for the range in `f2s`.",
    ):
        results.plot(f2s=(10.1, 10.2))

    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(major_tick_intervals="5")
    with pytest.raises(
        TypeError,
        match=(
            "`major_tick_intervals` and `minor_tick_intervals` should be ints "
            "or floats."
        ),
    ):
        results.plot(minor_tick_intervals="1")
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(major_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=(
            r"`major_tick_intervals` and `minor_tick_intervals` should be \> "
            "0."
        ),
    ):
        results.plot(minor_tick_intervals=0)
    with pytest.raises(
        ValueError,
        match=r"`major_tick_intervals` should be \> `minor_tick_intervals`.",
    ):
        results.plot(major_tick_intervals=5, minor_tick_intervals=7)

    cbar_names = ["abs", "real", "imag", "phase"]
    for cbar_name in cbar_names:
        kwarg_name = f"cbar_range_{cbar_name}"
        with pytest.raises(
            TypeError, match=f"`{kwarg_name}` must be a list, tuple, or None."
        ):
            results.plot(**{kwarg_name: np.array([0, 1])})
        with pytest.raises(
            ValueError,
            match=(
                f"If `{kwarg_name}` is a list, one entry must be provided "
                "for each node being plotted."
            ),
        ):
            results.plot(**{kwarg_name: [None]})
        with pytest.raises(
            ValueError,
            match=f"Limits in `{kwarg_name}` must have length of 2.",
        ):
            results.plot(**{kwarg_name: (0, 1, 2)})
        with pytest.raises(
            ValueError,
            match=f"Limits in `{kwarg_name}` must have length of 2.",
        ):
            results.plot(**{kwarg_name: [(0, 1, 2) for _ in range(n_chans)]})

    with pytest.raises(TypeError, match="`plot_absolute` must be a bool."):
        results.plot(plot_absolute=None)


def test_plotting_waveshape_runs() -> None:
    """Test plotting in `ResultsWaveShape` runs with correct inputs."""
    n_chans = 9
    n_f1 = 50
    n_f2 = 50
    data = _generate_data(n_chans, n_f1, n_f2)
    f1s = np.arange(n_f1)
    f2s = np.arange(n_f2)
    name = "test"
    indices = tuple(range(n_chans))

    results = ResultsWaveShape(
        data=data,
        indices=indices,
        f1s=f1s,
        f2s=f2s,
        name=name,
    )

    figs, axes = results.plot(show=False)
    assert len(figs) == n_chans
    assert len(axes) == n_chans
    plt.close()

    figs, axes = results.plot(n_rows=3, n_cols=3, show=False)
    assert len(figs) == 1
    assert len(axes) == 1
    assert axes[0].shape == (n_chans, 4)
    plt.close()

    figs, axes = results.plot(
        f1s=(f1s[0], f1s[-1]), f2s=(f2s[0], f2s[-1]), show=False
    )
    plt.close()

    # check it works with non-exact frequencies
    figs, axes = results.plot(
        f1s=(10.25, 19.75), f2s=(10.25, 19.75), show=False
    )
    plt.close()
