import csv
from abc import ABC, abstractmethod


class ReportReader(ABC):

    @abstractmethod
    def read(self): ...


class CsvReader(ReportReader):

    def __init__(self, files: list[str]):
        self.files = files

    def read(self) -> list[dict[str, str]]:
        students = []

        for file in self.files:
            with open(file, newline="", encoding="utf-8") as csvfile:
                c = csv.DictReader(csvfile)

                for i in c:
                    students.append(i)
                csvfile.close()
        return students
