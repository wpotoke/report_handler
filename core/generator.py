from abc import ABC, abstractmethod


class ReportGenerator(ABC):

    @abstractmethod
    def generate(self): ...


class CsvReportGenerator(ReportGenerator):
    def __init__(self, students: list[dict]):
        self.students = students
        self.report = {}

    def generate(self):
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
            raise ValueError(f"Ошибочный формат файла: {e}") from e

        res = dict(sorted(res.items(), key=lambda item: (-item[1], item[0])))
        return res
