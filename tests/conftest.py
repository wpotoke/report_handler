import pytest


@pytest.fixture
def sample_students_data():
    """Фикстура с примером данных студентов."""
    return [
        {
            "student_name": "Иванов Алексей",
            "subject": "Математика",
            "teacher_name": "Петрова Ольга",
            "date": "2023-09-10",
            "grade": "5",
        },
        {
            "student_name": "Петрова Мария",
            "subject": "Физика",
            "teacher_name": "Сидоров Иван",
            "date": "2023-09-12",
            "grade": "4",
        },
        {
            "student_name": "Иванов Алексей",
            "subject": "Физика",
            "teacher_name": "Сидоров Иван",
            "date": "2023-09-15",
            "grade": "3",
        },
        {
            "student_name": "Сидоров Петр",
            "subject": "Математика",
            "teacher_name": "Петрова Ольга",
            "date": "2023-09-11",
            "grade": "5",
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
        {"student_name": "Иванов Алексей"},
        {"grade": "5"},
        {"invalid_key": "invalid_value"},
    ]


@pytest.fixture
def sample_report_data():
    """Фикстура с примером данных для отчета."""
    return {
        "Иванов Алексей": 4.5,
        "Петрова Мария": 4.8,
        "Сидоров Петр": 3.9,
        "Козлова Анна": 4.2,
    }


@pytest.fixture
def empty_report_data():
    """Фикстура с пустым отчетом."""
    return {}


@pytest.fixture
def single_student_report():
    """Фикстура с отчетом по одному студенту."""
    return {"Иванов Алексей": 4.5}


@pytest.fixture
def sorted_report_data():
    """Фикстура с данными, проверяющими сортировку."""
    return {
        "Сидоров Петр": 5.0,
        "Петрова Мария": 4.8,
        "Иванов Алексей": 4.8,
        "Козлова Анна": 4.2,
    }
