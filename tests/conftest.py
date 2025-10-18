import pytest


@pytest.fixture
def sample_students_data():
    """Фикстура с примером данных продуктов."""
    return [
        {
            "brand": "xiomi",
            "rating": "4",
        },
        {
            "brand": "apple",
            "rating": "4.5",
        },
        {
            "brand": "xiomi",
            "rating": "5",
        },
        {
            "brand": "samsung",
            "rating": "5",
        },
    ]


@pytest.fixture
def empty_students_data():
    """Фикстура с пустыми данными."""
    return []


@pytest.fixture
def invalid_students_data():
    """Фикстура с некорректными данными."""
    return [
        {"brand": "xiomi"},
        {"rating": "3.4"},
        {"invalid_key": "invalid_value"},
    ]


@pytest.fixture
def sample_report_data():
    """Фикстура с примером данных для отчета."""
    return {
        "xiomi": 4.5,
        "apple": 4.8,
        "honor": 3.9,
        "samsung": 4.2,
    }


@pytest.fixture
def empty_report_data():
    """Фикстура с пустым отчетом."""
    return {}


@pytest.fixture
def single_student_report():
    """Фикстура с отчетом по одному продукту."""
    return {"apple": 4.5}


@pytest.fixture
def sorted_report_data():
    """Фикстура с данными, проверяющими сортировку."""
    return {
        "samsung": 5.0,
        "apple": 4.8,
        "xiomi": 4.8,
        "nokia": 4.2,
    }
