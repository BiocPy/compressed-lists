from typing import List, Union

from biocutils.IntegerList import IntegerList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedIntegerList(CompressedList):
    """CompressedList implementation for lists of integers."""

    def __init__(
        self,
        unlist_data: IntegerList,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
        **kwargs,
    ):
        """Initialize a CompressedIntegerList.

        Args:
            unlist_data:
                List of integers.

            partitioning:
                Partitioning object defining element boundaries.

            element_metadata:
                Optional metadata for elements.

            metadata:
                Optional general metadata.

            kwargs:
                Additional arguments.
        """

        if not isinstance(unlist_data, IntegerList):
            try:
                unlist_data = IntegerList(unlist_data)
            except Exception as e:
                raise TypeError("'unlist_data' must be an `IntegerList`, provided ", type(unlist_data)) from e

        super().__init__(
            unlist_data, partitioning, element_type=IntegerList, element_metadata=element_metadata, metadata=metadata
        )


@splitAsCompressedList.register
def _(
    data: Union[List[List[int]], List[IntegerList]], names: List[str] = None, metadata: dict = None
) -> CompressedIntegerList:
    """Handle lists of integers."""
    return CompressedIntegerList.from_list(data, names, metadata)
