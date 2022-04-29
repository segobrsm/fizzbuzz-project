from api.database import db


class FizzBuzz(db.Model):
    __tablename__ = 'fizzbuzz'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    int1 = db.Column(db.Integer, nullable=False)
    int2 = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    str1 = db.Column(db.String(80), nullable=False)
    str2 = db.Column(db.String(80), nullable=False)
    nb_hit = db.Column(db.Integer, nullable=False, default=1)
