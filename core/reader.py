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
            try:
                with open(file, newline="", encoding="utf-8") as csvfile:
                    c = csv.DictReader(csvfile)

                    for i in c:
                        students.append(i)
            except FileNotFoundError as e:
                raise FileNotFoundError(
                    f"Не найден указанный файл {file}, проверьте название файла"
                ) from e
            except csv.Error as e:
                raise csv.Error(f"Ошибка чтения CSV в файле {file}: {e}") from e
        if not students:
            raise ValueError("Файлы не содержат данных или пустые")
        return students
