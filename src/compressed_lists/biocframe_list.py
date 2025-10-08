from typing import List, Union

from biocframe import BiocFrame

from .base import CompressedList
from .partition import Partitioning
from .split_generic import splitAsCompressedList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class CompressedBiocFrameList(CompressedList):
    """CompressedList for BiocFrames."""

    def __init__(
        self,
        unlist_data: BiocFrame,
        partitioning: Partitioning,
        element_metadata: dict = None,
        metadata: dict = None,
        **kwargs,
    ):
        super().__init__(
            unlist_data, partitioning, element_type="BiocFrame", element_metadata=element_metadata, metadata=metadata
        )

    @classmethod
    def from_list(cls, lst: List[BiocFrame], names: List[str] = None, metadata: dict = None):
        partitioning = Partitioning.from_list(lst, names)
        return cls(lst, partitioning, metadata=metadata)

    def __getitem__(self, key: Union[int, str, slice]):
        """Override to handle column extraction using `splitAsCompressedList`.

        When extracting a column, this will automatically dispatch to the
        appropriate `CompressedList` subclass based on the column data type.
        """
        if isinstance(key, str):
            column_data = []
            for df in self.unlist_data:
                if key in df.columns:
                    column_data.append(df[key].tolist())
                else:
                    column_data.append([])

            return splitAsCompressedList(column_data, names=self.names, metadata=self.metadata)
        else:
            return super().__getitem__(key)

    @classmethod
    def _from_partitioned_data(cls, partitioned_data: List, partitioning: Partitioning, metadata: dict = None) -> "CompressedBiocFrameList":
        """Create CompressedBiocFrameList from already-partitioned data.
        
        Args:
            partitioned_data: List of BiocFrame objects (already partitioned)
            partitioning: Partitioning object defining the boundaries  
            metadata: Optional metadata
            
        Returns:
            A new CompressedBiocFrameList
        """
        # For BiocFrame, the partitioned_data should already be a list of BiocFrame objects
        # so we can use it directly as unlist_data
        return cls(partitioned_data, partitioning, metadata=metadata)


@splitAsCompressedList.register
def _(data: List[BiocFrame], names: List[str] = None, metadata: dict = None) -> CompressedBiocFrameList:
    """Handle lists of boolean."""
    return CompressedBiocFrameList.from_list(data, names, metadata)
