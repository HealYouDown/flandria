def probability_to_float(
    probability: int,
    total: int = 10_000,
) -> float:
    """Converts a given probability value to the respective float
    value (0 - 1).

    Args:
        probability (int): Probabiltiy value.
        total (int, optional): The total value. Defaults to 10_000.

    Returns:
        float: Probability value as float ranging from 0 to 1.
    """
    return probability / total
