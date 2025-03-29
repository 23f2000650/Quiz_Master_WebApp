from sqlalchemy import (
    DateTime, func, Date, Column, Integer, String, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import os
from utils import IndianTimeZone, format_ist_datetime
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
import os

# Load from environment variable or fallback to default
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    dob = Column(Date, nullable=False)
    qualification = Column(String(50), nullable=False)
    role = Column(String(10), nullable=False, default="student")
    password = Column(String(200), nullable=False)

    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")

class Subject(db.Model):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(120), nullable=False)
    credit = Column(Integer, nullable=False)

    chapters = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")

    def to_dict(self):
        quiz_count = sum(len(chapter.quizzes) for chapter in self.chapters)
        student_attempted_count = (
            db.session.query(func.count(func.distinct(QuizResult.user_id)))
            .join(Quiz, Quiz.id == QuizResult.quiz_id)
            .join(Chapter, Chapter.id == Quiz.chapter_id)
            .filter(Chapter.subject_id == self.id)
            .scalar()
        )
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "credit": self.credit,
            "quiz_count": quiz_count,
            "students": student_attempted_count,
            "chapters": len(self.chapters),
        }

class Chapter(db.Model):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(120), nullable=False)

    quizzes = relationship("Quiz", back_populates="chapter", cascade="all, delete-orphan")
    subject = relationship("Subject", back_populates="chapters")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject_id": self.subject_id,
            "total_quizzes": len(self.quizzes),
        }

class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(120), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    time_duration = Column(Integer, nullable=False, default=0)
    deadline = Column(DateTime, nullable=True)
    one_attempt_only = Column(Boolean, default=True)

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")
    chapter = relationship("Chapter", back_populates="quizzes")

    def is_available(self):
        return not self.deadline or datetime.now() < self.deadline

    def has_attempted(self, user_id):
        return QuizResult.query.filter_by(user_id=user_id, quiz_id=self.id).first() is not None

    def get_status_message(self):
        if not self.deadline:
            return "Available"
        return f"Available until {self.deadline.strftime('%Y-%m-%d %H:%M')} IST" if self.is_available() else f"Deadline passed on {self.deadline.strftime('%Y-%m-%d %H:%M')} IST"

    @staticmethod
    def parse_deadline(deadline_str):
        if not deadline_str:
            return None
        try:
            return datetime.fromisoformat(deadline_str.replace("Z", "+00:00"))
        except ValueError:
            return datetime.strptime(deadline_str, "%d-%m-%YT%H:%M")

class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question = Column(String(255), nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    answer = Column(String(1), nullable=False)
    quiz = relationship("Quiz", back_populates="questions")


# ||----------------------Quiz Result Model----------------------||#
class QuizResult(db.Model):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    marks_scored = Column(Integer, nullable=True)
    total_marks = Column(Integer, nullable=True)
    completed_at = Column(DateTime, default=IndianTimeZone())

    user = relationship("User", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="quiz_results")
    # user_answers = relationship(
    #     "UserAnswer", back_populates="quiz_result", cascade="all, delete", lazy="joined"
    # )
    
    

# ||----------------------User Answer Model (Move it up)----------------------||#
# class UserAnswer(db.Model):
#     __tablename__ = "user_answers"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     result_id = Column(
#         Integer, ForeignKey("quiz_results.id", ondelete="CASCADE"), nullable=False
#     )
#     question_id = Column(
#         Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
#     )
#     selected_option = Column(String(1), nullable=True)  # Fix: No FK needed here
#     is_correct = Column(Boolean, default=False)

#     quiz_result = relationship("QuizResult", back_populates="user_answers")
#     question = relationship("Question", backref="user_answers")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email="admin@gmail.com").first():
            admin_user = User(name="admin",
                            email="admin@gmail.com",
                            password=generate_password_hash("000"),
                            role="admin", qualification="N/A",
                            dob=datetime.utcnow())
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")
