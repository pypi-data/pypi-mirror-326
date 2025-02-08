TODO:


- Airflow?
  - AIRFLOW_CTX_* https://stackoverflow.com/questions/54934732/airflow-how-to-get-env-vars-of-each-dag-from-the-code-itself


- platform module for getting OS/python/arch info `platform.system()` https://docs.python.org/3/library/platform.html
  - OS specifics: `platform.mac_ver()`, `platform.win32_ver()`, etc.
  - Python specifics: `platform.python_version()`, `platform.python_version_tuple()`

Ruff Rules https://docs.astral.sh/ruff/linter/#rule-selection


uv run pytest --cov=ami.envvar --cov-report=html tests/test_envvar.py
