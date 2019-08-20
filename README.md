# Easy record linkage

This library is a drop-in replacement for the [`recordlinkage`](https://github.com/J535D165/recordlinkage/) python library. Please read the [Record Linkage Toolkit documentation](https://recordlinkage.readthedocs.io/en/latest/) for a complete guidance.

Here, we simply extend the `recordlinkage` library with a few functionalities that make it easy to use in the context of medical databases.

## Main features

* A soft blocking indexing algorithm based on k-Means clustering.
* Default comparisons for names, dates, identifiers, etc.
* Automated complex comparisons, based on multiple types of similarities.
* Agnostic binarization of the data to make it compatible with the classical Expectation Condition Maximization (ECM) algorithm.
* Ensemble-based version of the ECM algorithm to reduce the impact of highly correlated variables.
* A merging method to postprocess the linkage results.
* ...and all functionalities of the `recordlinkage` package!

## Basic linking example

This library is bound to [pandas](https://pandas.pydata.org/) data frames, which are commonly used in data manipulation projects. To get started, import both libraries.

```python
import easylinkage
import pandas as pd
```

### Read the data

Start by loading the two datasets of interest.

```python
df_a = pd.read_csv(YOUR_FIRST_DATASET)
df_b = pd.read_csv(YOUR_SECOND_DATASET)
```

### Preprocess

Data [preprocessing](https://recordlinkage.readthedocs.io/en/latest/ref-preprocessing.html) is an important and time-consuming step. The better the processing, the more accurate the linkage will be. For instance, one should normalize (clean) text fields.

```python
from easylinkage.preprocessing import clean
df_a["firstname"] = clean(df_a["firstname"])
```

### Index

Comparing all records against all may be computationally intractable, and it is advisable to reduce the search space. We can partition the pairwise matrix in `k = 5` blocks using fuzzy similarities between names.

```python
indexer = easylinkage.Index()
indexer.softblock(left_on = ['firstname', 'surname'], right_on = ['givenname', 'familyname'], k = 5)
pairs = indexer.index(df_a, df_b)
```

For large datasets, other [indexing techniques](https://recordlinkage.readthedocs.io/en/latest/ref-index.html) can be used.

### Compare

This is the most important part of the procedure. We need to specify what fields are to be compared. The `Compare` class has several built-in functions to easily compare fields.

```python
comp = easylinkage.Compare()
comp.name("firstname", "givenname", expand = True)
comp.name("surname", "familyname")
comp.birthdate("birthdate", "dateofbirth")
comp.sex("sex", "sex")
comp.location("location", "site")
comparison_vectors = comp.compute(df_a, df_b)
```

By default, these instructions will use multiple (expanded) types of similarities between fields. If a faster comparison is desired, we can turn off the expansion (`expand = False`).

### Link

Most machine-learning based linkage algorithms are [supervised](https://recordlinkage.readthedocs.io/en/latest/notebooks/classifiers.html#Supervised-learning), meaning they require training data (i.e. known linked pairs). [Unsupervised](https://recordlinkage.readthedocs.io/en/latest/notebooks/classifiers.html#Unsupervised-learning) algorithms are typically slower, but can function without previously known links. A classical algorithm is ECM, which we have adapted to work robustly as an ensemble-learning approach.

```python
ecm = easylinkage.EnsembleECMClassifier()
ecm.fit(comparison_vectors)
probabilities = ecm.prob(comparison_vectors)
```

### Merge

Now that we have matching probabilities for each candidate pair, we can merge results in a data frame.

```python
from easylinkage.postprocessing import merge
df_ab = merge(probabilities, df_a, df_b)
```

## Work in progress

The **Easy linkage** library is currently being tested and we do recommend to use 

* Add more built-in comparisons (e.g. identifiers).
* Test scalability.
* Smart sampling based on prior probabilities.
* Add different degrees of expansion.

## Need help?

Please contact <miquelduranfrigola@gmail.com> for questions regarding the **Easy linkage** library.



