from typing import List


def get_fizzbuzz(int1: int, int2: int, limit: int, str1: str, str2: str) -> List[str]:
    """Compute fizz buzz i.e. in numbers from 1 to limit :
        - all multiples of int1 are replaced by str1,
        - all multiples of int2 are replaced by str2
        - all multiples of int1 and int2 are replaced by str1str

    Returns
    -------
    List[str]
        List of numbers from 1 to limit, where some of them were replaced by str1, str2 or str1str2
    """
    result = []
    for i in range(1, limit + 1):
        if i % int1 == 0 and i % int2 == 0:
            result.append(str1 + str2)
        elif i % int1 == 0:
            result.append(str1)
        elif i % int2 == 0:
            result.append(str2)
        else:
            result.append(i)

    return [str(i) for i in result]
