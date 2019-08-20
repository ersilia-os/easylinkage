# -*- coding: utf-8 -*-

import pandas as pd

def merge(probabilities, x, x_link, multiindex = True):
    data = {}
    columns = []
    if not multiindex:
        data["index.x"] = probabilities.index.labels[0]
        data["index.y"] = probabilities.index.labels[1]
        columns += ["index.x"]
        columns += ["index.y"]
    data["proba"] = probabilities.values
    columns += ["proba"]
    for c in x.columns:
        data[c + ".x"] = x.iloc[probabilities.index.labels[0]][c].values
        columns += [c + ".x"]
    for c in x_link.columns:
        data[c + ".y"] = x_link.iloc[probabilities.index.labels[1]][c].values
        columns += [c + ".y"]
    if multiindex:
        df = pd.DataFrame(data = data, index = probabilities.index)
    else:
        df = pd.DataFrame(data = data)
        df = df.sort_values(by = ["index.x", "proba"], ascending = [True, False])
        df = df.reset_index(drop = True)
    df = df[columns]
    return df
