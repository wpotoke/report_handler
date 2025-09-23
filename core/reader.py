import csv
from abc import ABC, abstractmethod


class ReportReader(ABC):
    """Абстрактный класс чтения отсчетов позволяет читать различные виды отсчетов"""

    @abstractmethod
    def read(self): ...


class CsvReader(ReportReader):
    """Класс для чтения файлов в CSV формате и преобразования их в удобный вид"""

    def __init__(self, files: list[str]):
        self.files = files

    def read(self) -> list[dict[str, str]]:
        """Читатет файлы в CSV формате

        Raises:
            FileNotFoundError: если не найден указанный файл
            csv.Error: если ошибка чтения CSV в файле
            ValueError: если Файлы не содержат данных или пустые

        Returns:
            list[dict[str, str]]: список словарей со всеми значениями из файла
        """
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
