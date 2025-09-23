import csv


class CsvReader:

    def __init__(self, files: list[str]):
        self.files = files

    def read(self) -> list[dict[str, str]]:
        students = []

        for file in self.files:
            with open(file, newline="", encoding="utf-8") as csvfile:
                c = csv.DictReader(csvfile)

                for i in c:
                    students.append(i)
                csvfile.close()
        return students
