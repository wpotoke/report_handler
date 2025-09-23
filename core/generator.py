from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    """Абстрактный класс генерации отсчетов позволяет добавить различные виды отсчетов"""

    @abstractmethod
    def generate(self): ...


class CsvReportGenerator(ReportGenerator):
    """Класс для генерации отсчетов в CSV формате."""

    def __init__(self, students: list[dict[str, str]]):
        self.students = students
        self.report = {}

    def generate(self) -> dict[str, float | int]:
        """Генерирует student performance отсчет с средним значением оценки

        Raises:
            ValueError: если файлы ничего не содержат
            ValueError: если неправильный формат файла

        Returns:
            dict[str, float|int]: словарь с именами студентов как ключи и
                                их среднее значение оценки как значение,
                                отсортированный по оценке и по имени студентаю
        """
        res = {}
        if not self.students:
            raise ValueError("Файлы ничего не содержат")
        try:
            for student in self.students:
                if student["student_name"] not in self.report:
                    self.report[student["student_name"]] = [int(student["grade"])]
                else:
                    self.report[student["student_name"]].extend([int(student["grade"])])
            for key, val in self.report.items():
                res[key] = sum(val) / len(val)
        except ValueError as e:
            raise ValueError(f"Неправильный формат файла: {e}") from e

        res = dict(sorted(res.items(), key=lambda item: (-item[1], item[0])))
        return res
