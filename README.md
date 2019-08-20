# Easy record linkage

This python library is a drop-in replacement for the [recordlinkage](https://github.com/J535D165/recordlinkage/) toolkit. Please read the [Record Linkage Toolkit documentation](https://recordlinkage.readthedocs.io/en/latest/) for a complete and up-to-date guidance.

Here, we simply extend the `recordlinkage` library with a few functionalities to make it easy to use for medical records data.

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
df_a = pd.read_csv(YOUR_FIRST_DATASET)
df_b = pd.read_csv(YOUR_SECOND_DATASET)
```

### Preprocess

Data [preprocessing](https://recordlinkage.readthedocs.io/en/latest/ref-preprocessing.html) is an important step. The better the processing, the more accurate the linkage will be. For example, you would like to clean:

```python
from easylinkage.preprocessing import clean
df_a["firstname"] = clean(df_a["firstname"])
```

### Index

Comparing all records against all may be computationally intractable, and it is advisable to reduce the search space. For instance, we can partition the pairwise matrix in `k = 5` blocks using fuzzy similarities between names.

```python
indexer = easylinkage.Index()
indexer.softblock(left_on = ['firstname', 'surname'], right_on = ['firstname', 'surname'], k = 5)
pairs = indexer.index(df_a, df_b)
```

The higher the number of partitions, the less pairs will be considered. For large datasets, other [indexing techniques](https://recordlinkage.readthedocs.io/en/latest/ref-index.html) such as `sortedneighborhood` can be used.

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

## Work in progress

The **Easy linkage** library is currently being tested and we do recommend to use 

* Add more default comparisons, such as between identifiers.
* Test scalability.

## Need help?

Please contact <miquelduranfrigola@gmail.com> for questions regarding the **Easy linkage** library.



