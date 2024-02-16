import random

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Group, Student, Subject, Grade

fake = Faker('uk-UA')

STUDENTS = 45
GROUPS = 3
SUBJECTS = 6
TEACHERS = 3
GRADES = 810


def insert_groups():
    for _ in range(GROUPS):
        group = Group(
            name=fake.word()
        )
        session.add(group)


def insert_students():
    for group_id in range(1, GROUPS + 1):
        for _ in range(15):
            student = Student(
                fullname=fake.name(),
                group_id=group_id
            )
            session.add(student)


def insert_teachers():
    for _ in range(TEACHERS):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)


def insert_subjects():
    for teacher_id in range(1, TEACHERS + 1):
        for _ in range(2):
            subject = Subject(
                name=fake.job(),
                teacher_id=teacher_id
            )
            session.add(subject)


def insert_grades():
    for _ in range(3):
        for student_id in range(1, STUDENTS + 1):
            for subject_id in range(1, SUBJECTS + 1):
                grade = Grade(
                    grade=random.randint(0, 100),
                    grade_date=fake.date_this_year(),
                    student_id=student_id,
                    subject_id=subject_id
                )
                session.add(grade)


if __name__ == '__main__':
    try:
        insert_groups()
        insert_students()
        insert_teachers()
        insert_subjects()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
