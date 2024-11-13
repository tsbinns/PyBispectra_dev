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

Various forms of information can be extracted from neural timeseries data. Of this information, phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics are of great interest, providing crucial insights into neuronal function and dysfunction. However, the methods commonly used for analysing these features possess notable limitations. Recent work has revealed the bispectrum – the Fourier transform of the third order moment – to be a powerful method for the analysis of electrophysiology data, overcoming many of these limitations. Here we present `PyBispectra`, a package for bispectral analyses of electrophysiology data including phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics.

# Statement of need

Analysis of phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics provide important mechanistic insights into interneuronal communication [@Canolty2010;@Silchenko2010;@Sherman2016]. Studies of these features in neural timeseries data have been used to investigate core nervous system functions such as movement and memory, including their perturbation in disease [@deHemptinne2013;@Cole2017;@Bazzigaluppi2018;@Binns2024]. However, traditional methods for analysing this information have critical limitations that hinder their utility. In contrast, the bispectrum - the Fourier transform of the third order moment [@Nikias1987] - can be used for phase-amplitude coupling [@Zandvoort2021], non-sinusoidal waveshape [@Bartz2019], and time delay analyses [@Nikias1988], overcoming many of the limitations associated with traditional methods.

Despite these benefits, the bispectrum has seen relatively little use in the field of neuroscience, in part due to the lack of an accessible, easy-to-use toolbox tailored to the analysis of electrophysiology data. Code written in MATLAB exists for electrophysiological analyses (see e.g., [github.com/sccn/roiconnect](https://github.com/sccn/roiconnect), [github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence](https://github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence)), however it is spread across multiple repositories, and often not in the form of a toolbox. Furthermore, use of this code requires a paid MATLAB license, limiting its accessibility. Code for computing the bispectrum can also be found written in the free-to-use Python language - e.g., @Bachetti2024 - however these implementations are not tailored to the analysis of electrophysiology data, limiting their use for neuroscience research. The `PyBispectra` package aims to address these limitations by providing a single, comprehensive toolbox for analysing phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics in electrophysiology data with the bispectrum \autoref{fig:overview}, including tutorials to facilitate an understanding of these analyses in the context of neuroscience research. Data formats follow conventions from popular electrophysiological signal processing packages like `MNE-Python` [@Gramfort2013], and helper functions are provided as wrappers around `MNE-Python` and `SciPy` [@Virtanen2020] tools to facilitate data processing prior to bispectral analyses. Additional plotting tools are provided to visualise and aid the interpretation of results.

![Overview of the `PyBispectra` toolbox.\label{fig:overview}](Overview.png)

# Features

## Phase-amplitude coupling

Phase-amplitude coupling refers to the interaction between the phase of a lower frequency oscillation and the amplitude of a higher frequency oscillation, either within or across signals. It has been posited as a mechanism for the integration of neural information across spatiotemporal scales [@Canolty2010], with pathological alterations in coupling seen in neurological disorders [@deHemptinne2013;@Bazzigaluppi2018]. Common methods for quantifying phase-amplitude coupling include the Canolty approach [@Canolty2006] and modulation index [@Tort2010], which involve bandpass filtering signals in the frequency bands of interest and using the Hilbert transform to extract the phase and amplitude information. This approach has several limitations. First, the bandpass filters require precise properties that are not readily apparent, with incorrect filter properties smearing information across a broad frequency range, hindering the analysis of frequency-specific interactions [@Zandvoort2021]. Second, the Hilbert transform is a relatively demanding procedure, contributing to a high computational cost of the analysis. Finally, when analysing interactions between different signals, spurious coupling estimates can arise due to interactions within each signal which cannot be easily corrected for [@PellegriniPreprint]. In contrast, the bispectrum captures phase-amplitude coupling whilst overcoming these limitations. Specifically, coupling information is captured without requiring bandpass filtering, preserving the spectral resolution and reducing the risk of misinterpreting results [@Zandvoort2021]. Furthermore, bispectral analysis is computationally efficient, relying on the computationally cheap Fourier transform. Finally, spurious across-signal coupling estimates can be corrected for using bispectral antisymmetrisation [@Chella2014;@PellegriniPreprint]. `PyBispectra` provides the tools for performing bispectral phase-amplitude coupling analysis, with options for antisymmetrisation as well as normalisation using the threenorm [@Shahbazi2014], bounding coupling scores between 0 and 1 to enhance interpretability. Altogether, the bispectrum is a robust and computationally efficient approach for phase-amplitude coupling analysis, overcoming key limitations of traditional methods.

## Time delay analysis

Time delay analysis provides insight into the physical connections between brain regions by identifying latencies of information transfer between signals, complementing structural analyses using electrophysiology data [@Silchenko2010;@Binns2024]. A traditional approach for time delay analysis is cross-correlation, quantifying the similarity of signals at a set of time lags. However, there a two key limitations to this approach, including its limited robustness to noise in the data [@Nikias1988], as well as a vulnerability to spurious zero time lag interactions arising due to volume conduction and source mixing in the sensor space [@Chella2014]. On the other hand, the bispectrum is resilient to Gaussian noise sources in the data [@Nikias1988], and the process of antisymmetrisation can also be used to correct for spurious zero time lag interactions [@Chella2014]. `PyBispectra` provides tools for time delay analysis using the bispectrum, with options for antisymmetrisation, offering a robust method for the analysis of time delays in electrophysiology data.

## Non-sinusoidal waveshape characteristics

Non-sinusoidal signal characteristics can indicate particular properties of interneuronal communication [@Sherman2016], with pathological alterations seen in neurological disorders [@Cole2017]. Various non-sinusoidal properties can be identified, among them sawtooth signals and a dominance of peaks or troughs. Analysis of these characteristics can be performed on timeseries data using peak finding-based procedures - see e.g., @Cole2017 - however this is computationally demanding for high sampling rate data. Furthermore, this analysis is complicated by a desire in neuroscience to isolate frequency-specific neural activity, with bandpass filtering suppressing non-sinusoidal information [@Bartz2019]. More complicated procedures must therefore be used, which risk contamination from frequencies outside the band of interest - see e.g., @Cole2017. In contrast, the bispectrum captures frequency-resolved non-sinusoidal information directly [@Bartz2019], in a computationally efficient manner that minimises the impact of high sampling rate timeseries. `PyBispectra` provides tools for analysing non-sinusoidal waveshape characteristics using the bispectrum, including the option of normalisation using the threenorm [@Shahbazi2014] to bound values in a standardised range for improved interpretability. Altogether, this offers a robust and efficient method for the analysis of non-sinusoidal features in electrophysiology data.

## Supplementary tools for bispectral analyses

Two common issues faced in the analysis of electrophysiology data are dealing with a limited signal-to-noise ratio, and obtaining interpretable results from high-dimensional data [@Cohen2022]. Spatio-spectral decomposition is a multivariate technique that addresses these problems, using linear filters to capture the key aspects of frequency band-specific information in a high signal-to-noise ratio, low-dimensional space [@Nikulin2011]. This decomposition can be applied for the multivariate analysis of non-sinusoidal waveshape properties, with extensions like harmonic power maximisation available to more specifically target non-sinusoidal information [@Bartz2019]. `PyBispectra` provides tools for using spatio-spectral filtering to enhance the signal-to-noise ratio and reduce the dimensionality of electrophysiology data.

Other practical features of `PyBispectra` includes dedicated plotting tools for the visualisation of results from phase-amplitude coupling, time delay, and non-sinusoidal waveshape analyses to aid interpretability. Furthermore, other cross-frequency tools for amplitude-amplitude coupling and phase-phase coupling are also provided, recommended for use in identifying genuine phase-amplitude coupling [@Giehl2021]. Finally, the various forms of analysis are accompanied by detailed tutorials, helping to facilitate an understanding of how these tools can be used to analyse electrophysiology data.

# Conclusion

Altogether, the bispectrum is a robust and computationally efficient tool for the analysis of phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics. These bispectral approaches overcome key limitations of traditional methods, which have until now hindered neuroscience research. To aid in the uptake of bispectral methods, `PyBispectra` provides access to these tools in a comprehensive, easy-to-use package, tailored for use with electrophysiology data.

# Acknowledgements

We acknowledge contributions from Mr. Toni M. Brotons and Dr. Timon Merk, who provided valuable feedback and suggestions for the design of the `PyBispectra` package and its documentation.

# References