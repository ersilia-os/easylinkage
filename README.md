# Easy record linkage

This small python library is a drop-in replacement for the [recordlinkage](https://github.com/J535D165/recordlinkage/) toolkit. Please read the [documentation](https://recordlinkage.readthedocs.io/en/latest/).

## Main features

* A soft blocking algorithm based on k-means clustering.
* Default comparisons for names, dates, identifiers, etc.
* Automated complex comparisons.
* Smart binarization of the data to make it compatible with the classical ECM algorithm.
* Ensemble-based version of the ECM algorithm to reduce the impact of correlated variables.

## Basic linking example

```python
import easylinkage
import pandas as pd

```

Usually, comparing all datasets against all is computationally intractable. We can partition the pairwise data, for example, in `k = 5` blocks, using fuzzy similarities of first names and surnames.

```python
indexer = recordlinkage.Index()
indexer.softblock(left_on = ['firstname', 'surname'], right_on = ['firstname', 'surname'], k = 5)
pairs = indexer.index(df_a, df_b)
```