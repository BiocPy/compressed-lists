import pytest
from biocutils import StringList

from compressed_lists import CompressedStringList

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def char_data():
    return [["apple", "banana"], ["cherry", "date", "elderberry"], ["fig"]]


@pytest.fixture
def char_list(char_data):
    names = ["fruits1", "fruits2", "fruits3"]
    return CompressedStringList.from_list(char_data, names)


def test_creation(char_data):
    char_list = CompressedStringList.from_list(char_data)

    assert len(char_list) == 3
    assert isinstance(char_list.unlist_data, StringList)
    assert list(char_list.get_unlist_data()) == ["apple", "banana", "cherry", "date", "elderberry", "fig"]
    assert list(char_list.get_element_lengths()) == [2, 3, 1]


def test_getitem(char_list):
    assert list(char_list[0]) == ["apple", "banana"]
    assert list(char_list["fruits2"]) == ["cherry", "date", "elderberry"]


def test_lapply(char_list):
    uppercased = char_list.lapply(lambda x: [s.upper() for s in x])

    assert len(uppercased) == len(char_list)
    assert list(uppercased[0]) == ["APPLE", "BANANA"]
    assert list(uppercased[1]) == ["CHERRY", "DATE", "ELDERBERRY"]
    assert list(uppercased[2]) == ["FIG"]


def test_from_list_no_warning(char_data):
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        clist = CompressedStringList.from_list(char_data)
        assert len(clist) == 3


def test_from_list_preserves_names():
    import biocutils as ut

    # from dict
    d = {"fruits1": ["apple", "banana"], "fruits2": ["cherry"]}
    clist_dict = CompressedStringList.from_list(d)
    assert list(clist_dict.names) == ["fruits1", "fruits2"]
    assert list(clist_dict["fruits1"]) == ["apple", "banana"]
    assert list(clist_dict["fruits2"]) == ["cherry"]

    # from NamedList
    nl = ut.NamedList([["apple", "banana"], ["cherry"]], names=["f1", "f2"])
    clist_nl = CompressedStringList.from_list(nl)
    assert list(clist_nl.names) == ["f1", "f2"]
    assert list(clist_nl["f1"]) == ["apple", "banana"]


def test_print_representation(char_list, char_data):
    # Named print
    printed_named = str(char_list)
    assert "CompressedStringList of length 3" in printed_named
    assert '[["fruits1"]] apple banana' in printed_named
    assert '[["fruits2"]] cherry date elderberry' in printed_named
    assert '[["fruits3"]] fig' in printed_named

    # Unnamed print
    unnamed = CompressedStringList.from_list(char_data)
    printed_unnamed = str(unnamed)
    assert "CompressedStringList of length 3" in printed_unnamed
    assert "[[0]] apple banana" in printed_unnamed
    assert "[[1]] cherry date elderberry" in printed_unnamed
    assert "[[2]] fig" in printed_unnamed


def test_to_list_elements(char_list):
    # list(csl) returns list of StringLists
    as_list_objs = list(char_list)
    assert len(as_list_objs) == 3
    assert isinstance(as_list_objs[0], StringList)

    # csl.to_list(as_lists=False) returns list of StringLists
    assert isinstance(char_list.to_list(as_lists=False)[0], StringList)

    # csl.to_list(as_lists=True) returns list of plain lists
    plain_lists = char_list.to_list(as_lists=True)
    assert isinstance(plain_lists[0], list)
    assert not isinstance(plain_lists[0], StringList)


def test_splitAsCompressedList_on_list():
    from compressed_lists import splitAsCompressedList

    split_res = splitAsCompressedList(["apple", "banana", "cherry"], [1, 1, 2])
    assert isinstance(split_res, CompressedStringList)
    assert len(split_res) == 2
    assert list(split_res[0]) == ["apple", "banana"]
    assert list(split_res[1]) == ["cherry"]
