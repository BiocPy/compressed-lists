from typing import List, Optional, Sequence, Union

from biocutils.StringList import StringList

from .base import CompressedList
from .partition import Partitioning
from .split_generic import _generic_register_helper, splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedStringList(CompressedList):
    """CompressedList implementation for lists of strings."""

    def __init__(
        self,
        unlist_data: StringList,
        partitioning: Partitioning,
        element_metadata: Optional[dict] = None,
        metadata: Optional[dict] = None,
        **kwargs,
    ):
        """Initialize a CompressedStringList.

        Args:
            unlist_data:
                List of strings.

            partitioning:
                Partitioning object defining element boundaries.

            element_metadata:
                Optional metadata for elements.

            metadata:
                Optional general metadata.

            kwargs:
                Additional arguments.
        """
        if not isinstance(unlist_data, StringList):
            try:
                unlist_data = StringList(unlist_data)
            except Exception as e:
                raise TypeError("'unlist_data' must be an `StringList`, provided ", type(unlist_data)) from e

        super().__init__(
            unlist_data, partitioning, element_type=StringList, element_metadata=element_metadata, metadata=metadata
        )

    @classmethod
    def from_partitioned_data(
        cls, partitioned_data: List[List], partitioning: Partitioning, metadata: Optional[dict] = None
    ) -> "CompressedStringList":
        """Create `CompressedStringList` from already-partitioned data.

        Args:
            partitioned_data:
                List of lists, each containing strings for one partition.

            partitioning:
                Partitioning object defining the boundaries.

            metadata:
                Optional metadata.

        Returns:
            A new `CompressedStringList`.
        """
        flat_data = []
        for partition in partitioned_data:
            flat_data.extend(partition)

        unlist_data = StringList(flat_data)

        return cls(unlist_data, partitioning, metadata=metadata)


class CompressedCharacterList(CompressedStringList):
    pass


@splitAsCompressedList.register
def _(
    data: StringList,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Sequence[str]] = None,
    metadata: Optional[dict] = None,
) -> CompressedStringList:
    """Handle lists of floats."""

    partitioned_data, groups_or_partitions = _generic_register_helper(
        data=data, groups_or_partitions=groups_or_partitions, names=names
    )

    return CompressedStringList.from_partitioned_data(
        partitioned_data=partitioned_data, partitioning=groups_or_partitions, metadata=metadata
    )
