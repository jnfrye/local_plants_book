"""Functions of scalars"""


def is_normed(scalar: float, *, threshold=0.001) -> bool:
    """Check if input is roughly equal to 1.

    Args:
        scalar:     input to check
        threshold:  acceptable deviation from 1

    Returns:
        True if within threshold of 1.
    """
    return abs(1. - scalar) < threshold
