import argparse

from sqlalchemy.exc import SQLAlchemyError

from conf.models import Teacher, Subject, Group, Student, Grade
from conf.db import session

from abc import ABC, abstractmethod

parser = argparse.ArgumentParser(
    prog='Database Updater',
    description='Adds information to the database')

parser.add_argument('-a', '--action', required=True)
parser.add_argument('-m', '--model', required=True)
parser.add_argument('-id', '--id', required=False)
parser.add_argument('-n', '--name', required=False)
parser.add_argument('-g', '--grade', required=False)
parser.add_argument('-gd', '--grade_date', required=False)
parser.add_argument('-st_id', '--student_id', required=False)
parser.add_argument('-su_id', '--subject_id', required=False)

args = vars(parser.parse_args())

action = args.get('action')
model = args.get('model')
identifier = args.get('id')
name = args.get('name')
grade = args.get('grade')
grade_date = args.get('grade_date')
student_id = args.get('student_id')
subject_id = args.get('subject_id')


def action_validation(action):
    action_commands = ['create', 'list', 'update', 'remove']
    try:
        if action not in action_commands:
            raise ValueError(f'Invalid action: {action}')
        return action
    except ValueError as err:
        print(err)


class AbstractBot(ABC):
    def __init__(self, name=None):
        self.name = name

    @abstractmethod
    def handle(self):
        pass


class InsertCommand(AbstractBot):
    def __init__(self, name, teacher_id=None, grade=None, grade_date=None, student_id=None, subject_id=None):
        super().__init__(name)
        self.name = name
        self.teacher_id = teacher_id
        self.grade = grade
        self.grade_date = grade_date
        self.student_id = student_id
        self.subject_id = subject_id

    def handle(self):
        self.insert_data(self.name, self.teacher_id)

    def insert_data(self, name, identifier=None):
        if model == 'Teacher':
            teacher = Teacher(
                fullname=name
            )
            session.add(teacher)
            print(f'Teacher "{name}" has been added successfully.')
            return

        elif model == 'Subject':
            subject = Subject(
                name=name,
                teacher_id=identifier
            )
            session.add(subject)
            print(f'Subject "{name}" has been added successfully.')

        elif model == 'Group':
            group = Group(
                name=name,
            )
            session.add(group)
            print(f'Group "{name}" has been added successfully.')

        elif model == 'Student':
            student = Student(
                fullname=name,
                group_id=identifier
            )
            session.add(student)
            print(f'Student "{name}" has been added successfully.')

        elif model == 'Grade':
            grade = Grade(
                grade=self.grade,
                grade_date=self.grade_date,
                student_id=self.student_id,
                subject_id=self.subject_id
            )
            session.add(grade)
            print(f'Grade has been added successfully.')


class ListCommand(AbstractBot):
    def handle(self):
        self.list_data()

    def list_data(self):
        if model == 'Teacher':
            result = (session.query(Teacher.id, Teacher.fullname).select_from(Teacher).order_by(Teacher.id).all())
            print(f'List of all teachers:\n', result)

        elif model == 'Subject':
            result = (session.query(Subject.id, Subject.name, Subject.teacher_id).select_from(Subject).order_by(
                Subject.id).all())
            print(f'List of all subjects:\n', result)

        elif model == 'Group':
            result = (session.query(Group.id, Group.name).select_from(Group).order_by(Group.id).all())
            print(f'List of all groups:\n', result)

        elif model == 'Student':
            result = (session.query(Student.id, Student.fullname, Student.group_id).select_from(Student).order_by(
                Student.id).all())
            print(f'List of all students:\n', result)

        elif model == 'Grade':
            result = (
                session.query(Grade.id, Grade.grade, Grade.grade_date, Grade.student_id, Grade.subject_id).select_from(
                    Grade).order_by(
                    Grade.id).all())
            print(f'List of all grades:\n', result)


class UpdateCommand(AbstractBot):
    def __init__(self, name, teacher_id=None, new_name=None):
        super().__init__(name)
        self.name = name
        self.teacher_id = teacher_id
        self.new_name = new_name

    def handle(self):
        self.update_data(self.name, self.teacher_id)

    def update_data(self, identifier=None, new_name=None):
        if model == 'Teacher':
            teacher = (session.query(Teacher).filter(Teacher.id == identifier).first())
            teacher.fullname = new_name
            session.commit()
            print(f"The name of the teacher with ID {identifier} has been updated to '{new_name}'.")

        elif model == 'Subject':
            subject = (session.query(Subject).filter(Subject.id == identifier).first())
            subject.name = new_name
            session.commit()
            print(f"The name of the subject with ID {identifier} has been updated to '{new_name}'.")


class RemoveCommand(AbstractBot):
    def __init__(self, identifier, name=None, teacher_id=None, new_name=None):
        super().__init__(name)
        self.name = name
        self.teacher_id = teacher_id
        self.new_name = new_name
        self.identifier = identifier

    def handle(self):
        self.remove_data(self.identifier)

    def remove_data(self, identifier):
        if model == 'Teacher':
            teacher = (session.query(Teacher).filter(Teacher.id == identifier).first())
            session.delete(teacher)
            session.commit()
            print(f"The teacher with ID {identifier} has been removed.")

        elif model == 'Subject':
            subject = (session.query(Subject).filter(Subject.id == identifier).first())
            session.delete(subject)
            session.commit()
            print(f"The subject with ID {identifier} has been removed.")


if __name__ == '__main__':
    try:
        action_validation(action)
        if action == 'create' and model == 'Grade':
            InsertCommand(name, grade=grade, grade_date=grade_date, student_id=student_id,
                          subject_id=subject_id).handle()
        else:
            choice = {
                'create': InsertCommand(name, identifier),
                'list': ListCommand(),
                'update': UpdateCommand(identifier, name),
                'remove': RemoveCommand(identifier),
            }
            if action in choice:
                choice[action].handle()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
