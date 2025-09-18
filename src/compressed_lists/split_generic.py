from functools import singledispatch
from typing import Any, List

import numpy as np
from base import CompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@singledispatch
def splitAsCompressedList(data: Any, names: List[str] = None, metadata: dict = None) -> CompressedList:
    """Generic function to split data into an appropriate `CompressedList` subclass.

    This function uses single dispatch to automatically choose the right
    `CompressedList` subclass based on the data type. Third parties can
    register their own types by using the @splitAsCompressedList.register
    decorator.

    Args:
        data:
            The data to split into a `CompressedList`.

        names:
            Optional names for the list elements.

        metadata:
            Optional metadata for the `CompressedList`.

    Returns:
        An appropriate `CompressedList` subclass instance.
    """
    raise NotImplementedError(f"No `splitAsCompressedList` implementation for type {type(data)}.")


@splitAsCompressedList.register
def _(data: list, names: List[str] = None, metadata: dict = None) -> CompressedList:
    """Handle regular Python lists by inspecting element types."""
    if not data:
        raise ValueError("Cannot create `CompressedList` from empty list.")

    first_element = None
    for item in data:
        if item and len(item) > 0:
            first_element = item[0]
            break

    if first_element is None:
        raise ValueError("All elements are empty, cannot determine type")

    if isinstance(first_element, int):
        from integer_list import CompressedIntegerList

        return CompressedIntegerList.from_list(data, names, metadata)
    elif isinstance(first_element, str):
        from string_list import CompressedCharacterList

        return CompressedCharacterList.from_list(data, names, metadata)
    elif isinstance(first_element, float):
        from float_list import CompressedFloatList

        return CompressedFloatList.from_list(data, names, metadata)
    elif isinstance(first_element, float):
        from bool_list import CompressedBooleanList

        return CompressedBooleanList.from_list(data, names, metadata)
    elif isinstance(first_element, np.ndarray):
        from numpy_list import CompressedNumpyList

        return CompressedNumpyList.from_list(data, names, metadata)
    else:
        raise NotImplementedError(f"No `CompressedList` implementation for element type {type(first_element)}.")
