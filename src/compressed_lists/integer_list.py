from typing import Optional, Sequence, Union

from biocutils.IntegerList import IntegerList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList, _generic_register_helper

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedIntegerList(CompressedList):
    """CompressedList implementation for lists of integers."""

    def __init__(
        self,
        unlist_data: IntegerList,
        partitioning: Partitioning,
        element_metadata: Optional[dict] = None,
        metadata: Optional[dict] = None,
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

    @classmethod
    def from_partitioned_data(
        cls, partitioned_data: Sequence[IntegerList], partitioning: Partitioning, metadata: Optional[dict] = None
    ) -> "CompressedIntegerList":
        """Create `CompressedIntegerList` from already-partitioned data.

        Args:
            partitioned_data:
                List of `IntegerList`'s, each containing integers for one partition.

            partitioning:
                Partitioning object defining the boundaries.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedIntegerList`.
        """

        flat_data = []
        for partition in partitioned_data:
            flat_data.extend(partition)

        unlist_data = IntegerList(flat_data)

        return cls(unlist_data, partitioning, metadata=metadata)


@splitAsCompressedList.register
def _(
    data: IntegerList,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Sequence[str]] = None,
    metadata: Optional[dict] = None,
) -> CompressedIntegerList:
    """Handle lists of integers."""

    partitioned_data, groups_or_partitions = _generic_register_helper(
        data=data, groups_or_partitions=groups_or_partitions, names=names
    )

    return CompressedIntegerList.from_partitioned_data(
        partitioned_data=partitioned_data, partitioning=groups_or_partitions, metadata=metadata
    )
