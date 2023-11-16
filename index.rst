:tocdepth: 1

.. sectnum::

.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

.. note::

   **This technote is a work-in-progress.**


Abstract
========

Data analysis of the `LVV-1791 M2 RBP REPEATABILITY TEST`_.

.. _LVV-1791 M2 RBP REPEATABILITY TEST: https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T1829

The test is designed to check the repeatability in the measured position for all the 6 :abbr:`DoF (Degrees of Freedom)`.
The requirements to met are:

- Linear repeatability within 1 :math:`\mu\mathrm{m}`
- Rotation repeatability within :math:`1\cdot10^{-5}\mathrm{arcsec}` 0.108 :math:`\mathrm{arcsec}`

Test Case
=========

In the test M2 is moved sequentially along each DoF for most of the travel range in a positive and a negative.
Excursion ranges are
:math:`\pm 250 \mu\mathrm{m}` for the linear movements and :math:`\pm 15 \mathrm{arcsec}` for rotations.
For each :abbr:`DoF (Degrees of Freedom)` are perfomed 5 sequence of 8 steps holded for 37 sec.

Data analysis
=============

Walking of the :abbr:`DoF (Degrees of Freedom)`
-----------------------------------------------

The values are retrieved from the :abbr:`IMS (Indipendent Measurement System)`. 
In the code are stored the start times for each sequence and it filter the datatset accordingly.
Then the first result is a summary plot showing the :abbr:`DoF (Degrees of Freedom)` walks with all the sequence.
The X-axis are the relative time from the beggining of each sequence, so that they are overlapped to each other.

.. figure:: /_static/figures/DOF_seq.png
   :name: fig-dof-seq
   :target: ../_images/DOF_seq.png
   :alt: DoF walking subplots

   DoF walking subplots.

Reserach of the Plateaus
------------------------

.. _np.ediff1d: https://numpy.org/doc/stable/reference/generated/numpy.ediff1d.html

In order to understand if the requirements are met or not, we need to claculate the statistic (i.e. mean, 
:abbr:`RMS (Root Mean Square error)` and :abbr:`PtV (Peak to Valley)`) of the plateaus in each sequences of the :abbr:`DoF (Degrees of Freedom)` s.
The code exploits the proximity difference of the points to each other in order to indentify the flat regions. More precisely the function 
`np.ediff1d`_ is used. Doing so, a new columns in the data frame is created with the difference of each element wrt the next one. Using this information
the code identifies the flat region if the difference fall below a certain threshold defined empirically. Even though this method can be considered
quite silly, it is more robust against high frequency noise respect some more elegnt approach like using the slope. Because this noise is present in the plateau (see fig. )
We decied to use the simple difference. Moreover, to avoid contamination from the outer part, when the M2 cell is still moving, the code adds a pad (i.e. it does not consider)

.. figure:: /_static/figures/plat_plot.png
   :name: fig-plats-seq
   :target: ../_images/plat_plot.png
   :alt: Example of a plateaus found in a single sequence.

   Example of a plateaus found in a single sequence.

Retrieving the plateaus statistic
---------------------------------


Add content here
================

Add content here.
See the `reStructuredText Style Guide <https://developer.lsst.io/restructuredtext/style.html>`__ to learn how to create sections, links, images, tables, equations, and more.

.. Make in-text citations with: :cite:`bibkey`.
.. Uncomment to use citations
.. .. rubric:: References
.. 
.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :style: lsst_aa
