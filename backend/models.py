from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_name = "trivia"
database_path = f'postgresql://postgres:solidsnake208@localhost:5432/{database_name}'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, db_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        success = True
        try:
            db.session.add(self)
            db.session.commit()
        except():
            db.session.rollback()
            success = False
        return success

    def update(self):
        success = True
        try:
            db.session.commit()
        except():
            db.session.rollback()
            success = False
        return success

    def delete(self):
        success = True
        try:
            db.session.delete(self)
            db.session.commit()
        except():
            db.session.rollback()
            success = False
        return success

    def format(self):
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
          'id': self.id,
          'type': self.type
        }
