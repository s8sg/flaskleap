[tox]
envlist = py33, py35, py37

[testenv]
setenv =
    PYTHONPATH = {toxinidir}:{toxinidir}/{{ service_name }}
deps =
    -r{toxinidir}/requirements.txt
    pytest
commands =
    python setup.py coverage

[testenv:flake8]
deps =
    -r{toxinidir}/requirements.txt
    flake8
commands =
    python setup.py flake8
