import sys
import json
import re
from argparse import ArgumentParser, ArgumentTypeError, FileType
from io import TextIOWrapper
from typing import Dict, List
from collections import defaultdict

DEFAULT_PATH_TO_STORE_INVERTED_INDEX = "inverted.index"


class EncodedFileType(FileType):
    def __call__(self, string):
        if string == "-":
            if "r" in self._mode:
                return TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
            if "w" in self._mode:
                return TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
            raise ValueError(f"argument '-' with mode {self._mode!r}")

        try:
            return open(string, self._mode, self._bufsize, self._encoding, self._errors)
        except OSError as exception:
            raise ArgumentTypeError(f"can't open '{string}': {exception}")


class InvertedIndex:
    def __init__(self, words_ids: Dict[str, List[int]]):
        self.words_ids = words_ids

    def query(self, words: List[str]) -> List[int]:
        sets = [set(self.words_ids.get(word, [])) for word in words]
        return sorted(set.intersection(*sets)) if sets else []

    def dump(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.words_ids, f)

    @classmethod
    def load(cls, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            words_ids = json.load(f)
        words_ids = {word: list(map(int, ids)) for word, ids in words_ids.items()}
        return cls(words_ids)


def load_documents(filepath: str) -> Dict[int, str]:
    documents = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            doc_id, content = line.lower().split("\t", 1)
            documents[int(doc_id)] = content.strip()
    return documents


def build_inverted_index(documents: Dict[int, str]) -> InvertedIndex:
    inverted = defaultdict(set)
    stop_words = {
        "the", "a", "an", "is", "of", "and", "in", "on", "it", "to", "by", "for"
    }

    for doc_id, text in documents.items():
        words = re.split(r"\W+", text)
        for word in words:
            if word and word not in stop_words:
                inverted[word].add(doc_id)

    inverted = {word: sorted(list(doc_ids)) for word, doc_ids in inverted.items()}
    return InvertedIndex(inverted)


def callback_build(arguments) -> None:
    return process_build(arguments.dataset, arguments.output)


def process_build(dataset, output) -> None:
    documents = load_documents(dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(output)


def callback_query(arguments) -> None:
    process_query(arguments.query, arguments.index)


def process_query(queries, index) -> None:
    inverted_index = InvertedIndex.load(index)
    if hasattr(queries, 'read'):
        queries = [line.strip().split() for line in queries if line.strip()]
    for query in queries:
        if isinstance(query, str):
            query = query.strip().split()
        print(" ".join(query))
        print(",".join(str(doc_id) for doc_id in inverted_index.query(query)))


def setup_subparsers(parser) -> None:
    subparser = parser.add_subparsers(dest="command")

    build_parser = subparser.add_parser("build", help="Build inverted index from dataset")
    build_parser.add_argument(
        "-d", "--dataset",
        required=True,
        help="Path to dataset file"
    )
    build_parser.add_argument(
        "-o", "--output",
        default=DEFAULT_PATH_TO_STORE_INVERTED_INDEX,
        help="Path to save inverted index (default: %(default)s)"
    )
    build_parser.set_defaults(callback=callback_build)

    query_parser = subparser.add_parser("query", help="Query the inverted index")
    query_parser.add_argument(
        "--index",
        default=DEFAULT_PATH_TO_STORE_INVERTED_INDEX,
        help="Path to inverted index file (default: %(default)s)"
    )
    query_group = query_parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        "-q", "--query",
        dest="query",
        action="append",
        nargs="+",
        help="Queries as inline word lists"
    )
    query_group.add_argument(
        "--query_from_file",
        dest="query",
        type=EncodedFileType("r", encoding="utf-8"),
        help="Path to query file"
    )
    query_parser.set_defaults(callback=callback_query)


def main():
    parser = ArgumentParser(description="Inverted Index CLI")
    setup_subparsers(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
