[bumpversion]
current_version = 0.1.0
commit = True
tag = True

[bumpversion:file:setup.py]
search = version='{current_version}'
replace = version='{new_version}'

[bumpversion:file:test/__init__.py]
search = __version__ = '{current_version}'
replace = __version__ = '{new_version}'

[wheel]
universal = 1

[sdist_wheel]
universal = 1

[flake8]
exclude = 
    .tox,
    .git,
    __pycache__,
    docs/source/conf.py,
    build,
    dist,
    ext,
    test/fixtures/*,
    *.pyc,
    *.egg-info,
    .cache,
    .eggs

[egg_info]
tag_build = .dev
tag_date = 1

[aliases]
release = egg_info -RDb ''
