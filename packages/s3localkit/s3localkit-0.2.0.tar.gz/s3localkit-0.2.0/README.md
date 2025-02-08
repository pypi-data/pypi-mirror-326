# s3localkit

Operations for either local files or files in s3

To pip install

--------------------
```pip install s3localkit```

--------------------

To publish a new version in pip:

```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-<your-api-token>"
python setup.py sdist bdist_wheel
twine upload dist/*
```
