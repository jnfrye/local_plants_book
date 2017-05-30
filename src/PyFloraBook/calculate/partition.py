import pandas as pd


def _partitions(n: int):
    """Generate partitions of the integer in lexicographic order.
    """
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return

    # modify partitions of n-1 to form partitions of n
    for p in _partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]


def find_best_partitioning(
        dataframe: pd.DataFrame, value_column: str,
        partition_size: float, smallest_partition: float) -> pd.DataFrame:
    """Find the partitioning of the data that minimizes the error.

    Args:
        dataframe:
            Dataframe containing the data to be partitioned.
        value_column:
            Header of the column containing the values
        partition_size:
            Total size of the partitioning
        smallest_partition:
            All partitionings are multiples of this value

    Returns:
        Dataframe containing the best partitioning for each row
    """
    num_entries = len(dataframe)

    partition_table = pd.DataFrame({
        'partitioning': [0] * num_entries,
        'best_partitioning': [0] * num_entries
        }, index=dataframe.index)

    # Normalize and sort the values
    partition_table['values'] = \
        dataframe[value_column] / dataframe[value_column].sum()
    partition_table.sort_values('values', inplace=True)

    assert (-0.00005 < partition_table['values'].sum() - 1. < 0.00005), \
        "Normalization of partition table failed!"

    # Each partition is checked to see how much error it has against the ideal
    # partitioning, and the best is selected.
    best_error = float("inf")
    for partition in _partitions(int(partition_size / smallest_partition)):
        # Fill the rest of the partition with zeros
        partitioning = pd.Series(
            [0] * (num_entries - len(partition)) + list(partition),
            index=partition_table.index)

        partition_table['partitioning'] = partitioning * smallest_partition
        error = sum(
            abs(partition_table['partitioning']
                - partition_table['values'] * partition_size))

        if error < best_error:
            best_error = error
            partition_table['best_partitioning'] = \
                partition_table['partitioning']

        print(error, best_error, " ... ", partition[len(partition) - 4:])

    del partition_table['partitioning']
    # Return only non-zero partitions
    return partition_table[partition_table["best_partitioning"] > 0]