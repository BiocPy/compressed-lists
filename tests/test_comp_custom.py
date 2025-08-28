from typing import List

import pytest

from compressed_lists import CompressedList, Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def CompressedCustomFloatList():
    class CompressedCustomFloatList(CompressedList):
        def __init__(
            self,
            unlist_data: List[float],
            partitioning: Partitioning,
            element_metadata: dict = None,
            metadata: dict = None,
        ):
            super().__init__(
                unlist_data, partitioning, element_type="float", element_metadata=element_metadata, metadata=metadata
            )

        def extract_range(self, start: int, end: int) -> List[float]:
            return self._unlist_data[start:end]

        @classmethod
        def from_list(
            cls, lst: List[List[float]], names: list = None, metadata: dict = None
        ) -> "CompressedCustomFloatList":
            flat_data = []
            for sublist in lst:
                flat_data.extend(sublist)

            partitioning = Partitioning.from_list(lst, names)
            return cls(flat_data, partitioning, metadata=metadata)

    return CompressedCustomFloatList


def test_custom_class(CompressedCustomFloatList):
    float_data = [[1.1, 2.2, 3.3], [4.4, 5.5], [6.6, 7.7, 8.8, 9.9]]
    names = ["X", "Y", "Z"]
    float_list = CompressedCustomFloatList.from_list(float_data, names)

    assert len(float_list) == 3
    assert float_list._element_type == "float"
    assert list(float_list.names) == names
    assert float_list["Y"] == [4.4, 5.5]

    # Test lapply
    rounded = float_list.lapply(lambda x: [round(f, 0) for f in x])
    assert rounded[0] == [1.0, 2.0, 3.0]
    assert rounded[1] == [4.0, 6.0]
    assert rounded[2] == [7.0, 8.0, 9.0, 10.0]
