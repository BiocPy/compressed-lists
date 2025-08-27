from typing import List, Optional, Sequence

import numpy as np
from biocutils.IntegerList import IntegerList

from .base import CompressedList
from .partition import Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedNumpyList(CompressedList):
    """CompressedList implementation for lists of NumPy vectors."""

    def __init__(
        self,
        unlist_data: np.ndarray,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
        **kwargs,
    ):
        """Initialize a CompressedNumpyList.

        Args:
            unlist_data:
                NumPy vector.

            partitioning:
                Partitioning object defining element boundaries.

            element_metadata:
                Optional metadata for elements.

            metadata:
                Optional general metadata.

            kwargs:
                Additional arguments.
        """

        if not isinstance(unlist_data, np.ndarray):
            try:
                unlist_data = np.array(unlist_data)
            except Exception as e:
                raise TypeError("'unlist_data' must be an `np.ndarray`, provided ", type(unlist_data)) from e

        print(unlist_data)
        super().__init__(
            unlist_data, partitioning, element_type="ndarray", element_metadata=element_metadata, metadata=metadata
        )

    def _extract_range(self, start: int, end: int) -> np.ndarray:
        """Extract a range from unlist_data.

        Args:
            start:
                Start index (inclusive).

            end:
                End index (exclusive).

        Returns:
            Same type as unlist_data.
        """
        return self._unlist_data[start:end]

    @classmethod
    def from_list(
        cls, lst: List[List[np.ndarray]], names: Optional[Sequence[str]] = None, metadata: dict = None
    ) -> "CompressedNumpyList":
        """
        Create a `CompressedNumpyList` from a list of NumPy vectors.

        Args:
            lst:
                List of NumPy vectors.

            names:
                Optional names for list elements.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedNumpyList`.
        """

        # Create partitioning
        partitioning = Partitioning.from_list(lst, names)

        # Create unlist_data
        if len(lst) == 0:
            unlist_data = np.array([])
        else:
            unlist_data = np.hstack(lst)

        return cls(unlist_data, partitioning, metadata=metadata)
