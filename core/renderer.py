from abc import ABC, abstractmethod
import tabulate


class ReportRenderer(ABC):
    """Абстрактный класс вывода отсчетов позволяет добавить различные вариаци выводв"""

    @abstractmethod
    def render(self): ...


class TableRenderer(ReportRenderer):
    """Класс для удобного вывода отсчетов в табличном виде"""

    def __init__(self, report: dict[str, float | int]) -> None:
        self.report = report

    def render(self) -> None:
        """Отображает отсчет в табличном виде"""
        table = []
        for i, (k, v) in enumerate(self.report.items(), start=1):
            val = (i, k, v)
            table.append(val)
        print(
            tabulate.tabulate(table, headers=[" ", "brand", "rating"], tablefmt="psql")
        )
