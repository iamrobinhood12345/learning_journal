# learning_journal

A learning journal built in python on the Pyramid framework.

## Setup

### Testing:

Create a postgres database:

```bash
createdb test_learning_journal1
```

Export database environment variable:

```bash
export DATABASE_URL="postgres://name@localhost:5432/test_learning_journal1"
```

Run tests:

```bash
tox
```

### Production:

Create a postgres database:

```bash
createdb \<dbname>
```

Export database environment variable:

```bash
export DATABASE_URL="\<dburl>"
```

Fill database:

```bash
initialize_db development.ini
```


## Tox


    learning_journal/tests/tests.py .......................

    ---------- coverage: platform darwin, python 3.5.2-final-0 -----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                  10      0   100%
    learning_journal/models/__init__.py           22      0   100%
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      0   100%
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      30     18    40%   31-34, 38-56
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             48      5    90%   19-20, 30-31, 56
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        136     25    82%


    =============================== 23 passed in 10.72 seconds ===============================


-

        learning_journal/tests/tests.py .......................

    ---------- coverage: platform darwin, python 2.7.13-final-0 ----------
    Name                                       Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------
    learning_journal/__init__.py                  10      0   100%
    learning_journal/models/__init__.py           22      0   100%
    learning_journal/models/meta.py                5      0   100%
    learning_journal/models/mymodel.py            10      0   100%
    learning_journal/routes.py                     7      0   100%
    learning_journal/scripts/__init__.py           0      0   100%
    learning_journal/scripts/initializedb.py      30     18    40%   31-34, 38-56
    learning_journal/views/__init__.py             0      0   100%
    learning_journal/views/default.py             48      5    90%   19-20, 30-31, 56
    learning_journal/views/notfound.py             4      2    50%   6-7
    ------------------------------------------------------------------------
    TOTAL                                        136     25    82%


    =============================== 23 passed in 10.60 seconds ===============================
