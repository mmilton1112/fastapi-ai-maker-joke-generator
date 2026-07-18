"""Generate jokes from a CSV data file by keyword or at random."""

from __future__ import annotations

import argparse
import csv
import random
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_JOKES_FILE = Path(__file__).resolve().parent / "data" / "jokes.csv"


@dataclass(frozen=True)
class Joke:
    id: str
    text: str
    category: str
    keywords: str
    date_added: str
    rating: str

    def matches_keyword(self, keyword: str) -> bool:
        needle = keyword.lower().strip()
        if not needle:
            return False

        haystacks = (
            self.text.lower(),
            self.category.lower(),
            self.keywords.lower(),
        )
        return any(needle in value for value in haystacks)


def load_jokes(path: Path = DEFAULT_JOKES_FILE) -> list[Joke]:
    if not path.exists():
        raise FileNotFoundError(f"Joke file not found: {path}")

    jokes: list[Joke] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            jokes.append(
                Joke(
                    id=row["id"],
                    text=row["joke"],
                    category=row["category"],
                    keywords=row["keywords"],
                    date_added=row["date_added"],
                    rating=row["rating"],
                )
            )
    return jokes


def find_jokes_by_keyword(jokes: list[Joke], keyword: str) -> list[Joke]:
    return [joke for joke in jokes if joke.matches_keyword(keyword)]


def get_random_joke(jokes: list[Joke]) -> Joke:
    if not jokes:
        raise ValueError("No jokes available.")
    return random.choice(jokes)


def format_joke(joke: Joke) -> str:
    return (
        f"[#{joke.id}] ({joke.category}, {joke.date_added}, rating {joke.rating}/5)\n"
        f"{joke.text}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Get jokes from a CSV file by keyword or at random."
    )
    parser.add_argument(
        "-k",
        "--keyword",
        help="Search jokes by keyword in text, category, or keywords column.",
    )
    parser.add_argument(
        "-c",
        "--category",
        help="Filter jokes by exact category (e.g. programming, food).",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=1,
        help="Number of jokes to return (default: 1).",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_JOKES_FILE,
        help="Path to jokes CSV file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.count < 1:
        parser.error("--count must be at least 1.")

    try:
        jokes = load_jokes(args.file)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.category:
        jokes = [
            joke
            for joke in jokes
            if joke.category.lower() == args.category.lower()
        ]

    if args.keyword:
        jokes = find_jokes_by_keyword(jokes, args.keyword)
        if not jokes:
            print(f"No jokes found for keyword: {args.keyword}", file=sys.stderr)
            return 1
        selected = random.sample(jokes, k=min(args.count, len(jokes)))
    else:
        try:
            selected = [get_random_joke(jokes) for _ in range(args.count)]
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1

    for index, joke in enumerate(selected, start=1):
        if args.count > 1:
            print(f"Joke {index}:")
        print(format_joke(joke))
        if index < len(selected):
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
