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

Various forms of information can be extracted from neural timeseries data. Of this information, phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics are of great interest, providing crucial insights into neuronal function and dysfunction. However, the methods commonly used for analysing these features possess notable limitations. In contrast, recent work has revealed the bispectrum – the Fourier transform of the third order moment – to be a powerful method for the analysis of electrophysiological data, tools offered by the `PyBispectra` package.

# Statement of need

Analysis of phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics provide important mechanistic insights into interneuronal communication [@Canolty2010;@Silchenko2010;@Sherman2016]. Studies of these features in neural timeseries data have been used to investigate core nervous system functions such as movement and memory, including their perturbation in disease [@deHemptinne2013;@Cole2017;@Bazzigaluppi2018;@Binns2024]. However, traditional methods for analysing this information have critical limitations that hinder their utility. In contrast, the bispectrum - the Fourier transform of the third order moment [@Nikias1987] - can be used for phase-amplitude coupling [@Zandvoort2021], non-sinusoidal waveshape [@Bartz2019], and time delay analyses [Nikias1988], overcoming many of these limitations.

Despite these benefits, the bispectrum has seen relatively little use in the field of neuroscience, in part due to the lack of an accessible, easy-to-use toolbox tailored to electrophysiological analyses. Code written in MATLAB exists for electrophysiological analyses (see e.g., [github.com/sccn/roiconnect](https://github.com/sccn/roiconnect), [github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence](https://github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence)), however it is spread across multiple repositories, often not in the form of a toolbox. Furthermore, use of this code requires a paid MATLAB license, limiting its accessibility. Code for computing the bispectrum can also be found written in the free-to-use Python language (e.g., @Stringray), however these implementations are not tailored to electrophysiological analyses, limiting their use for neuroscience research. The `PyBispectra` package aims to address these limitations by providing a single, comprehensive toolbox for analysing phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics in electrophysiological data, including tutorials to facilitate an understanding of these analyses in the context of neuroscience research \autoref{fig:overview}. Data formats follow conventions from popular electrophysiological signal processing packages like MNE-Python [@Gramfort2013], and helper functions are provided as wrappers around MNE-Python and SciPy [@Virtanen2020] tools to facilitate data processing prior to bispectral analyses. Additional plotting tools are provided to visualise and aid the interpretation of results.

![Overview of the `PyBispectra` toolbox.\label{fig:overview}](Overview.pdf)

# Features

## Phase-amplitude coupling

Phase-amplitude coupling refers to the interaction between the phase of a lower frequency oscillation and the amplitude of a higher frequency oscillation, either within or across signals. Phase-amplitude coupling is commonly quantified using the Canolty approach [@Canolty2006] and modulation index [@Tort2010], which involve bandpass filtering signals in the frequency bands of interest and using the Hilbert transform to extract the phase and amplitude information. This approach has several limitations. First, the bandpass filters require precise properties that are not readily apparent, with incorrect filter properties smearing information across a broad frequency range, hindering the analysis of frequency-specific interactions [@Zandvoort2021]. Second, the Hilbert transform is a relatively demanding procedure, contributing to a high computational cost of the analysis. Finally, when analysing interactions between different signals, spurious coupling estimates can arise due to interactions within each signal which cannot be easily corrected for [@PellegriniPreprint]. In contrast, the bispectrum captures phase-amplitude coupling whilst overcoming these limitations. Specifically, coupling information is captured without requiring bandpass filtering, preserving the spectral resolution and reducing the risk of misinterpreting results [@Zandvoort2021]. Furthermore, bispectral analysis is computationally efficient, relying on the computationally cheap Fourier transform. Additionally, spurious across-signal coupling estimates can be corrected for using bispectral antisymmetrisation [@Chella2014;@PellegriniPreprint]. `PyBispectra` provides the tools for performing bispectral phase-amplitude coupling analysis, with options for antisymmetrisation as well as normalisation using the threenorm [@Shahbazi2014], bounding coupling scores between 0 and 1 to aid interpretability. Altogether, the bispectrum is a robust and computationally efficient approach for phase-amplitude coupling analysis, overcoming key limitations of traditional methods.

\autoref{fig:overview}

## Time delay analysis

Time delay analysis provides insight into the physical connections between brain regions, complementing structural analyses using functional investigations from electrophysiological data. A traditional approach for time delay analysis is cross-correlation, quantifying the similarity of signals at a set of time lags. However, there a two key limitations to this approach, including its limited robustness to noise in the data [@Nikias1988], as well as a vulnerability to spurious zero time lag interactions arising due to volume conduction and source mixing in the sensor space [@JurharInPrep]. On the other hand, the bispectrum is resilient to Gaussian noise sources in the data [@Nikias1988], and the process of antisymmetrisation can also be used to correct for spurious zero time lag interactions [@Chella2014;@JurharInPrep]. `PyBispectra` provides tools for time delay analysis using the bispectrum, with options for antisymmetrisation, offering a robust method for the analysis of time delays in electrophysiological data.

## Non-sinusoidal waveshape characteristics

## Multivariate preprocessing with spatio-spectral filtering

## Additional cross-frequency coupling methods

## Constructing spectral representations of data

## Visualising results

For instance, when analysing phase-amplitude coupling, the interaction between the phase of a lower frequency oscillation and the amplitude of a higher frequency oscillation is commonly quantified using the Canolty approach [@Canolty2006] and modulation index [@Tort2010]. However, these approaches require filters to be applied to the data whose properties are not readily apparent. Crucially, incorrect filter properties risk smearing information across a broad frequency range, hindering the analysis of frequency-specific interactions [@Zandvoort2021]. Additionally, these approaches are computationally demanding due to their reliance on the Hilbert transform. Furthermore, when analysing interactions between different signals, spurious coupling estimates can arise due to volume conduction and source-mixing in the sensor space [@PellegriniPreprint]. This vulnerability is also suffered by traditional methods for analysing time delays between signals - which provide insights into the physical connections between brain regions - such as the cross-correlation [@JurharInPrep]. Finally, extracting frequency-specific non-sinusoidal waveshape information using peak finding-based timseries analyses necessitates preprocessing steps that corrupt the shape of the underlying signal [@Bartz2019]. Approaches to overcome this limitation prevent a direct analysis of frequency-specific activity, in addition to these analyses being generally computationally demanding [@Cole2017]. Altogether, there are notabe limitations with traditional approaches for analysing phase-amplitude coupling, time delays, and non-sinusoidal waveshapes.

In contrast, the bispectrum overcomes these limitations, acting as a robust and computationally efficient tool for electrophysiological signal analysis. For phase-amplitude coupling, use of the bispectrum obviates the need to define precise filter settings [@Zandvoort2021], the computationally demanding Hilbert transform is avoided in favour of the Fourier transform to reduce the computational burden of the analysis. Furthermore, bispectral coupling analysis can easily be corrected for spurious across-site coupling estimates using the technique of antisymmetrisation [@Chella2014;@PellegriniPreprint]. This same benefit is also found for time delay analysis [@Chella2014;@JurharInPrep], where spurious estimates can obscure genuine interactions. Finally, the bispectrum allows for the direct examination of frequency-specific non-sinusoidal characteristics, all without corrupting waveshape information and the need for expensive peak-based analyses [@Bartz2019]. More generally, the bispectrum is also highly resilient to non-Gaussian noise [@Nikias1988], and normalisation approaches exist ...
    further adding to the robust nature of the method. Overall, many limitations of traditional analysis methods are addressed by the use of the bispectrum.

Despite these benefits, the bispectrum has seen relatively little use in the field of neuroscience, in part due to the lack of an accessible, easy-to-use toolbox tailored to electrophysiological analyses. Code written in MATLAB exists for electrophysiological analyses (see e.g., [github.com/sccn/roiconnect](https://github.com/sccn/roiconnect), [github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence](https://github.com/ZuseDre1/AnalyzingWaveshapeWithBicoherence)), however it is spread across multiple repositories, often not in the form of a toolbox. Furthermore, use of this code requires a paid MATLAB license, limiting its accessibility. Code for computing the bispectrum can also be found written in the free-to-use Python language (e.g., @Stringray), however these implementations are not tailored to electrophysiological analyses, limiting their use for neuroscience research. The `PyBispectra` package aims to address these limitations by providing a single, comprehensive toolbox for analysing phase-amplitude coupling, time delays, and non-sinusoidal waveshape characteristics in electrophysiological data, including tutorials to facilitate an understanding of these analyses in the context of neuroscience research. The toolbox includes approaches for antisymmetrisation to correct for spurious coupling estimates [@Chella2014;@PellegriniPreprint;@JurharInPrep], 

Data formats follow conventions from popular electrophysiological signal processing packages like MNE-Python [@Gramfort2013], and helper functions are provided as wrappers around MNE-Python and SciPy [@Virtanen2020] tools to facilitate data processing prior to bispectral analyses. Additional plotting tools are provided to visualise and aid the interpretation of results.



`Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References