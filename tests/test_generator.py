import pytest
from core.generator import AverageRatingReportGenerator


class TestCsvGenerator:
    """Тесты для CsvReportGenerator"""

    def test_generate_valid_data(self, sample_students_data):
        generator = AverageRatingReportGenerator(sample_students_data)
        result = generator.generate()

        assert isinstance(result, dict)
        assert len(result) == 3

        assert result["xiomi"] == 4.5
        assert result["apple"] == 4.5
        assert result["samsung"] == 5.0

        students = list(result.items())
        assert students[0][0] == "samsung"
        assert students[1][0] == "apple"
        assert students[2][0] == "xiomi"

    def test_generate_empty_data(self, empty_students_data):
        """Тест генерации отчета из пустых данных."""
        generator = AverageRatingReportGenerator(empty_students_data)

        with pytest.raises(ValueError, match="Файлы ничего не содержат"):
            generator.generate()

    def test_generate_invalid_grade_format(self):
        """Тест обработки некорректного формата рейтинга."""
        invalid_data = [
            {"brand": "xiomi", "rating": "пять"},
        ]

        generator = AverageRatingReportGenerator(invalid_data)

        with pytest.raises(ValueError, match="Неправильный формат файла"):
            generator.generate()

    def test_generate_missing_required_fields(self, invalid_students_data):
        """Тест обработки данных с отсутствующими обязательными полями."""
        generator = AverageRatingReportGenerator(invalid_students_data)

        with pytest.raises((KeyError, ValueError)):
            generator.generate()

    def test_generate_single_student(self):
        """Тест генерации отчета для одного продукта."""
        single_student_data = [
            {"brand": "xiomi", "rating": "5"},
            {"brand": "xiomi", "rating": "4"},
            {"brand": "xiomi", "rating": "3"},
        ]

        generator = AverageRatingReportGenerator(single_student_data)
        result = generator.generate()

        assert result == {"xiomi": 4.0}

    def test_generate_same_grades(self):
        """Тест когда у всех продуктов одинаковый рейтинг."""
        same_rating_data = [
            {"brand": "samsung", "rating": "4"},
            {"brand": "xiomi", "rating": "4"},
            {"brand": "apple", "rating": "4"},
        ]

        generator = AverageRatingReportGenerator(same_rating_data)
        result = generator.generate()

        assert all(rating == 4.0 for rating in result.values())
        students = list(result.keys())
        assert students == ["apple", "samsung", "xiomi"]
