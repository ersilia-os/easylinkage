# Easy record linkage

This small python library is a drop-in replacement for the [recordlinkage](https://github.com/J535D165/recordlinkage/) toolkit. Please read the [documentation](https://recordlinkage.readthedocs.io/en/latest/) of this .

## Main features

* A soft blocking algorithm based on k-Means clustering.
* Default comparisons for names, dates, identifiers, etc.
* Automated complex comparisons, based on multiple types of similarities.
* Smart binarization of the data to make it compatible with the classical ECM algorithm.
* Ensemble-based version of the ECM algorithm to reduce the impact of correlated variables.
* Merged dataframe to visualize results.
* All functionalities of the `recordlinkage` package!

## Basic linking example

```python
import easylinkage
import pandas as pd
```

### Read the data

```python
df_a = pd.read_esv
df_b = pd.read_csv
```

### Preprocess

```python
df_a
df_b
```

### Index

Usually, comparing all datasets against all is computationally intractable. We can partition the pairwise data, for example, in `k = 5` blocks, using fuzzy similarities of first names and surnames.

```python
indexer = easylinkage.Index()
indexer.softblock(left_on = ['firstname', 'surname'], right_on = ['firstname', 'surname'], k = 5)
pairs = indexer.index(df_a, df_b)
```

### Compare

```python
comp = easylinkage.Compare()
comp.name("firstname", "firstname")
comp.name("surname", "surname")
comp.birthdate("birthdate", "birthdate")
comp.sex("sex", "sex")
comp.location("locname", "locname")
comparison_vectors = comp.compute()
```

### Link

```python
ecm = easylinkage.EnsembleECMClassifier()
ecm.fit(comparison_vectors)
probabilities = ecm.prob(comparison_vectors)
```

### Merge

```python
df_ab = easylinkage.merge(probabilities, df_a["firstname", "surname", "birthdate"], df_b["firstname", "surname", "birthdate"])
```

## Help?



