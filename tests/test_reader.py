# pylint:disable=duplicate-code
import tempfile
import os
import pytest
from core.reader import CsvReader


class TestCsvReader:
    """Тесты для CsvReader."""

    def test_read_valid_csv(self):
        """Тест чтения корректного CSV файла."""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\nxiomi,4.5\napple,4.3\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            result = reader.read()

            assert len(result) == 2
            assert result[0] == {"brand": "xiomi", "rating": "4.5"}
            assert result[1] == {"brand": "apple", "rating": "4.3"}

        finally:
            os.unlink(temp_file)

    def test_read_multiple_files(self):
        """Тест чтения нескольких CSV файлов."""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f1:
            f1.write("brand,rating\napple,2.3\n")
            temp_file1 = f1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f2:
            f2.write("brand,rating\nxiomi,5")
            temp_file2 = f2.name

        try:
            reader = CsvReader([temp_file1, temp_file2])
            result = reader.read()

            assert len(result) == 2
            assert result[0]["brand"] == "apple"
            assert result[1]["brand"] == "xiomi"

        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)

    def test_read_empty_file(self):
        """Тест чтения пустого CSV файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brand,rating\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])

            with pytest.raises(ValueError, match="Файлы не содержат данных"):
                reader.read()

        finally:
            os.unlink(temp_file)

    def test_read_nonexistent_file(self):
        """Тест чтения несуществующего файла."""
        reader = CsvReader(["nonexistent_file.csv"])

        with pytest.raises(FileNotFoundError, match="Не найден указанный файл"):
            reader.read()

    def test_read_invalid_csv_format(self):
        """Тест чтения CSV с некорректным форматом."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("brandname,rating_value\nxiomi,12.3\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])

            result = reader.read()
            assert result == [{"brandname": "xiomi", "rating_value": "12.3"}]

        finally:
            os.unlink(temp_file)

    def test_read_empty_file_list(self):
        """Тест поведения при пустом списке файлов."""
        reader = CsvReader([])

        with pytest.raises(ValueError, match="Файлы не содержат данных или пустые"):
            reader.read()


if __name__ == "__main__":
    pytest.main([__file__])
