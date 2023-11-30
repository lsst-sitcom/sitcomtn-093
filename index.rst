:tocdepth: 1

.. sectnum::

.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

.. note::

   **This technote is a work-in-progress.**


Abstract
========

Data analysis of the `LVV-T1829 M2 Rigid Body Position - Stability and Repeatability - Position Sensor Verification - Data Analysis`_.

.. _LVV-T1829 M2 Rigid Body Position - Stability and Repeatability - Position Sensor Verification - Data Analysis: https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T1829


The test is designed to check the repeatability in the measured position for all the 6 :abbr:`DoF (Degrees of Freedom)`.
related to the IMS measurements
The requirements verified by the test are:

- Linear repeatability within 1 :math:`\mu\mathrm{m}`
- Rotation repeatability within :math:`1\cdot10^{-5}  deg` 

Test Case
=========

The test case is the data collection of the test case M2 Rigid Body Motion - TMA https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T1791

In this test M2 is moved sequentially along each DoF for most of the travel range in a positive and a negative.

Excursion ranges retrieved by the test are
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

Reserach of the Plateau
------------------------

.. _np.ediff1d: https://numpy.org/doc/stable/reference/generated/numpy.ediff1d.html

In order to understand if the requirements are met or not, we need to claculate the statistic (i.e. mean, 
:abbr:`RMS (Root Mean Square error)` and :abbr:`PtV (Peak to Valley)`) of the plateaus in each sequences of the :abbr:`DoF (Degrees of Freedom)` s.
The code exploits the proximity difference of the points to each other in order to indentify the flat regions. More precisely the function 
`np.ediff1d`_ is used. Doing so, a new columns in the data frame is created with the difference of each element wrt the next one. Using this information
the code identifies the flat region if the difference fall below a certain threshold defined empirically. This method is more robust against high frequency noise.
Because of noise is present in the plateau (see fig. :numref:`label2`) the simple difference has been applied.  
Moreover, to avoid contamination from the outer part, when the M2 cell is still moving, the code rejects data found at the border of the plateau region.

.. _label2:
.. figure:: /_static/figures/plat_plot.png
   :name: fig-plats-seq
   :target: ../_images/plat_plot.png
   :alt: Example of a plateaus found in a single sequence.

   Example of a plateaus found in a single sequence.

Retrieving the plateaus statistic
---------------------------------
For each IMS axis statistics have been reduced for the plateau of each of the 8 step in which the path has been fractionated. The Peak to Valley 
values (P_V) between the commanded position and the measured one is plotted to check if the requirement `LVV-18727 LTS-146-REQ-0111-V-04 3.4.4 MIRROR POSITION SENSORS - M2 LSST Re-verification`_
is verified.

.. _LVV-18727 LTS-146-REQ-0111-V-04 3.4.4 MIRROR POSITION SENSORS - M2 LSST Re-verification: https://jira.lsstcorp.org/browse/LVV-18727

.. _label3:
.. figure:: /_static/figures/X_PV.png
   :name: repeatibility_x
   :target: ../_images/X_PV.png
   :alt: Repeatibility measured in X direction for the 8 data series.

   Repeatability along X axis.

.. _label4:
.. figure:: /_static/figures/Y_PV.png
   :name: repeatibility_y
   :target: ../_images/Y_PV.png
   :alt: Repeatibility measured in Y direction for the 8 data series.

   Repeatability along Y axis.

.. _label5:
.. figure:: /_static/figures/Z_PV.png
   :name: repeatibility_z
   :target: ../_images/Z_PV.png
   :alt: Repeatibility measured in Z direction for the 8 data series.

   Repeatability along Z axis.

.. _label6:
.. figure:: /_static/figures/DRX_PV.png
   :name: repeatibility_drx
   :target: ../_images/DRX_PV.png
   :alt: Repeatibility measured in DRX angle for the 8 data series.

   Repeatability along DRX angle.

.. _label7:
.. figure:: /_static/figures/DRY_PV.png
   :name: repeatibility_dry
   :target: ../_images/DRY_PV.png
   :alt: Repeatibility measured in DRY angle for the 8 data series.

   Repeatability along DRY angle.

.. _label8:
.. figure:: /_static/figures/DRZ_PV.png
   :name: repeatibility_drz
   :target: ../_images/DRZ_PV.png
   :alt: Repeatibility measured in DRZ angle for the 8 data series.

   Repeatability along DRY angle.


As cleary indentified by the plots repeatibility is well inside specifications and the requirement is so verified.

Conclusions
================

Data analysis for  Rigid Body Position its stability and repeatability and position sensor verification has bee carry out. Results show that requirements are 
verified and the IMS works as by design.

.. See the `reStructuredText Style Guide <https://developer.lsst.io/restructuredtext/style.html>`__ to learn how to create sections, links, images, tables, equations, and more.

.. Make in-text citations with: :cite:`bibkey`.
.. Uncomment to use citations
.. .. rubric:: References
.. 
.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :style: lsst_aa
