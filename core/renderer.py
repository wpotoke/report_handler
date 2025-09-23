from abc import ABC, abstractmethod
import tabulate


class ReportRenderer(ABC):

    @abstractmethod
    def render(self): ...


class TableRenderer(ReportRenderer):
    def __init__(self, report):
        self.report = report

    def render(self) -> None:
        table = []
        for i, (k, v) in enumerate(self.report.items(), start=1):
            val = (i, k, v)
            table.append(val)
        print(
            tabulate.tabulate(
                table, headers=[" ", "student_name", "grade"], tablefmt="psql"
            )
        )
