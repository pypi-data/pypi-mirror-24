from __future__ import absolute_import


import functools
import inspect

import pandas as pd
from sklearn import base
from .._adapter import  frame


def _wrap_transform_type(fn):
    @functools.wraps(fn)
    def wrapped(self, X, *args, **kwargs):
        ret = fn(self, X, *args, **kwargs)
        if isinstance(ret, pd.DataFrame):
            ret.columns = ['comp_%i' % i for i in range(len(ret.columns))]
        return ret
    return wrapped


def _from_pickle(est, params):
    est = frame(est)

    _update_est(est)

    return est(**params)


def _update_est(est):
    est.transform = _wrap_transform_type(est.transform)
    est.fit_transform = _wrap_transform_type(est.fit_transform)
    est.__reduce__ = lambda self: (_from_pickle, (inspect.getmro(est)[1], self.get_params(deep=True), ))


_extra_doc = """

Transformers in this module label their columns as ``comp_0``, ``comp_1``, and so on.

Example

    >>> import pandas as pd
    >>> import numpy as np
    >>> from ibex.sklearn import datasets
    >>> from ibex.sklearn.decomposition import PCA as PDPCA

    >>> iris = datasets.load_iris()
    >>> features = iris['feature_names']
    >>> iris = pd.DataFrame(
    ...     np.c_[iris['data'], iris['target']],
    ...     columns=features+['class'])

    >>> iris[features]
       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
    0                5.1               3.5                1.4               0.2
    1                4.9               3.0                1.4               0.2
    2                4.7               3.2                1.3               0.2
    3                4.6               3.1                1.5               0.2
    4                5.0               3.6                1.4               0.2
    ...

    >>> PDPCA(n_components=2).fit(iris[features], iris['class']).transform(iris[features])
           comp_0    comp_1
    0   -2.684207  0.326607
    1   -2.715391 -0.169557
    2   -2.889820 -0.137346
    3   -2.746437 -0.311124
    4   -2.728593  0.333925
    ...

"""


def update_module(name, module):
    if name != 'decomposition':
        return

    module.__doc__ += _extra_doc

    for name in dir(module):
        c = getattr(module, name)
        try:
            if not issubclass(c, base.TransformerMixin):
                continue
        except TypeError:
            continue
        _update_est(c)





