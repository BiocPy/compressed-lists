[![PyPI-Server](https://img.shields.io/pypi/v/compressed-lists.svg)](https://pypi.org/project/compressed-lists/)
![Unit tests](https://github.com/BiocPy/compressed-lists/actions/workflows/run-tests.yml/badge.svg)

# CompressedList Implementation in Python

This module provides a Python implementation of the CompressedList class from R/Bioconductor.
CompressedList is an [efficient] way to store list-like objects by concatenating elements into
a single vector-like object and maintaining partitioning information.

## Install

To get started, install the package from [PyPI](https://pypi.org/project/compressed-lists/)

```bash
pip install compressed-lists
```

```py
# Create a CompressedIntegerList
data = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
names = ["A", "B", "C"]

int_list = CompressedIntegerList.from_list(data, names)
print(f"CompressedIntegerList: {int_list}")
print(f"Length: {len(int_list)}")
print(f"Names: {int_list.names}")
print(f"Element lengths: {int_list.element_lengths()}")
print(f"First element: {int_list[0]}")
print(f"Element 'B': {int_list['B']}")
print(f"Slice [1:3]: {int_list[1:3]}")

# Create a CompressedCharacterList
char_data = [["apple", "banana"], ["cherry", "date", "elderberry"], ["fig"]]
char_list = CompressedCharacterList.from_list(char_data)
print(f"\nCompressedCharacterList: {char_list}")

# Convert to list
regular_list = int_list.to_list()
print(f"\nRegular list: {regular_list}")

# Apply function to each element
squared = int_list.lapply(lambda x: [i**2 for i in x])
print(f"\nSquared: {squared}")
```

<!-- biocsetup-notes -->

## Note

This project has been set up using [BiocSetup](https://github.com/biocpy/biocsetup)
and [PyScaffold](https://pyscaffold.org/).
