# -*- coding: utf-8 -*-

def merge(probabilities, x, x_link, multiindex = True):

    

	pass




def linkage(dfc, dfq, dft, ensemble):
    raws  = raw_match(dfc)
    probas = ensemble_ecm_probabilities(dfc, ensemble)
    dfl = pd.DataFrame(data = {"index.q": probas.index.labels[0],
                               "index.t": probas.index.labels[1],
                               "raw": raws.values,
                               "proba": probas.values,
                               "firstname.q": dfq.iloc[probas.index.labels[0]]["firstname"].values,
                               "surname.q": dfq.iloc[probas.index.labels[0]]["surname"].values,
                               "birthdate.q": dfq.iloc[probas.index.labels[0]]["birthdate"].values,
                               "firstname.t": dft.iloc[probas.index.labels[1]]["firstname"].values,
                               "surname.t": dft.iloc[probas.index.labels[1]]["surname"].values,
                               "birthdate.t": dft.iloc[probas.index.labels[1]]["birthdate"].values})
    dfl = dfl[["index.q", "index.t", "raw", "proba", "firstname.q", "surname.q", "birthdate.q", "firstname.t", "surname.t", "birthdate.t"]]
    dfl = dfl[dfl.proba >= min_prob]
    dfl = dfl.sort_values(by = ["index.q", "raw"], ascending = [True, False])
    dfl = dfl.reset_index(drop = True)
    return dfl
