from typing import Optional, Sequence, Union

from biocutils.BooleanList import BooleanList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import _generic_register_helper, splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedBooleanList(CompressedList):
    """CompressedList implementation for lists of booleans."""

    def __init__(
        self,
        unlist_data: BooleanList,
        partitioning: Partitioning,
        element_metadata: Optional[dict] = None,
        metadata: Optional[dict] = None,
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

    @classmethod
    def from_partitioned_data(
        cls, partitioned_data: Sequence[BooleanList], partitioning: Partitioning, metadata: Optional[dict] = None
    ) -> "CompressedBooleanList":
        """Create `CompressedBooleanList` from already-partitioned data.

        Args:
            partitioned_data:
                List of `BooleanList`'s, each containing booleans for one partition.

            partitioning:
                Partitioning object defining the boundaries.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedBooleanList`.
        """
        unlist_data = partitioned_data
        if isinstance(partitioned_data, list):
            flat_data = []
            for partition in partitioned_data:
                flat_data.extend(partition)

            unlist_data = BooleanList(flat_data)

        return cls(unlist_data, partitioning, metadata=metadata)


@splitAsCompressedList.register
def _(
    data: BooleanList,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Sequence[str]] = None,
    metadata: Optional[dict] = None,
) -> CompressedBooleanList:
    """Handle lists of booleans."""

    partitioned_data, groups_or_partitions = _generic_register_helper(
        data=data, groups_or_partitions=groups_or_partitions, names=names
    )

    return CompressedBooleanList.from_partitioned_data(
        partitioned_data=partitioned_data, partitioning=groups_or_partitions, metadata=metadata
    )
