from typing import List, Union

from biocutils.FloatList import FloatList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList

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
            unlist_data, partitioning, element_type=FloatList, element_metadata=element_metadata, metadata=metadata
        )


@splitAsCompressedList.register
def _(
    data: Union[List[List[float]], List[FloatList]], names: List[str] = None, metadata: dict = None
) -> CompressedFloatList:
    """Handle lists of floats."""
    return CompressedFloatList.from_list(data, names, metadata)
