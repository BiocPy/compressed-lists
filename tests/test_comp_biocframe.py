import pytest
from biocframe import BiocFrame

from compressed_lists import CompressedBiocFrameList, Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def frame_data():
    return BiocFrame(
        {
            "ensembl": ["ENS00001", "ENS00002", "ENS00003"],
            "symbol": ["MAP1A", "BIN1", "ESR1"],
        }
    )


def test_creation(frame_data):
    frame_list = CompressedBiocFrameList(frame_data, partitioning=Partitioning.from_lengths([1, 2]))

    assert isinstance(frame_list, CompressedBiocFrameList)
    assert len(frame_list) == 2
    assert isinstance(frame_list.unlist_data, BiocFrame)
    assert len(frame_list.get_unlist_data()) == 3
    assert list(frame_list.get_element_lengths()) == [1, 2]
    print(frame_list._unlist_data)
    print(frame_list[0])
    assert frame_list[0].get_column("symbol") == ["MAP1A"]
