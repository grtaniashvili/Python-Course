# from collections import defaultdict as dd
from itertools import product
from typing import Any, Dict, List, Tuple
#from pygments.lexer import words
def task_1(data_1: Dict[str, int], data_2: Dict[str, int]):
    result = data_1.copy()
    for key, value in data_2.items():
        if key in result:
            result[key] += value
        else:
            result[key] = value
    return result
def task_2():
    return {x: x**2 for x in range(1, 16)}
def task_3(data: Dict[Any, List[str]]):
    values_lists = data.values()
    combinations = product(*values_lists)
    return [''.join(combo) for combo in combinations]
def task_4(data: Dict[str, int]):
    sorted_keys = sorted(data, key=data.get, reverse=True)
    return sorted_keys[:3]
def task_5(data: List[Tuple[Any, Any]]) -> Dict[str, List[int]]:
    result: Dict[str, List[int]] = {}
    for key, value in data:
        if key in result:
            result[key].append(value)
        else:
            result[key] = [value]
    return result
def task_6(data: List[Any]):
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    return result
def task_7(words: [List[str]]) -> str:
    if not words:
        return ""
    result: List[str] = []
    for i in range(len(words)-1):
        check = words[i]
        for word in words[i+1:]:
            prefix = check
            while not word.startswith(prefix):
                prefix = prefix[:-1]
            if prefix not in result and len(prefix)>0:
                result.append(prefix)
    if len(result) == 0: return ""
    return max(result, key=len)
def task_8(haystack: str, needle: str) -> int:
    if needle == "":
        return 0
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    return -1
