
# Link
https://pypi.python.org/pypi/fipipkg


# .pypirc
```
mkdir ~/.pypirc
chmod 600 ~/.pypirc
vim ~/.pypirc

[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://pypi.python.org/pypi
username: <username>
password: <password>

[pypitest]
repository: https://testpypi.python.org/pypi
username: <username>
password: <password>
```

# upload
```
pip install twine
```

```
python setup.py sdist
python setup.py bdist_wheel

twine register dist/*.whl
twine upload dist/*
```


