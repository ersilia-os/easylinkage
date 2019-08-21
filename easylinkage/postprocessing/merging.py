# -*- coding: utf-8 -*-

import pandas as pd

def merge(probabilities, x, x_link, min_proba = 0.5):
    data = {}
    columns = []
    data = probabilities.copy()
    data = data.reset_index()
    data.columns = ["index.x", "index.y", "proba"]
    columns += ["index.x", "index.y", "proba"]
    for c in x.columns:
        data[c + ".x"] = x.loc[data["index.x"]][c].values
        columns += [c + ".x"]
    for c in x_link.columns:
        data[c + ".y"] = x_link.loc[data["index.y"]][c].values
        columns += [c + ".y"]
    df = pd.DataFrame(data = data)
    df = df.sort_values(by = ["index.x", "proba"], ascending = [True, False])
    df = df.reset_index(drop = True)
    df = df[columns]
    return df[df["proba"] >= min_proba]
