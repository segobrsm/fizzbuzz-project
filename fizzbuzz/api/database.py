import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


def commit_changes():
    db.session.commit()


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()


def get_instance(model, **kwargs):
    return model.query.filter_by(**kwargs).first()
