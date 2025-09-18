from typing import List, Union

from biocutils.BooleanList import BooleanList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedBooleanList(CompressedList):
    """CompressedList implementation for lists of booleans."""

    def __init__(
        self,
        unlist_data: BooleanList,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
        **kwargs,
    ):
        """Initialize a CompressedBooleanList.

        Args:
            unlist_data:
                List of booleans.

            partitioning:
                Partitioning object defining element boundaries.

            element_metadata:
                Optional metadata for elements.

            metadata:
                Optional general metadata.

            kwargs:
                Additional arguments.
        """

        if not isinstance(unlist_data, BooleanList):
            try:
                unlist_data = BooleanList(unlist_data)
            except Exception as e:
                raise TypeError("'unlist_data' must be an `BooleanList`, provided ", type(unlist_data)) from e

        super().__init__(
            unlist_data, partitioning, element_type=BooleanList, element_metadata=element_metadata, metadata=metadata
        )


@splitAsCompressedList.register
def _(
    data: Union[List[List[bool]], List[BooleanList]], names: List[str] = None, metadata: dict = None
) -> CompressedBooleanList:
    """Handle lists of boolean."""
    return CompressedBooleanList.from_list(data, names, metadata)
