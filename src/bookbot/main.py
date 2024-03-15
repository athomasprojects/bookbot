import dataclasses
import functools
from collections import OrderedDict
from enum import Enum
from pathlib import Path


class BookDir(Enum):
    DIR = "./src/bookbot/books/"


def string_of_dict(d):
    N = len(d)
    s = "{ \n"
    for i, (k, v) in enumerate(d.items()):
        if i <= N - 2:
            s += f"  {repr(k) if ':' not in k else k} : {v},\n"
        else:
            s += f"  {repr(k) if ':' not in k else k} : {v}\n"
    s += "}\n"
    return s


@dataclasses.dataclass(slots=True)
class Book:
    file: Path
    title: str = dataclasses.field(init=False)
    text: str = dataclasses.field(init=False)
    word_count: int = dataclasses.field(init=False)
    freq: dict = dataclasses.field(init=False)

    def __init__(self, file):
        f = Path(BookDir.DIR.value) / Path(file)
        assert f.exists() and f.is_file()
        print(str(file))
        self.file = Path(f)
        self.title = file
        self.read_file()
        self.count_words()
        self.count_frequency()

    def __str__(self):
        return f"File: {self.file}\nContents: {self.text[:34]}\nWord Count: {self.word_count}\nCharacter Frequency: {string_of_dict(self.freq)}\n"

    def read_file(self):
        with open(str(self.file), "r") as f:
            text = f.read()
        self.text = text

    def count_words(self):
        self.word_count = len(self.text.split())

    def count_frequency(self):
        str = self.text.lower()
        chars = {}
        for c in str:
            if c not in chars:
                chars[c] = 1
            else:
                chars[c] += 1
        chars = OrderedDict(sorted(chars.items()))
        self.freq = chars

    def report(self):
        s = f"--- Begin report of '{self.title}' ---\n{self.word_count} words found in the document\n\n"
        for k, v in self.freq.items():
            s += f"The {repr(k) if ':' not in k else k} was found {v} times\n"
        s += "--- End of report ---\n"
        print(s)


def book():
    file = "frankenstein.txt"
    b = Book(file)
    # print(str(b))
    b.report()


if __name__ == "__main__":
    book()
