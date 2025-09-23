import sys
import argparse
import csv
from core import CsvReader, CsvReportGenerator, TableRenderer


REPORT_CONFIG = {
    "student-performance": {
        "reader": CsvReader,
        "generator": CsvReportGenerator,
        "renderer": TableRenderer,
    }
}


class ReportHandler:
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
        data = self.reader(self.paths).read()
        gen_report = self.generator(data).generate()
        self.renderer(gen_report).render()


parser = argparse.ArgumentParser(
    description="Генератор отчетов по оценкам студентов",
    epilog="""
Примеры использования:
  python main.py files/students1.csv files/students2.csv
        """,
)

parser.add_argument(
    "-f",
    "--files",
    type=str,
    dest="file_paths",
    nargs="*",
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

if __name__ == "__main__":
    try:
        report = ReportHandler(args.file_paths, args.report_type)
        report.run()
    except (KeyError, FileNotFoundError, csv.Error, ValueError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
