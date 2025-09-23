import pytest
from core.generator import CsvReportGenerator


class TestCsvGenerator:
    """Тесты для CsvReportGenerator"""

    def test_generate_valid_data(self, sample_students_data):
        generator = CsvReportGenerator(sample_students_data)
        result = generator.generate()

        assert isinstance(result, dict)
        assert len(result) == 3

        assert result["Иванов Алексей"] == 4.0
        assert result["Петрова Мария"] == 4.0
        assert result["Сидоров Петр"] == 5.0

        students = list(result.items())
        assert students[0][0] == "Сидоров Петр"
        assert students[1][0] == "Иванов Алексей"
        assert students[2][0] == "Петрова Мария"

    def test_generate_empty_data(self, empty_students_data):
        """Тест генерации отчета из пустых данных."""
        generator = CsvReportGenerator(empty_students_data)

        with pytest.raises(ValueError, match="Файлы ничего не содержат"):
            generator.generate()

    def test_generate_invalid_grade_format(self):
        """Тест обработки некорректного формата оценок."""
        invalid_data = [
            {"student_name": "Иванов Алексей", "grade": "пять"},
        ]

        generator = CsvReportGenerator(invalid_data)

        with pytest.raises(ValueError, match="Неправильный формат файла"):
            generator.generate()

    def test_generate_missing_required_fields(self, invalid_students_data):
        """Тест обработки данных с отсутствующими обязательными полями."""
        generator = CsvReportGenerator(invalid_students_data)

        with pytest.raises((KeyError, ValueError)):
            generator.generate()

    def test_generate_single_student(self):
        """Тест генерации отчета для одного студента."""
        single_student_data = [
            {"student_name": "Иванов Алексей", "grade": "5"},
            {"student_name": "Иванов Алексей", "grade": "4"},
            {"student_name": "Иванов Алексей", "grade": "3"},
        ]

        generator = CsvReportGenerator(single_student_data)
        result = generator.generate()

        assert result == {"Иванов Алексей": 4.0}

    def test_generate_same_grades(self):
        """Тест когда у всех студентов одинаковые оценки."""
        same_grades_data = [
            {"student_name": "Иванов Алексей", "grade": "4"},
            {"student_name": "Петрова Мария", "grade": "4"},
            {"student_name": "Сидоров Петр", "grade": "4"},
        ]

        generator = CsvReportGenerator(same_grades_data)
        result = generator.generate()

        assert all(grade == 4.0 for grade in result.values())
        students = list(result.keys())
        assert students == ["Иванов Алексей", "Петрова Мария", "Сидоров Петр"]
