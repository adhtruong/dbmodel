# DBModel

<p align="center">
    <a href="https://codecov.io/gh/adhtruong/dbmodel">
        <img src="https://codecov.io/gh/adhtruong/dbmodel/main/graph/badge.svg?token=4I7OINJKAO"/>
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/pre-commit/pre-commit">
        <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="pre-commit" style="max-width:100%;">
    </a>
</p>

Utils and wrappers for SQLAlchemy.

```python
from db_model import register, PrimaryKey

# Make SQLAlchemy model based on annotations.
@register
class MyModel:
    id: PrimaryKey[int]
    name: str

```

## TODO

- [ ] Add documentation
- [ ] Add testing
- [ ] Add main decorator
- [ ] Allow better configuration
- [ ] Improve mypy plugin
  - Intercept dataclass transformer so descriptor can be transformed before generating init.
- [x] Make pip installable

## Development Set Up

```
    pip install -r requirements-dev.txt
    pre-commit install
```
