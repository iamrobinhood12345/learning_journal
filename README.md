# learning journal

A learning journal built with the Pyramid framework.

## Tox:

    learning_journal/tests/tests.py .....................

    ---------- coverage: platform darwin, python 3.5.2-final-0 -----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                   8      0   100%
    learning_journal/models/__init__.py           22      0   100%
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      0   100%
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      28     17    39%   30-33, 37-54
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             47      5    89%   17-18, 28-29, 55
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        131     24    82%


    ======================= 21 passed in 2.83 seconds =======================


  
-

    learning_journal/tests/tests.py .....................

    ---------- coverage: platform darwin, python 2.7.13-final-0 ----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                   8      0   100%
    learning_journal/models/__init__.py           22      0   100%
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      0   100%
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      28     17    39%   30-33, 37-54
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             47      5    89%   17-18, 28-29, 55
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        131     24    82%


    ======================= 21 passed in 1.63 seconds =======================
