from collections import defaultdict
from functools import singledispatch
from typing import Any, List, Optional, Sequence, Tuple, Union

import biocutils as ut
import numpy as np

from .partition import Partitioning

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def groups_to_partition(
    data: Any, groups: list, names: Optional[Union[ut.Names, Sequence[str]]] = None
) -> Tuple[List[Any], Partitioning]:
    """Convert group membership vector to partitioned data and Partitioning object.

    Args:
        data:
            The data to be split (flat vector-like object).

        groups:
            Group membership vector, same length as data.

        names:
            Optional names for groups.

    Returns:
        Tuple of (partitioned_data_list, partitioning_object)
    """
    if len(data) != len(groups):
        raise ValueError(f"Length of data ({len(data)}) must match length of groups ({len(groups)})")

    group_idx_dict = defaultdict(list)
    for idx, group in enumerate(groups):
        group_idx_dict[group].append(idx)

    group_dict = defaultdict(list)
    for key, val in group_idx_dict.items():
        group_dict[key] = ut.subset(data, val)

    sorted_groups = sorted(group_dict.keys())
    partitioned_data = [group_dict[group] for group in sorted_groups]

    if names is None:
        group_names = [str(group) for group in sorted_groups]
    else:
        if len(names) != len(sorted_groups):
            raise ValueError(
                f"Length of names ({len(names)}) must match number of unique groups ({len(sorted_groups)})"
            )
        group_names = names

    partitioning = Partitioning.from_list(partitioned_data, group_names)
    return partitioned_data, partitioning


@singledispatch
def splitAsCompressedList(
    data: Any,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Union[ut.Names, Sequence[str]]] = None,
    metadata: Optional[dict] = None,
) -> Any:
    """Generic function to split data into an appropriate `CompressedList` subclass.

    This function can work in two modes:
    1. Group-based splitting where a flat vector is split according to group membership.
    2. Partition-based splitting where a flat vector is split according to explicit partitions.

    Args:
        data:
            The data to split into a `CompressedList`.

        groups_or_partitions:
            Optional group membership vector (same length as data) or
            explicit partitioning object.

        names:
            Optional names for the list elements.

        metadata:
            Optional metadata for the `CompressedList`.

    Returns:
        An appropriate `CompressedList` subclass instance.
    """
    element_type = type(data)
    try:
        if isinstance(groups_or_partitions, Partitioning):
            partitioned_data = []
            for i in range(len(groups_or_partitions)):
                start, end = groups_or_partitions.get_partition_range(i)
                _part = data[start:end]
                partitioned_data.append(_part)
        else:
            if isinstance(groups_or_partitions, np.ndarray):
                groups_or_partitions = groups_or_partitions.tolist()

            group_idx_dict = defaultdict(list)
            for idx, group in enumerate(groups_or_partitions):
                group_idx_dict[group].append(idx)

            group_dict = defaultdict(list)
            for key, val in group_idx_dict.items():
                group_dict[key] = ut.subset(data, val)

            sorted_groups = sorted(group_dict.keys())
            partitioned_data = [group_dict[group] for group in sorted_groups]

        return partitioned_data
    except Exception as e:
        raise NotImplementedError(f"No `splitAsCompressedList` dispatcher found for element type {element_type}") from e


def _generic_register_helper(data, groups_or_partitions, names=None):
    if groups_or_partitions is None:
        raise ValueError("'groups_or_paritions' cannot be 'None'.")

    if data is None:
        raise ValueError("'data' cannot be empty.")

    if isinstance(groups_or_partitions, Partitioning):
        if names is not None:
            groups_or_partitions = groups_or_partitions.set_names(names, in_place=False)

        # TODO: probably not necessary to split when groups is a partition object.
        # unless ordering matters
        # partitioned_data = []
        # for i in range(len(groups_or_partitions)):
        #     start, end = groups_or_partitions.get_partition_range(i)
        #     partitioned_data.append(data[start:end])
        partitioned_data = data
    elif isinstance(groups_or_partitions, (list, np.ndarray)):
        if isinstance(groups_or_partitions, np.ndarray):
            groups_or_partitions = groups_or_partitions.tolist()

        partitioned_data, groups_or_partitions = groups_to_partition(data, groups=groups_or_partitions, names=names)

        if partitioned_data is None:
            raise ValueError("No data after grouping")
    else:
        raise ValueError("'groups_or_paritions' must be a group vector or a Partition object.")

    return partitioned_data, groups_or_partitions


@splitAsCompressedList.register(list)
def _(
    data: list,
    groups_or_partitions: Union[list, Partitioning],
    names: Optional[Union[ut.Names, Sequence[str]]] = None,
    metadata: Optional[dict] = None,
) -> Any:
    """Handle plain Python lists."""
    if len(data) == 0:
        return splitAsCompressedList(ut.StringList([]), groups_or_partitions, names=names, metadata=metadata)

    first = data[0]
    if isinstance(first, str) and all(isinstance(x, str) for x in data):
        return splitAsCompressedList(ut.StringList(data), groups_or_partitions, names=names, metadata=metadata)
    elif isinstance(first, bool) and all(isinstance(x, bool) for x in data):
        return splitAsCompressedList(ut.BooleanList(data), groups_or_partitions, names=names, metadata=metadata)
    elif isinstance(first, int) and all(isinstance(x, int) for x in data):
        return splitAsCompressedList(ut.IntegerList(data), groups_or_partitions, names=names, metadata=metadata)
    elif isinstance(first, float) and all(isinstance(x, (int, float)) for x in data):
        return splitAsCompressedList(ut.FloatList(data), groups_or_partitions, names=names, metadata=metadata)
    else:
        from .base import CompressedList

        partitioned_data, groups_or_partitions = _generic_register_helper(
            data=data, groups_or_partitions=groups_or_partitions, names=names
        )
        if len(partitioned_data) != 0 and not isinstance(partitioned_data, list):
            partitioned_data = ut.combine_sequences(*partitioned_data)
        elif len(partitioned_data) != 0 and isinstance(partitioned_data, list):
            flat = []
            for sub in partitioned_data:
                flat.extend(sub)
            partitioned_data = flat

        assert isinstance(groups_or_partitions, Partitioning)
        return CompressedList(unlist_data=partitioned_data, partitioning=groups_or_partitions, metadata=metadata)
