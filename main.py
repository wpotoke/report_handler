import sys
import argparse
import csv
from core import CsvReader, AverageRatingReportGenerator, TableRenderer


REPORT_CONFIG = {
    "average-rating": {
        "reader": CsvReader,
        "generator": AverageRatingReportGenerator,
        "renderer": TableRenderer,
    }
}


class ReportHandler:
    """Управляет полным процессом генерации отчетов.

    Организует последовательность чтения данных, обработки и вывода результатов
    в соответствии с указанным типом отчета и входными файлами."""

    def __init__(self, paths, report_type):
        self.paths = paths
        self.report_type = report_type

        try:
            config = REPORT_CONFIG[report_type]
        except KeyError as e:
            available_reports = " ".join(list(REPORT_CONFIG.keys()))
            raise KeyError(
                f"Не найден тип отсчета: {report_type} - Доступные отсчеты: {available_reports}"
            ) from e

        self.reader = config["reader"]
        self.generator = config["generator"]
        self.renderer = config["renderer"]

    def run(self):
        """Запуск обработки отсчета"""
        data = self.reader(self.paths).read()
        gen_report = self.generator(data).generate()
        self.renderer(gen_report).render()


def main():
    """Основная функция, которая парсит аргументы и запускает обработчик."""
    parser = argparse.ArgumentParser(
        description="Генератор отчетов по оценкам студентов",
        epilog="""
Примеры использования:
  python main.py --files file1.csv file2.csv --report average-rating
        """,
    )

    parser.add_argument(
        "-f",
        "--files",
        type=str,
        dest="file_paths",
        nargs="+",
        required=True,
        help="Пути к CSV файлам",
    )
    parser.add_argument(
        "-r",
        "--report",
        type=str,
        required=True,
        dest="report_type",
        help="Название отсчета, который вы хотите получить",
    )

    args = parser.parse_args()

    try:
        report = ReportHandler(args.file_paths, args.report_type)
        report.run()
    except (KeyError, FileNotFoundError, csv.Error, ValueError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
