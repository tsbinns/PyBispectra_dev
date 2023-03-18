"""Tools for handling PAC analysis."""

import copy

import numpy as np
from pqdm.processes import pqdm

from pybispectra.utils import ResultsCFC
from pybispectra.utils._process import (
    _ProcessBispectrum,
    _compute_bispectrum,
    _compute_threenorm,
)


np.seterr(divide="ignore", invalid="ignore")  # no warning for NaN division


class PAC(_ProcessBispectrum):
    """Class for computing phase-amplitude coupling (PAC) using the bispectrum.

    Parameters
    ----------
    data : numpy.ndarray of float
        3D array of FFT coefficients with shape `[epochs x channels x
        frequencies]`.

    freqs : numpy.ndarray of float
        1D array of the frequencies in :attr:`data`.

    verbose : bool (default True)
        Whether or not to report the progress of the processing.

    Attributes
    ----------
    results : tuple of ResultsCFC
        PAC results for each of the computed metrics.

    data : numpy.ndarray of float
        FFT coefficients with shape `[epochs x channels x frequencies]`.

    freqs : numpy.ndarray of float
        1D array of the frequencies in :attr:`data`.

    indices : tuple of numpy.ndarray of int
        Two arrays containing the seed and target indices (respectively) most
        recently used with :meth:`compute`.

    f1 : numpy.ndarray of float
        1D array of low frequencies most recently used with :meth:`compute`.

    f2 : numpy.ndarray of float
        1D array of high frequencies most recently used with :meth:`compute`.

    verbose : bool
        Whether or not to report the progress of the processing.
    """

    _return_nosym = False
    _return_antisym = False
    _return_nonorm = False
    _return_threenorm = False

    _bispectrum = None
    _bicoherence = None

    _pac_nosym_nonorm = None
    _pac_nosym_threenorm = None
    _pac_antisym_nonorm = None
    _pac_antisym_threenorm = None

    def compute(
        self,
        indices: tuple[np.ndarray] | None = None,
        f1: np.ndarray | None = None,
        f2: np.ndarray | None = None,
        symmetrise: str | list[str] = ["none", "antisym"],
        normalise: str | list[str] = ["none", "threenorm"],
        n_jobs: int = 1,
    ) -> None:
        r"""Compute PAC, averaged over epochs.

        Parameters
        ----------
        indices : tuple of numpy.ndarray of int | None (default None)
            Indices of the channels to compute PAC between. Should contain two
            1D arrays of equal length for the seed and target indices,
            respectively. If ``None``, coupling between all channels is
            computed.

        f1 : numpy.ndarray of float | None (default None)
            A 1D array of the lower frequencies to compute PAC on. If ``None``,
            all frequencies are used.

        f2 : numpy.ndarray of float | None (default None)
            A 1D array of the higher frequencies to compute PAC on. If
            ``None``, all frequencies are used.

        symmetrise : str | list of str (default ``["none", "antisym"]``)
            Symmetrisation to perform when computing PAC. If ``"none"``, no
            symmetrisation is performed. If ``"antisym"``, antisymmetrisation
            is performed.

        normalise : str | list of str (default ``["none", "threenorm"]``)
            Normalisation to perform when computing PAC. If ``"none"``, no
            normalisation is performed. If ``"threenorm"``, the bispectrum is
            normalised to the bicoherence using a threenorm.

        n_jobs : int (default ``1``)
            The number of jobs to run in parallel.

        Notes
        -----
        PAC can be computed as the bispectrum, :math:`B`, of signals
        :math:`\vec{x}` and :math:`\vec{y}` of the seeds and targets,
        respectively, which has the general form

        :math:`\large B_{kmn}(f_1,f_2)=<\vec{k}(f_1)\vec{m}(f_2)\vec{n}^*(f_2+f_1)>`,

        where :math:`kmn` is a combination of channels :math:`\vec{x}` and
        :math:`\vec{y}`, and the angled brackets represent the averaged value
        over epochs. PAC between signals :math:`\vec{x}` and :math:`\vec{y}` is
        given as

        :math:`\large PAC(\vec{x}_{f_1},\vec{y}_{f_2})=B_{xyy}(f_1)B_{xyy}(f_2)B_{xyy}^*(f_2+f_1)`.

        Antisymmetrisaion is achieved by subtracting the PAC results from the
        transposed bispectrum, :math:`B_{xyx}` :footcite:`Chella2014`. The
        bispectrum can be normalised to the bicoherence, :math:`\mathcal{B}`,
        using the threenorm, :math:`N` :footcite:`Zandvoort2021`:

        :math:`\large N_{xyy}(f_1,f_2)=(<|\vec{x}(f_1)|^3><|\vec{y}(f_2)|^3><|\vec{y}(f_2+f_1)|^3>)^{\frac{1}{3}}`,

        :math:`\large \mathcal{B}_{xyy}(f_1,f_2)=\Large \frac{B_{xyy}(f_1,f_2)}{N_{xyy}(f_1,f_2)}`.

        If the seed and target for a given connection is the same channel and
        antisymmetrisation is being performed, ``numpy.nan`` values are
        returned.

        PAC is computed between all values of :attr:`f1` and :attr:`f2`. If any
        value of :attr:`f1` is higher than :attr:`f2`, a ``numpy.nan`` value is
        returned.

        References
        ----------
        .. footbibliography::
        """  # noqa E501
        self._reset_attrs()

        self._sort_metrics(symmetrise, normalise)
        self._sort_indices(indices)
        self._sort_freqs(f1, f2)
        self._sort_parallelisation(n_jobs)

        if self.verbose:
            print("Computing PAC...\n")

        self._compute_bispectrum()
        if self._return_threenorm:
            self._compute_bicoherence()
        self._compute_pac()
        self._store_results()

        if self.verbose:
            print("    [PAC computation finished]\n")

    def _reset_attrs(self) -> None:
        """Reset attrs. of the object to prevent interference."""
        super()._reset_attrs()

        self._return_nosym = False
        self._return_antisym = False
        self._return_nonorm = False
        self._return_threenorm = False

        self._bispectrum = None
        self._bicoherence = None

        self._pac_nosym_nonorm = None
        self._pac_nosym_threenorm = None
        self._pac_antisym_nonorm = None
        self._pac_antisym_threenorm = None

    def _sort_metrics(
        self, symmetrise: str | list[str], normalise: str | list[str]
    ) -> None:
        """Sort inputs for the form of results being requested."""
        if not isinstance(symmetrise, str) and not isinstance(
            symmetrise, list
        ):
            raise TypeError(
                "`symmetrise` must be a list of strings or a string."
            )
        if not isinstance(normalise, str) and not isinstance(normalise, list):
            raise TypeError(
                "`normalise` must be a list of strings or a string."
            )

        if isinstance(symmetrise, str):
            symmetrise = [copy.copy(symmetrise)]
        if isinstance(normalise, str):
            normalise = [copy.copy(normalise)]

        supported_sym = ["none", "antisym"]
        if any(entry not in supported_sym for entry in symmetrise):
            raise ValueError("The value of `symmetrise` is not recognised.")
        supported_norm = ["none", "threenorm"]
        if any(entry not in supported_norm for entry in normalise):
            raise ValueError("The value of `normalise` is not recognised.")

        if "none" in symmetrise:
            self._return_nosym = True
        if "antisym" in symmetrise:
            self._return_antisym = True

        if "none" in normalise:
            self._return_nonorm = True
        if "threenorm" in normalise:
            self._return_threenorm = True

    def _compute_bispectrum(self) -> None:
        """Compute bispectrum between f1s and f2s of seeds and targets."""
        if self.verbose:
            print("    Computing bispectrum...")

        if self._return_antisym:
            # kmm, mkm
            kmn = np.array([np.array([0, 1, 1]), np.array([1, 0, 1])])
        else:
            # kmm
            kmn = np.array([np.array([0, 1, 1])])

        args = [
            {
                "data": self.data[:, (seed, target)],
                "freqs": self.freqs,
                "f1s": self.f1,
                "f2s": self.f2,
                "kmn": kmn,
            }
            for seed, target in zip(self._seeds, self._targets)
        ]

        # have to average complex value outside of Numba-compiled function
        self._bispectrum = (
            np.array(
                pqdm(
                    args,
                    _compute_bispectrum,
                    self._n_jobs,
                    argument_type="kwargs",
                    desc="Processing connections...",
                    disable=not self.verbose,
                )
            )
            .mean(axis=2)
            .transpose(1, 0, 2, 3)
        )

        if self.verbose:
            print("        [Bispectra computation finished]\n")

    def _compute_bicoherence(self) -> None:
        """Compute bicoherence from the bispectrum using the threenorm."""
        if self.verbose:
            print("    Computing bicoherence...")

        args = [
            {
                "data": self.data[:, (seed, target)],
                "freqs": self.freqs,
                "f1s": self.f1,
                "f2s": self.f2,
            }
            for seed, target in zip(self._seeds, self._targets)
        ]

        threenorm = np.array(
            pqdm(
                args,
                _compute_threenorm,
                self._n_jobs,
                argument_type="kwargs",
                desc="Processing connections...",
                disable=not self.verbose,
            )
        )

        self._bicoherence = self._bispectrum / threenorm

        if self.verbose:
            print("        [Bicoherence computation finished]\n")

    def _compute_pac(self) -> None:
        """Compute PAC results from bispectrum/bicoherence."""
        if self._return_nonorm:
            if self._return_nosym:
                self._pac_nosym_nonorm = np.abs(self._bispectrum[0])
            if self._return_antisym:
                self._pac_antisym_nonorm = np.abs(
                    self._bispectrum[0] - self._bispectrum[1]
                )
                for con_i, seed, target in zip(
                    range(self._n_cons), self._seeds, self._targets
                ):
                    if seed == target:
                        self._pac_antisym_nonorm[con_i] = np.full_like(
                            self._pac_antisym_nonorm[con_i], fill_value=np.nan
                        )

        if self._return_threenorm:
            if self._return_nosym:
                self._pac_nosym_threenorm = np.abs(self._bicoherence[0])
            if self._return_antisym:
                self._pac_antisym_threenorm = np.abs(
                    self._bicoherence[0] - self._bicoherence[1]
                )
                for con_i, seed, target in zip(
                    range(self._n_cons), self._seeds, self._targets
                ):
                    if seed == target:
                        self._pac_antisym_threenorm[con_i] = np.full_like(
                            self._pac_antisym_threenorm[con_i],
                            fill_value=np.nan,
                        )

    def _store_results(self) -> None:
        """Store computed results in objects."""
        results = []

        if self._pac_nosym_nonorm is not None:
            results.append(
                ResultsCFC(
                    self._pac_nosym_nonorm,
                    self.indices,
                    self.f1,
                    self.f2,
                    "PAC - Unsymmetrised Bispectra",
                )
            )

        if self._pac_nosym_threenorm is not None:
            results.append(
                ResultsCFC(
                    self._pac_nosym_threenorm,
                    self.indices,
                    self.f1,
                    self.f2,
                    "PAC - Unsymmetrised Bicoherence",
                )
            )

        if self._pac_antisym_nonorm is not None:
            results.append(
                ResultsCFC(
                    self._pac_antisym_nonorm,
                    self.indices,
                    self.f1,
                    self.f2,
                    "PAC - Antisymmetrised Bispectra",
                )
            )

        if self._pac_antisym_threenorm is not None:
            results.append(
                ResultsCFC(
                    self._pac_antisym_threenorm,
                    self.indices,
                    self.f1,
                    self.f2,
                    "PAC - Antisymmetrised Bicoherence",
                )
            )

        self._results = tuple(results)

    @property
    def results(self) -> tuple[ResultsCFC]:
        """Return the results."""
        return self._results
