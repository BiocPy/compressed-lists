from typing import List, Optional, Sequence, Union

import numpy as np
from biocutils.FloatList import FloatList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import _generic_register_helper, splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedFloatList(CompressedList):
    """CompressedList implementation for lists of floats."""

    def __init__(
        self,
        unlist_data: FloatList,
        partitioning: Partitioning,
        element_metadata: Optional[dict] = None,
        metadata: Optional[dict] = None,
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

    @classmethod
    def from_partitioned_data(
        cls, partitioned_data: List[List], partitioning: Partitioning, metadata: Optional[dict] = None
    ) -> "CompressedFloatList":
        """Create `CompressedFloatList` from already-partitioned data.

        Args:
            partitioned_data:
                List of lists, each containing floats for one partition.

            partitioning:
                Partitioning object defining the boundaries.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedFloatList`.
        """
        flat_data = []
        for partition in partitioned_data:
            flat_data.extend(partition)

        unlist_data = FloatList(flat_data)

        return cls(unlist_data, partitioning, metadata=metadata)


@splitAsCompressedList.register
def _(
    data: FloatList,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Sequence[str]] = None,
    metadata: Optional[dict] = None,
) -> CompressedFloatList:
    """Handle lists of floats."""

    partitioned_data, groups_or_partitions = _generic_register_helper(
        data=data, groups_or_partitions=groups_or_partitions, names=names
    )

    return CompressedFloatList.from_partitioned_data(
        partitioned_data=partitioned_data, partitioning=groups_or_partitions, metadata=metadata
    )
