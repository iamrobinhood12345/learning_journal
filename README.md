# learning_journal

A learning journal built in python on the Pyramid framework.

## Setup

Create a postgres database:

```bash
createdb \<dbname>
```

Export database environment variable:

```
export DATABASE_URL="\<dbname>"
```

## Tox

    ================================== test session starts ===================================
    platform darwin -- Python 2.7.13, pytest-3.0.5, py-1.4.32, pluggy-0.4.0
    rootdir: /Users/ben/401/pyramid/learning_journal, inifile: pytest.ini
    plugins: cov-2.4.0
    collected 23 items 

    tests.py .......................

    =============================== 23 passed in 1.64 seconds ================================

-

    platform darwin -- Python 2.7.13, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /Users/ben/401/pyramid/learning_journal, inifile: pytest.ini
    plugins: cov-2.4.0
    collected 23 items 

    learning_journal/tests/tests.py ...........EEEEEEEEEEEE

    ---------- coverage: platform darwin, python 2.7.13-final-0 ----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                  10      6    40%   10-15
    learning_journal/models/__init__.py           22      3    86%   46-49
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      6    14%   2-7
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      30     18    40%   31-34, 38-56
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             48      7    85%   19-20, 30-31, 38, 56, 75
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        136     42    69%


    ========================================= ERRORS =========================================
    _______________________ ERROR at setup of test_index_page_renders ________________________

-

    platform darwin -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /Users/ben/401/pyramid/learning_journal, inifile: pytest.ini
    plugins: cov-2.4.0
    collected 23 items 

    learning_journal/tests/tests.py ...........EEEEEEEEEEEE

    ---------- coverage: platform darwin, python 3.5.2-final-0 -----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                  10      6    40%   10-15
    learning_journal/models/__init__.py           22      3    86%   46-49
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      6    14%   2-7
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      30     18    40%   31-34, 38-56
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             48      7    85%   19-20, 30-31, 38, 56, 75
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        136     42    69%


    ========================================= ERRORS =========================================
    _______________________ ERROR at setup of test_index_page_renders ________________________
