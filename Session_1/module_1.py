from typing import List


def task_1(array: List[int], target: int) -> List[int]:
    list = []
    for num in array:
        check_value = target - num
        if check_value in array:
            if check_value not in list:
                list.append(num)
                list.append(check_value)
    return list


def task_2(number: int) -> int:
    result = 0
    while number > 0:
        digit = number % 10
        result *= 10
        result += digit
        number //= 10
    return result


def task_3(array: List[int]) -> int:
    for i in range(len(array)):
        val = array[i]
        if val in array[i+1:]:
            return val
    return -1


def task_4(string: str) -> int:
    roman_map = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }

    total = 0
    prev_value = 0

    for char in reversed(string):
        value = roman_map[char]
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value
    return total


def task_5(array: List[int]) -> int:
    if len(array) == 0:
        return None

    smallest = array[0]
    for num in array[1:]:
        if num < smallest:
            smallest = num
    return smallest

