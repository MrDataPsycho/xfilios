#!/bin/bash

echo "=== Sorting with ISORT ==="
isort . --line-length=150 --profile=hug

echo "=== Formatting with AUTOPEP8 ==="
autopep8 . --max-line-length=150 \
  --in-place \
  --recursive \
  --aggressive \
  --ignore=F821,W292,E302,E305,W391,W503,W504

#autoflake --in-place --remove-unused-variables --remove-all-unused-imports

