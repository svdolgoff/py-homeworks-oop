# Задание № 1. Наследование.
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Список закрепленных курсов

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    """Лекторы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)  # Наследует список курсов от родителя


class Reviewer(Mentor):
    """Ревьюверы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)  # Наследует список курсов от родителя


# Пример из задания (students_and_mentor.py):
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']

# Лектор и ревьювер
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')

# Курсы, унаследованные от родителя
reviewer.courses_attached += ['Python']
lecturer.courses_attached += ['Python']

# Проверки из задания
print(isinstance(lecturer, Mentor))  # True
print(isinstance(reviewer, Mentor))  # True
print(lecturer.courses_attached)     # []
print(reviewer.courses_attached)     # []


# Задание № 2. Атрибуты и взаимодействие классов.
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        """Метод для выставления оценок лекторам"""
        # Проверка на то, что оценка от 1 до 10
        if not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 1 до 10'

        # Проверка, что оценивается лектор
        if not isinstance(lecturer, Lecturer):
            return f"Ошибка: {lecturer.name} {lecturer.surname} не является лектором"

        # Проверка, что курс есть у студента
        if course not in self.courses_in_progress:
            return f"Ошибка: студент {self.name} {self.surname} не записан на курс {course}"

        # Проверка, что курс есть у лектора
        if course not in lecturer.courses_attached:
            return f"Ошибка: лектор {lecturer.name} {lecturer.surname} не ведет курс {course}"

        # Добавление оценки лектору
        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]

        # Возвращаем None при успешном выполнении
        return None


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Список закрепленных курсов родителя

    def rate_hw(self, student, course, grade):
        """Метод для выставления оценок студентам"""
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    """Лекторы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # Словарь для хранения оценок от студентов


class Reviewer(Mentor):
    """Ревьюверы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        """Переопределенный метод для выставления оценок студентам"""
        # Проверка, что оценка в диапазоне от 1 до 10
        if not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 1 до 10'

        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            return None  # Возвращаем None при успехе
        else:
            return 'Ошибка'


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'C++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка

print(lecturer.grades)  # {'Python': [7]}


# Задание № 3. Полиморфизм и магические методы
# Задание № 4. Полевые испытания
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, grade):
        """Метод для выставления оценок лекторам"""
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            # Разрешаем оценивать, если курс либо в процессе, либо завершен
            if course in self.courses_in_progress or course in self.finished_courses:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                print('Ошибка: студент не изучал этот курс')
                return
        else:
            print('Ошибка: лектор не ведет этот курс')
            return

    def __lt__(self, other):
        """Сравнение студентов через '<', '>' по средней оценке за домашние задания"""
        if not isinstance(other, Student):
            print('Сравнивать можно только студентов')
            return None
        return self.average_rating() < other.average_rating()

    def average_rating(self):
        """Вычисляет среднюю оценку студента"""
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if all_grades:
            return sum(all_grades) / len(all_grades)
        return 0

    def __str__(self):
        courses_in_progress_string = ', '.join(self.courses_in_progress) if self.courses_in_progress else 'нет'
        finished_courses_string = ', '.join(self.finished_courses) if self.finished_courses else 'нет'

        avg_rating = self.average_rating()

        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_rating:.1f}\n'
                f'Курсы в процессе изучения: {courses_in_progress_string}\n'
                f'Завершенные курсы: {finished_courses_string}')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        """Метод для выставления оценок студентам"""
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    """Лекторы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_rating(self):
        """Вычисляет среднюю оценку лектора"""
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if all_grades:
            return sum(all_grades) / len(all_grades)
        return 0

    def __str__(self):
        avg_grade = self.average_rating()
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade:.1f}'

    def __lt__(self, other):
        """Сравнение лекторов через '<', '>' по средней оценке за лекции"""
        if not isinstance(other, Lecturer):
            print('Сравнивать можно только лекторов')
            return None
        return self.average_rating() < other.average_rating()


class Reviewer(Mentor):
    """Ревьюверы, наследуются от Mentor"""
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# Список лекторов, закрепленных за курсами
best_lecturer_1 = Lecturer('Иван', 'Петров')
best_lecturer_1.courses_attached += ['Python с нуля']

best_lecturer_2 = Lecturer('Степан', 'Степанов')
best_lecturer_2.courses_attached += ['Java']

best_lecturer_3 = Lecturer('Антон', 'Антонов')
best_lecturer_3.courses_attached += ['Введение в программирование']

# Список ревьюверов, закрепленных за курсами
cool_reviewer_1 = Reviewer('Гомер', 'Симпсон')
cool_reviewer_1.courses_attached += ['Python с нуля']
cool_reviewer_1.courses_attached += ['Java']
cool_reviewer_1.courses_attached += ['Введение в программирование']

cool_reviewer_2 = Reviewer('Лиза', 'Симпсон')
cool_reviewer_2.courses_attached += ['Python с нуля']
cool_reviewer_2.courses_attached += ['Java']
cool_reviewer_2.courses_attached += ['Введение в программирование']

cool_reviewer_3 = Reviewer('Барт', 'Симпсон')
cool_reviewer_3.courses_attached += ['Python с нуля']
cool_reviewer_3.courses_attached += ['Java']
cool_reviewer_3.courses_attached += ['Введение в программирование']

# Список студентов и курсов 'в процессе' и 'завершенные'
student_1 = Student('Сергей', 'Долгов', 'M')
student_1.courses_in_progress += ['Python с нуля']
student_1.courses_in_progress += ['Java']
student_1.finished_courses += ['Введение в программирование']

student_2 = Student('Тугарин', 'Змей', 'M')
student_2.courses_in_progress += ['Python с нуля']
student_2.courses_in_progress += ['Введение в программирование']
student_2.finished_courses += ['Java']

student_3 = Student('Левша', 'Тульский', 'M')
student_3.courses_in_progress += ['Python с нуля']
student_3.finished_courses += ['Введение в программирование']
student_3.finished_courses += ['Java']

# Выставляем оценки лекторам за лекции
student_1.rate_hw(best_lecturer_1, 'Python с нуля', 9)
student_1.rate_hw(best_lecturer_1, 'Python с нуля', 5)
student_1.rate_hw(best_lecturer_1, 'Python с нуля', 10)

student_1.rate_hw(best_lecturer_2, 'Java', 7)
student_1.rate_hw(best_lecturer_2, 'Java', 7)
student_1.rate_hw(best_lecturer_2, 'Java', 7)

student_1.rate_hw(best_lecturer_1, 'Python с нуля', 2)
student_1.rate_hw(best_lecturer_1, 'Python с нуля', 3)
student_1.rate_hw(best_lecturer_1, 'Python с нуля', 5)

student_2.rate_hw(best_lecturer_2, 'Java', 9)
student_2.rate_hw(best_lecturer_2, 'Java', 8)
student_2.rate_hw(best_lecturer_2, 'Java', 5)

student_3.rate_hw(best_lecturer_3, 'Введение в программирование', 8)
student_3.rate_hw(best_lecturer_3, 'Введение в программирование', 9)
student_3.rate_hw(best_lecturer_3, 'Введение в программирование', 6)

student_2.rate_hw(best_lecturer_1, 'Python с нуля', 3)
student_2.rate_hw(best_lecturer_1, 'Python с нуля', 8)
student_2.rate_hw(best_lecturer_1, 'Python с нуля', 9)

# Выставляем оценки студентам за домашние задания
cool_reviewer_1.rate_hw(student_1, 'Python с нуля', 8)
cool_reviewer_1.rate_hw(student_1, 'Python с нуля', 9)
cool_reviewer_1.rate_hw(student_1, 'Python с нуля', 10)

cool_reviewer_2.rate_hw(student_2, 'Java', 8)
cool_reviewer_2.rate_hw(student_2, 'Java', 7)
cool_reviewer_2.rate_hw(student_2, 'Java', 9)

cool_reviewer_3.rate_hw(student_3, 'Python с нуля', 8)
cool_reviewer_3.rate_hw(student_3, 'Python с нуля', 7)
cool_reviewer_3.rate_hw(student_3, 'Python с нуля', 9)
cool_reviewer_2.rate_hw(student_3, 'Python с нуля', 7)
cool_reviewer_2.rate_hw(student_3, 'Python с нуля', 7)
cool_reviewer_2.rate_hw(student_3, 'Python с нуля', 6)

# Выводим характеристики ревьюверов
print(f'Перечень ревьюверов:\n\n{cool_reviewer_1}\n\n{cool_reviewer_2}\n\n{cool_reviewer_3}')
print()
print()

# Выводим характеристики созданных и оцененных студентов
print(f'Перечень студентов:\n\n{student_1}\n\n{student_2}\n\n{student_3}')
print()
print()

# Выводим характеристики созданных и оцененных лекторов
print(f'Перечень лекторов:\n\n{best_lecturer_1}\n\n{best_lecturer_2}\n\n{best_lecturer_3}')
print()
print()

# Выводим результат сравнения студентов по средним оценкам за домашние задания
print(f'Результат сравнения студентов (по средним оценкам за ДЗ): '
      f'{student_1.name} {student_1.surname} < {student_2.name} {student_2.surname} = {student_1 < student_2}')
print()

# Выводим результат сравнения лекторов по средним оценкам за лекции
print(f'Результат сравнения лекторов (по средним оценкам за лекции): '
      f'{best_lecturer_1.name} {best_lecturer_1.surname} < {best_lecturer_2.name} {best_lecturer_2.surname} = {best_lecturer_1 < best_lecturer_2}')
print()

# Создаем список студентов
student_list = [student_1, student_2, student_3]

# Создаем список лекторов
lecturer_list = [best_lecturer_1, best_lecturer_2, best_lecturer_3]


# Создаем функцию для подсчета средней оценки за домашние задания
# по всем студентам в рамках конкретного курса
def student_rating(student_list, course_name):
    """Функция для подсчета средней оценки за домашние задания
    по всем студентам в рамках конкретного курса"""
    sum_all = 0
    count_all = 0
    for stud in student_list:
        if course_name in stud.courses_in_progress:
            sum_all += stud.average_rating()
            count_all += 1

    if count_all == 0:
        return 0

    return sum_all / count_all


# Создаем функцию для подсчета средней оценки за лекции всех лекторов в рамках курса
def lecturer_rating(lecturer_list, course_name):
    """Функция для подсчета средней оценки за лекции всех лекторов в рамках курса"""
    sum_all = 0
    count_all = 0
    for lect in lecturer_list:
        if course_name in lect.courses_attached:
            sum_all += lect.average_rating()
            count_all += 1

    if count_all == 0:
        return 0

    return sum_all / count_all


