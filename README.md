# s61-supplements

Supplementary materials for the paper:

*Agliozzo et al. 2016, "New ATCA, ALMA and VISIR observations of the
candidate LBV SK -67266 (S61): the nebular mass from modelling 3D
density distributions", MNRAS MN-16-3575-MJ.*
| [MNRAS](http://mnras.oxfordjournals.org/content/early/2016/11/18/FINALLINKHERE)
| [astro-ph](https://arxiv.org/abs/1611.05259)

**Authors:** Robert Nikutta, Claudia Agliozzo

**License:** All code under BSD 3-clause, please see [LICENSE](./LICENSE) file. Use and have fun.

**Version:** 2016-11-17

*Data files:*

`em_map\*fits`: Emission measure maps for S61 at 9 and 17 GHZ. Masked at 3-sigma level.

`err_em_map\*fits`: Corresponding error maps.

*Source code:*

[plots.py](./plots.py): Python source code to generate several figures from the paper

[computations.py](./computations.py): Python source code for some computations, e.g. fitting EM maps with [RHOCUBE](https://github.com/rnikutta/rhocube)

This directory also contains required auxiliary data files, models, etc.

**More content to come shortly, stay tuned!!**

!["Gallery of come RHOCUBE models"](https://github.com/rnikutta/s61-supplements/blob/master/rhocube_gallery.png)
