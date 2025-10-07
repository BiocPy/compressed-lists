from typing import List, Optional

import numpy as np

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedNumpyList(CompressedList):
    """CompressedList implementation for lists of NumPy vectors."""

    def __init__(
        self,
        unlist_data: np.ndarray,
        partitioning: Partitioning,
        element_metadata: Optional[dict] = None,
        metadata: Optional[dict] = None,
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

        super().__init__(
            unlist_data, partitioning, element_type=np.array, element_metadata=element_metadata, metadata=metadata
        )

    @classmethod
    def from_list(
        cls, lst: List[List[np.ndarray]], names: Optional[List[str]] = None, metadata: Optional[dict] = None
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

    @classmethod
    def _from_partitioned_data(
        cls, partitioned_data: List[List], partitioning: Partitioning, metadata: Optional[dict] = None
    ) -> "CompressedNumpyList":
        """Create CompressedNumpyList from already-partitioned data.

        Args:
            partitioned_data: List of arrays, each containing numpy data for one partition
            partitioning: Partitioning object defining the boundaries
            metadata: Optional metadata

        Returns:
            A new CompressedNumpyList
        """
        import numpy as np

        # Concatenate the numpy arrays
        if not partitioned_data or not partitioned_data[0]:
            unlist_data = np.array([])
        else:
            unlist_data = np.concatenate(partitioned_data)

        return cls(unlist_data, partitioning, metadata=metadata)


@splitAsCompressedList.register
def _(
    data: np.ndarray,
    names: Optional[List[str]] = None,
    metadata: Optional[dict] = None,
    groups: Optional[list] = None,
    partitions: Optional[Partitioning] = None,
):
    """Handle NumPy arrays."""

    if groups is not None:
        return _splitAsCompressedList_by_groups(data, groups, names, metadata)
    elif partitions is not None:
        return _splitAsCompressedList_by_partitions(data, partitions, names, metadata)
    else:
        # Original behavior: convert single array to list of arrays
        if data.ndim == 1:
            list_data = [data]
        else:
            list_data = [row for row in data]

        from .numpy_list import CompressedNumpyList

        return CompressedNumpyList.from_list(list_data, names, metadata)
