# models.py
from . import db
from flask_login import UserMixin

# Association table for Many-to-Many relationship between Students and Teachers
student_teacher = db.Table('student_teacher',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Role field to differentiate user types

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    enrolled_courses = db.relationship('Course', backref='student', lazy=True)
    teachers = db.relationship('Teacher', secondary=student_teacher, backref='students', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Teacher(User):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    courses_taught = db.relationship('Course', backref='teacher', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

class Administrator(User):
    __tablename__ = 'administrator'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    admin_code = db.Column(db.String(20), unique=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'administrator',
    }

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
