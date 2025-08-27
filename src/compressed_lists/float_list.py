from typing import List, Optional, Sequence

from biocutils.FloatList import FloatList

from .base import CompressedList
from .partition import Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedFloatList(CompressedList):
    """CompressedList implementation for lists of floats."""

    def __init__(
        self,
        unlist_data: FloatList,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
        **kwargs,
    ):
        """Initialize a CompressedFloatList.

        Args:
            unlist_data:
                List of floats.

            partitioning:
                Partitioning object defining element boundaries.

            element_metadata:
                Optional metadata for elements.

            metadata:
                Optional general metadata.

            kwargs:
                Additional arguments.
        """

        if not isinstance(unlist_data, FloatList):
            try:
                unlist_data = FloatList(unlist_data)
            except Exception as e:
                raise TypeError("'unlist_data' must be an `FloatList`, provided ", type(unlist_data)) from e

        super().__init__(
            unlist_data, partitioning, element_type="float", element_metadata=element_metadata, metadata=metadata
        )

    def _extract_range(self, start: int, end: int) -> FloatList:
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
        cls, lst: List[List[float]], names: Optional[Sequence[str]] = None, metadata: dict = None
    ) -> "CompressedFloatList":
        """
        Create a `CompressedFloatList` from a list of float lists.

        Args:
            lst:
                List of float lists.

            names:
                Optional names for list elements.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedFloatList`.
        """
        # Flatten the list
        flat_data = []
        for sublist in lst:
            flat_data.extend(sublist)

        # Create partitioning
        partitioning = Partitioning.from_list(lst, names)

        # Create unlist_data
        unlist_data = FloatList(data=flat_data)

        return cls(unlist_data, partitioning, metadata=metadata)
