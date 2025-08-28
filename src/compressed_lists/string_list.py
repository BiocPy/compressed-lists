from biocutils.StringList import StringList

from .base import CompressedList
from .partition import Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedStringList(CompressedList):
    """CompressedList implementation for lists of strings."""

    def __init__(
        self,
        unlist_data: StringList,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
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


class CompressedCharacterList(CompressedStringList):
    pass
