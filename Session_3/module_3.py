import time
from typing import List

Matrix = List[List[int]]


def task_1(exp: int):
    def power_factory(n):
        return n ** exp
    return power_factory


def task_2(*args, **kwags):
    for arg in args:
        print(arg)
    for kwarg in kwags.values():
        print(kwarg)


def helper(func):
    def wrapper(*args, **kwargs):
        print("Hi, friend! What's your name?")
        result = func(*args, **kwargs)
        print("See you soon!")
        return result
    return wrapper


@helper
def task_3(name: str):
    print(f"Hello! My name is {name}.")


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"Finished {func.__name__} in {run_time:.4f} secs")
        return result
    return wrapper


@timer
def task_4():
    return len([1 for _ in range(0, 10**8)])


def task_5(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def task_6(queue: str):
    result = 0
    for char in queue:
        if char == '(':
            result += 1
        elif char == ')':
            result -= 1
    return result == 0
