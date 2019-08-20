import recordlinkage.config_init  # noqa

from recordlinkage.api import Compare, Index
from recordlinkage.index import FullIndex
from recordlinkage.index import BlockIndex
from recordlinkage.index import SortedNeighbourhoodIndex
from recordlinkage.index import RandomIndex
from recordlinkage.classifiers import *
from recordlinkage.measures import *
from recordlinkage.network import *
from recordlinkage.utils import split_index, index_split
from recordlinkage.config import (get_option, set_option, reset_option,
                                  describe_option, option_context, options)
from recordlinkage import rl_logging as logging

from recordlinkage.deprecated import *

from recordlinkage import preprocessing
from recordlinkage import datasets

from .index import *
from .compare import *
from .classifiers import *