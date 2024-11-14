---
title: 'PyBispectra: A toolbox for advanced electrophysiological signal processing using the bispectrum'
tags:
  - Python
  - neuroscience
  - signal processing
  - bispectrum
authors:
  - name: Thomas S. Binns
    orcid: 0000-0003-0657-0891
    affiliation: "1, 2, 3"
    corresponding: true
  - name: Franziska Pellegrini
    orcid: 0000-0001-9769-1597
    affiliation: "3, 4"
  - name: Tin Jurhar
    orcid: 0000-0002-8804-2349
    affiliation: "5, 6"
  - name: Richard M. Köhler
    orcid: 0000-0002-5219-1289
    affiliation: 1
  - name: Stefan Haufe
    orcid: 0000-0003-1470-9195
    affiliation: "2, 3, 4, 5, 7"
affiliations:
 - name: Movement Disorders Unit, Charité - Universitätsmedizin Berlin, Germany
   index: 1
 - name: Einstein Center for Neurosciences Berlin, Charité - Universitätsmedizin Berlin, Germany
   index: 2
 - name: Bernstein Center for Computational Neuroscience Berlin, Germany
   index: 3
 - name: Berlin Center for Advanced Neuroimaging, Charité - Universitätsmedizin Berlin, Germany
   index: 4
 - name: Electrical Engineering and Computer Science Department, Technische Universität Berlin, Germany
   index: 5
 - name: Donders Institute for Brain, Cognition and Behaviour, Radboud Universiteit, The Netherlands
   index: 6
 - name: Physikalisch-Technische Bundesanstalt Braunschweig und Berlin, Germany
   index: 7
date: 01 October 2024
bibliography: paper.bib
---

# Summary

Various forms of information can be extracted from neural timeseries data. Of this information, phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics are of great interest, providing crucial insights into neuronal function and dysfunction. However, the methods commonly used for analysing these features possess notable limitations. Recent work has revealed the bispectrum – the Fourier transform of the third order moment – to be a powerful tool for the analysis of electrophysiology data, overcoming many of these limitations. Here we present `PyBispectra`, a package for bispectral analyses of electrophysiology data including phase-amplitude coupling, time delays, and non-sinusoidal waveshape.

# Statement of need

Analysis of phase-amplitude coupling, time delays, and non-sinusoidal waveshape provide important insights into interneuronal communication [@Canolty2010;@Silchenko2010;@Sherman2016]. Studies of these features in neural data have been used to investigate core nervous system functions such as movement and memory, including their perturbation in disease [@deHemptinne2013;@Cole2017;@Bazzigaluppi2018;@Binns2024]. However, traditional methods for analysing this information have critical limitations that hinder their utility. In contrast, the bispectrum - the Fourier transform of the third order moment [@Nikias1987] - can be used for the analysis of phase-amplitude coupling [@Zandvoort2021], non-sinusoidal waveshape [@Bartz2019], and time delays [@Nikias1988], overcoming many of the limitations associated with traditional methods.

Despite these benefits, the bispectrum has seen relatively little use in the field of neuroscience, in part due to the lack of an accessible, easy-to-use toolbox tailored to electrophysiology data. Code written in MATLAB exists for some analyses (see e.g., [github.com/sccn/roiconnect](https://github.com/sccn/roiconnect), [github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence](https://github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence)), however it is spread across multiple repositories, and often not in the form of a toolbox. Furthermore, use of this code requires a paid MATLAB license, limiting its accessibility. Code for computing the bispectrum does exist in the free-to-use Python language - e.g., @Bachetti2024 - however these implementations are not tailored to use with electrophysiology data. The `PyBispectra` package addressed these problems by providing a single, comprehensive toolbox for bispectral analysis of electrophysiology data (\autoref{fig:overview}), including tutorials to facilitate an understanding of these analyses in the context of neuroscience research.

![Overview of the `PyBispectra` toolbox.\label{fig:overview}](Overview.svg)

# Features

## Phase-amplitude coupling

Phase-amplitude coupling refers to the interaction between the phase of a lower frequency oscillation and the amplitude of a higher frequency oscillation. It has been posited as a mechanism for the integration of neural information across spatiotemporal scales [@Canolty2010], with perturbations seen in disease [@deHemptinne2013;@Bazzigaluppi2018]. Common methods for quantifying phase-amplitude coupling include the Canolty approach [@Canolty2006] and modulation index [@Tort2010], which involve bandpass filtering signals in the frequency bands of interest and using the Hilbert transform to extract the phase and amplitude information. This approach has several limitations. First, the bandpass filters require precise properties that are not readily apparent, with poorly designed filters smearing information across a broad spectral range, hindering the analysis of frequency-specific interactions [@Zandvoort2021]. Second, the Hilbert transform is a relatively demanding procedure, contributing to a high computational cost of the analysis. Finally, when analysing interactions between different signals, spurious coupling estimates can arise due to interactions within each signal which cannot be corrected for [@PellegriniPreprint]. In contrast, the bispectrum captures phase-amplitude coupling whilst overcoming these limitations. Specifically, analysing coupling does not require bandpass filtering, preserving the spectral resolution and reducing the risk of misinterpreting results [@Zandvoort2021]. Furthermore, bispectral analysis is computationally efficient, relying on the computationally cheap Fourier transform. Finally, spurious across-signal coupling estimates can be corrected for using bispectral antisymmetrisation [@Chella2014;@PellegriniPreprint]. `PyBispectra` provides the tools for performing bispectral phase-amplitude coupling analysis, with options for antisymmetrisation and a univariate normalisation procedure [@Shahbazi2014] that bounds coupling scores between 0 and 1 to enhance interpretability.

## Time delays

Time delay analysis identifies latencies of information transfer between signals, providing additional insight into the physical connections between brain regions using electrophysiology data [@Silchenko2010;@Binns2024]. A traditional time delay analysis method is cross-correlation, quantifying the similarity of signals at a set of time lags. However, this approach has a limited robustness to noise [@Nikias1988] and a vulnerability to spurious zero time lag interactions arising due to volume conduction and source mixing in the sensor space. On the other hand, the bispectrum is resilient to Gaussian noise sources in the data [@Nikias1988], and antisymmetrisation can be used to correct for spurious zero time lag interactions [@Chella2014]. `PyBispectra` provides tools for bispectral time delay analysis, with options for antisymmetrisation.

## Non-sinusoidal waveshapes

Non-sinusoidal signals indicates particular properties of interneuronal communication [@Sherman2016], with perturbations seen in disease [@Cole2017]. Various non-sinusoidal properties can be identified, among them sawtooth signals and a dominance of peaks or troughs. Analysis of these characteristics can be performed on timeseries data using peak finding-based procedures - see e.g., @Cole2017 - however this is computationally demanding for high sampling rate data. Furthermore, the analysis is complicated by a desire to isolate frequency-specific neural activity, with bandpass filtering suppressing non-sinusoidal information [@Bartz2019]. Attempts to address this remain limited by a risk of contamination from frequencies outside the band of interest - see e.g., @Cole2017. In contrast, the bispectrum captures frequency-resolved non-sinusoidal information directly [@Bartz2019], in a computationally efficient manner that minimises the impact of high sampling rate data. `PyBispectra` provides tools for analysing non-sinusoidal waveshapes using the bispectrum, including the option of univariate normalisation [@Shahbazi2014] to bound values in a standardised range for improved interpretability.

## Supplementary tools for bispectral analyses

Two common issues faced in the analysis of electrophysiology data are dealing with a limited signal-to-noise ratio, and obtaining interpretable results from high-dimensional data [@Cohen2022]. Spatio-spectral decomposition is a multivariate technique that addresses these problems, capturing the key aspects of frequency band-specific information in a high signal-to-noise ratio, low-dimensional space [@Nikulin2011]. This decomposition can be applied for the multivariate analysis of non-sinusoidal waveshapes, with extensions like harmonic power maximisation available that more specifically target non-sinusoidal information [@Bartz2019]. `PyBispectra` provides tools for using spatio-spectral filtering to enhance the signal-to-noise ratio and reduce the dimensionality of electrophysiology data.

Other practical features of `PyBispectra` include dedicated plotting tools for the visualisation of results to aid interpretability. Additionally, data formats follow conventions from popular signal processing packages like `MNE-Python` [@Gramfort2013], and helper functions are provided as wrappers around `MNE-Python` and `SciPy` [@Virtanen2020] tools to facilitate data processing prior to bispectral analyses. Furthermore, cross-frequency tools for amplitude-amplitude and phase-phase coupling are also provided, following literature recommendations for identifying genuine phase-amplitude coupling [@Giehl2021]. Finally, the various analyses are accompanied by detailed tutorials, facilitating an understanding of how the bispectrum can be used to analyse electrophysiology data.

# Conclusion

Altogether, the bispectrum is a robust and computationally efficient tool for the analysis of phase-amplitude coupling, time delays, and non-sinusoidal waveshapes. Bispectral approaches overcome key limitations of traditional methods, which have until now hindered neuroscience research. To aid in the uptake of bispectral methods, `PyBispectra` provides access to these tools in a comprehensive, easy-to-use package, tailored for use with electrophysiology data.

# Acknowledgements

We acknowledge contributions from Mr. Toni M. Brotons and Dr. Timon Merk, who provided valuable feedback and suggestions for the design of the `PyBispectra` package and its documentation.

# References