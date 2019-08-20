# Easy record linkage

This small python library is a drop-in replacement for the [recordlinkage](https://github.com/J535D165/recordlinkage/) toolkit. Please read the [documentation](https://recordlinkage.readthedocs.io/en/latest/) of this .

## Main features

* A soft blocking algorithm based on k-Means clustering.
* Default comparisons for names, dates, identifiers, etc.
* Automated complex comparisons, based on multiple types of similarities.
* Smart binarization of the data to make it compatible with the classical ECM algorithm.
* Ensemble-based version of the ECM algorithm to reduce the impact of correlated variables.
* A merged method to postprocess the results.
* All functionalities of the `recordlinkage` package!

## Basic linking example

```python
import easylinkage
import pandas as pd
```

### Read the data

```python
df_a = pd.read_csv(FIRST_DATAFRAME)
df_b = pd.read_csv(SECOND_DATAFRAME)
```

### Preprocess

```python
from easylinkage.preprocessing import clean
df_a["firstname"] = clean(df_a["firstname"])
```

### Index

Usually, comparing all datasets against all is computationally intractable. We can partition the pairwise data, for example, in `k = 5` blocks, using fuzzy similarities of first names and surnames.

```python
indexer = easylinkage.Index()
indexer.softblock(left_on = ['firstname', 'surname'], right_on = ['firstname', 'surname'], k = 5)
pairs = indexer.index(df_a, df_b)
```

### Compare

This is the most important part of the 

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
from easylinkage.postprocessing import merge
df_ab = merge(probabilities, df_a["firstname", "surname", "birthdate"], df_b["firstname", "surname", "birthdate"])
```

## TO-DO

* Add more default comparisons, such as between identifiers.
* Test scalability.

## Need help?

Please contact [](miquelduranfrigola@gmail.com) for questions regarding the **Easy linkage** library.



