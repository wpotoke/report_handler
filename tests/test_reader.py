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
            f.write("student_name,grade\nИван Иванов,85\nМария Петрова,92\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])
            result = reader.read()

            assert len(result) == 2
            assert result[0] == {"student_name": "Иван Иванов", "grade": "85"}
            assert result[1] == {"student_name": "Мария Петрова", "grade": "92"}

        finally:
            os.unlink(temp_file)

    def test_read_multiple_files(self):
        """Тест чтения нескольких CSV файлов."""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f1:
            f1.write("student_name,grade\nИван Иванов,85\n")
            temp_file1 = f1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f2:
            f2.write("student_name,grade\nМария Петрова,92\n")
            temp_file2 = f2.name

        try:
            reader = CsvReader([temp_file1, temp_file2])
            result = reader.read()

            assert len(result) == 2
            assert result[0]["student_name"] == "Иван Иванов"
            assert result[1]["student_name"] == "Мария Петрова"

        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)

    def test_read_empty_file(self):
        """Тест чтения пустого CSV файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("student_name,grade\n")
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
            f.write("name,score\nИван,85\n")
            temp_file = f.name

        try:
            reader = CsvReader([temp_file])

            result = reader.read()
            assert result == [{"name": "Иван", "score": "85"}]

        finally:
            os.unlink(temp_file)

    def test_read_empty_file_list(self):
        """Тест поведения при пустом списке файлов."""
        reader = CsvReader([])

        with pytest.raises(ValueError, match="Файлы не содержат данных или пустые"):
            reader.read()


if __name__ == "__main__":
    pytest.main([__file__])
