# s61-supplements

**Authors:** R. Nikutta, C. Agliozzo

**Version:** 20161115

Supplementary materials for the paper:

Agliozzo et al. 2016, "New ATCA, ALMA and VISIR observations of the
candidate LBV SK -67266 (S61): the nebular mass from modelling 3D
density distributions", MNRAS MN-16-3575-MJ.

[comment]: <> ([MNRAS](http://mnras.oxfordjournals.org/content/early/2016/11/14/mnras.stw2927.abstract)
[MNRAS](http://mnras.oxfordjournals.org/content/early/2016/11/16/xyz)

[astro-ph](foo)


*Data files:*

`em_map\*fits`: Emission measure maps for S61 at 8 and 17 GHZ. Masked at 3-sigma level.

`err_em_map\*fits`: Corresponding error maps.

*Source code:*

[plots.py](./plots.py): Python source code to generate several figures from the paper

[fits.py](./fits.py): Python source code for fit the EM maps with [RHOCUBE](https://github.com/rnikutta/rhocube)

This directory also contains required auxiliary data files, models, etc.
