from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum, auto
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class TaskPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class ObjectStatus(Enum):
    NOT_STARTED = auto()
    IN_PROCESS = auto()
    FINISHED = auto()


class TaskType(Enum):
    JOB = auto()
    HOUSE_TASKS = auto()
    WORKOUT = auto()
    PERSONAL_PROJECTS = auto()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    projects = db.relationship("Project", back_populates="user")
    tasks = db.relationship("Task", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        
    def is_correct_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.Enum(ObjectStatus))
    initial_date = db.Column(db.Date, nullable=False)
    finished_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="projects")
    tasks = db.relationship("Task", back_populates="project")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    initial_date = db.Column(db.Date, nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Enum(TaskPriority), nullable=False)
    type = db.Column(db.Enum(TaskType), nullable=False)
    status = db.Column(db.Enum(ObjectStatus), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    user = db.relationship("User", back_populates="tasks")
    project = db.relationship("Project", back_populates="tasks")

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

