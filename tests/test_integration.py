# pylint:disable=import-outside-toplevel,duplicate-code
import os
import tempfile
import pytest
from core import CsvReader, AverageRatingReportGenerator, TableRenderer


class TestIntegration:
    """Интеграционные тесты полного пайплайна отчетов."""

    def test_full_pipeline_single_file(self):
        """Полный тест: CSV файл → ридер → генератор → рендерер."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\napple,5\nxiomi,4\napple,3\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            students_data = reader.read()

            assert len(students_data) == 3
            assert students_data[0]["brand"] == "apple"

            generator = AverageRatingReportGenerator(students_data)
            report = generator.generate()

            assert len(report) == 2
            assert report["apple"] == 4.0
            assert report["xiomi"] == 4.0

            renderer = TableRenderer(report)

            import io
            import sys

            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            try:
                renderer.render()
                output = buffer.getvalue()

                assert "apple" in output
                assert "xiomi" in output
                assert "4" in output
                assert "brand" in output
                assert "rating" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(temp_file)

    def test_full_pipeline_multiple_files(self):
        """Тест с несколькими CSV файлами."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f1:
            f1.write("brand,rating\napple,5\nhonor,4.1\n")
            temp_file1 = f1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f2:
            f2.write("brand,rating\napple,3\nxiomi,2\n")
            temp_file2 = f2.name

        try:
            reader = CsvReader([temp_file1, temp_file2])
            students_data = reader.read()

            assert len(students_data) == 4

            generator = AverageRatingReportGenerator(students_data)
            report = generator.generate()

            assert len(report) == 3
            assert report["honor"] == 4.1
            assert report["apple"] == 4.0
            assert report["xiomi"] == 2.0

            sorted_students = list(report.items())
            assert sorted_students[0][0] == "honor"
            assert sorted_students[1][0] == "apple"
            assert sorted_students[2][0] == "xiomi"

            renderer = TableRenderer(report)
            renderer.render()

        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)

    def test_pipeline_with_empty_file(self):
        """Тест пайплайна с пустым файлом (должен упасть на ридере)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])

            with pytest.raises(ValueError, match="Файлы не содержат данных или пустые"):
                reader.read()

        finally:
            os.unlink(temp_file)

    def test_pipeline_with_invalid_data(self):
        """Тест пайплайна с некорректными данными."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\n2,пять\nnokia,1000\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            students_data = reader.read()

            assert len(students_data) == 2

            generator = AverageRatingReportGenerator(students_data)
            with pytest.raises(ValueError, match="Неправильный формат файла"):
                generator.generate()

        finally:
            os.unlink(temp_file)

    def test_pipeline_sorted_output(self):
        """Тест правильной сортировки в финальном выводе."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\nxiomi,4\napple,5\nnokia,4\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            generator = AverageRatingReportGenerator(reader.read())
            report = generator.generate()

            sorted_items = list(report.items())

            assert sorted_items[0] == ("apple", 5.0)
            assert sorted_items[1] == ("nokia", 4.0)
            assert sorted_items[2] == ("xiomi", 4.0)

        finally:
            os.unlink(temp_file)

    def test_pipeline_error_handling(self):
        """Тест обработки ошибок во всем пайплайне."""
        import csv

        reader = CsvReader(["nonexistent_file.csv"])

        with pytest.raises(FileNotFoundError):
            reader.read()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            with pytest.raises((ValueError, csv.Error)):
                reader.read()
        finally:
            os.unlink(temp_file)


class TestReportHandlerIntegration:
    """Интеграционные тесты для ReportHandler."""

    def test_report_handler_full_flow(self):
        """Тест полного потока через ReportHandler."""
        from main import ReportHandler, REPORT_CONFIG

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\nxiomi,5\nsony,4\n")
            temp_file = f.name

        try:
            report_type = "average-rating"
            assert report_type in REPORT_CONFIG

            handler = ReportHandler([temp_file], report_type)

            import io
            import sys

            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            try:
                handler.run()
                output = buffer.getvalue()

                assert "xiomi" in output
                assert "sony" in output
                assert "brand" in output
                assert "rating" in output

            finally:
                sys.stdout = old_stdout

        finally:
            os.unlink(temp_file)

    def test_report_handler_invalid_report_type(self):
        """Тест обработки неверного типа отчета."""
        from main import ReportHandler

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\npocophoooneee,5\n")
            temp_file = f.name

        try:
            with pytest.raises(KeyError):
                ReportHandler([temp_file], "invalid-report-type")

        finally:
            os.unlink(temp_file)
