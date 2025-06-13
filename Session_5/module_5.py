import os
from pathlib import Path
from random import choice, seed
from typing import List, Union
from collections import Counter
import re
import requests
from requests.exceptions import RequestException


S5_PATH = Path(os.path.realpath(__file__)).parent


PATH_TO_NAMES = S5_PATH / "names.txt"
PATH_TO_SURNAMES = S5_PATH / "last_names.txt"
PATH_TO_OUTPUT = S5_PATH / "sorted_names_and_surnames.txt"
PATH_TO_TEXT = S5_PATH / "random_text.txt"
PATH_TO_STOP_WORDS = S5_PATH / "stop_words.txt"


def task_1():
    seed(1)
    with open(PATH_TO_NAMES, 'r', encoding='utf-8') as f:
        names = sorted([line.strip().lower() for line in f if line.strip()])
    with open(PATH_TO_SURNAMES, 'r', encoding='utf-8') as f:
        surnames = [line.strip().lower() for line in f if line.strip()]
    with open(PATH_TO_OUTPUT, 'w', encoding='utf-8') as f:
        for name in names:
            full_name = f"{name} {choice(surnames)}"
            f.write(full_name + '\n')


def task_2(top_k: int):
    with open(PATH_TO_TEXT, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    with open(PATH_TO_STOP_WORDS, 'r', encoding='utf-8') as f:
        stop_words = set(word.strip().lower() for word in f if word.strip())
    words = re.findall(r'\b[a-z]+\b', text)
    filtered_words = [word for word in words if word not in stop_words]
    counter = Counter(filtered_words)
    return counter.most_common(top_k)


def task_3(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except RequestException as e:
        raise e


def task_4(data: List[Union[int, str, float]]):
    total = 0.0
    for value in data:
        try:
            total += float(value)
        except (TypeError, ValueError):
            continue
    return total


def task_5():
    try:
        a, b = input().split()
        result = float(a) / float(b)
        print(result)
    except ZeroDivisionError:
        print("Can't divide by zero")
    except ValueError:
        print("Entered value is wrong")
