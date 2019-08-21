from recordlinkage.datasets import load_febrl4
import pandas as pd

def load():
    # Load data
    df_a, df_b = load_febrl4()
    # Left dataset
    df_a["firstname"] = df_a["given_name"]
    df_a["surname"] = df_a["surname"]
    df_a["birthdate"] = pd.to_datetime(df_a["date_of_birth"], errors = "coerce")
    df_a["location"] = df_a["state"]
    # Right dataset
    df_b["givenname"] = df_b["given_name"]
    df_b["familyname"] = df_b["surname"]
    df_b["dateofbirth"] = pd.to_datetime(df_b["date_of_birth"], errors = "coerce")
    df_b["site"] = df_b["state"]
    df_a = df_a[["firstname", "surname", "birthdate", "location"]]
    df_b = df_b[["givenname", "familyname", "dateofbirth", "site"]]
    return df_a, df_b
