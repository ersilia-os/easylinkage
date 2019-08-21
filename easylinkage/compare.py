# -*- coding: utf-8 -*-

import pandas as pd
from recordlinkage import preprocessing
from recordlinkage import Compare as BaseCompare

class Compare(BaseCompare):
    
    # Utils
    
    def _add_exp(self, expfun, left_on, right_on):
        if not hasattr(self, "expands"):
            self.expands = [(expfun, left_on, right_on)]
        else:
            self.expands += [(expfun, left_on, right_on)]
    
    # Expand functions
    
    @staticmethod
    def _expand_identifier(df, col):
        pass
    
    @staticmethod
    def _expand_name(df, col):
        df[col] = preprocessing.clean(df[col])
        df[col+"---initial"] = df[col].str[0]
        df[col+"---soundex"] = preprocessing.phonetic(df[col], method = "soundex")
        df[col+"---nysiis"] = preprocessing.phonetic(df[col], method = "nysiis")
        df[col+"---metaphone"] = preprocessing.phonetic(df[col], method = "metaphone")

    @staticmethod
    def _expand_birthdate(df, col):
        df[col] = pd.to_datetime(df[col], errors = "coerce")
        df[col+"---string"] = df[col].dt.strftime('%Y-%m-%d')
        df[col+"---year"] = df[col].dt.year

    @staticmethod
    def _expand_sex(df, col):
        df[col] = preprocessing.clean(df[col])

    @staticmethod
    def _expand_location(df, col):
        df[col] = preprocessing.clean(df[col])
            
    # Compare functions (higher order than the recordlinkage package ones)
    
    def identifier(self, left_on, right_on, label = None, expand = True):
        pass
        
    def name(self, left_on, right_on, expand = True):
        if expand:
            # Expansions
            self._add_exp(self._expand_name, left_on, right_on)
            # Comparisons
            self.exact(left_on, right_on,
                       label = left_on + right_on)
            self.string(left_on, right_on,
                        method = "jarowinkler",
                        label = left_on + right_on + "---jarowinkler")
            self.exact(left_on + "---initial", right_on + "---initial",
                       label = left_on + right_on + "---initial")
            self.exact(left_on + "---soundex", right_on + "---soundex",
                       label = left_on + right_on + "---soundex")
            self.exact(left_on + "---nysiis", right_on + "---nysiis",
                       label = left_on + right_on + "---nysiis")
            self.exact(left_on + "---metaphone", right_on + "---metaphone",
                       label = left_on + right_on + "---metaphone")
        else:
            # Default
            self.string(left_on, right_on,
                        method = "jarowinkler",
                        label = left_on + right_on + "---jarowinkler")
            
    def birthdate(self, left_on, right_on, expand = True):
        if expand:
            # Expansions
            self._add_exp(self._expand_birthdate, left_on, right_on)
            # Comparisons
            self.date(left_on, right_on,
                      label = left_on + right_on)
            self.string(left_on + "---string", right_on + "---string",
                        method = "jarowinkler",
                        label = left_on + right_on + "---jarowinkler")
            self.numeric(left_on + "---year", right_on + "---year",
                         label = left_on + right_on + "---year")
        else:
            # Default
            self.date(left_on, right_on,
                      label = left_on + right_on)

    def sex(self, left_on, right_on, expand = True):
        if expand:
            # Expansions
            self._add_exp(self._expand_sex, left_on, right_on)
            # Comparisons
            self.exact(left_on, right_on,
                       label = left_on + right_on)
        else:
            # Default
            self.exact(left_on, right_on,
                       label = left_on + right_on)

    def location(self, left_on, right_on, expand = True):
        if expand:
            # Expansions
            self._add_exp(self._expand_location, left_on, right_on)
            # Comparisons
            self.exact(left_on, right_on,
                       label = left_on + right_on)
            self.string(left_on, right_on,
                        method = "jarowinkler",
                        label = left_on + right_on + "---jarowinkler")            
        else:
            # Default
            self.string(left_on, right_on,
                        method = "jarowinkler", threshold = 0.85,
                        label = left_on + right_on + "---jarowinkler")

    # Compute method    
    
    def compute(self, pairs, x, x_link):
        x = x.copy()
        x_link = x_link.copy()
        for expand in self.expands:
            exp_fun  = expand[0]
            left_on  = expand[1]
            right_on = expand[2]
            exp_fun(x, left_on)
            exp_fun(x_link, right_on)
        return super().compute(pairs, x, x_link)
