from abc import ABC, abstractmethod


class ReportGenerator(ABC):
    """Абстрактный класс генерации отсчетов позволяет добавить различные виды отсчетов"""

    @abstractmethod
    def generate(self): ...


class AverageRatingReportGenerator(ReportGenerator):
    """Класс для генерации отсчетов в CSV формате."""

    def __init__(self, products: list[dict[str, str]]):
        self.products = products
        self.report = {}

    def generate(self) -> dict[str, float | int]:
        """Генерирует rating average отсчет с средним значением оценки

        Raises:
            ValueError: если файлы ничего не содержат
            ValueError: если неправильный формат файла

        Returns:
            dict[str, float|int]: словарь с именами продуктов как ключи и
                                их цена как значение,
                                отсортированный по цене и по имени продукта
        """
        res = {}
        if not self.products:
            raise ValueError("Файлы ничего не содержат")
        try:
            for product in self.products:
                if product["brand"] not in self.report:
                    self.report[product["brand"]] = [float(product["rating"])]
                else:
                    self.report[product["brand"]].extend([float(product["rating"])])
            for key, val in self.report.items():
                res[key] = sum(val) / len(val)
        except ValueError as e:
            raise ValueError(f"Неправильный формат файла: {e}") from e

        res = dict(sorted(res.items(), key=lambda item: (-item[1], item[0])))
        return res


class AveragePriceReportGenerator(ReportGenerator):
    """Класс для генерации отсчетов в CSV формате."""

    def __init__(self, products: list[dict[str, str]]):
        self.products = products
        self.report = {}

    def generate(self) -> dict[str, float | int]:
        res = {}
        if not self.products:
            raise ValueError("Файлы ничего не содержат")
        try:
            for product in self.products:
                if product["brand"] not in self.report:
                    self.report[product["brand"]] = [float(product["price"])]
                else:
                    self.report[product["brand"]].extend([float(product["price"])])
            for key, val in self.report.items():
                res[key] = sum(val) / len(val)
        except ValueError as e:
            raise ValueError(f"Неправильный формат файла: {e}") from e

        res = dict(sorted(res.items(), key=lambda item: (-item[1], item[0])))
        return res
